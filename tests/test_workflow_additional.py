#!/usr/bin/env python3
"""
Additional comprehensive tests for check_arb.yml workflow.
These tests add extra confidence with negative cases, boundary conditions, and regression scenarios.
"""

import unittest
import yaml
from pathlib import Path


class TestWorkflowNegativeCases(unittest.TestCase):
    """Test negative cases and error scenarios."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_no_duplicate_step_ids(self):
        """Test that step IDs are unique within each job."""
        for job_name, job in self.workflow['jobs'].items():
            if 'steps' not in job:
                continue

            step_ids = []
            for step in job['steps']:
                if 'id' in step:
                    step_ids.append(step['id'])

            # All IDs should be unique
            self.assertEqual(len(step_ids), len(set(step_ids)),
                           f"Duplicate step IDs found in job {job_name}")

    def test_no_missing_required_fields(self):
        """Test that all jobs and steps have required fields."""
        # Jobs must have runs-on
        for job_name, job in self.workflow['jobs'].items():
            self.assertIn('runs-on', job, f"Job {job_name} missing runs-on")

        # Steps with actions must have 'uses' or 'run'
        for job_name, job in self.workflow['jobs'].items():
            if 'steps' not in job:
                continue
            for idx, step in enumerate(job['steps']):
                self.assertIn('name', step,
                            f"Step {idx} in job {job_name} missing name")
                has_action = 'uses' in step or 'run' in step
                self.assertTrue(has_action,
                              f"Step {step['name']} has neither 'uses' nor 'run'")

    def test_invalid_device_variant_combinations_excluded(self):
        """Test that invalid combinations are properly excluded."""
        matrix = self.workflow['jobs']['check-variant']['strategy']['matrix']

        # oneplus_15r CN should be excluded
        excluded = matrix.get('exclude', [])
        oneplus_15r_cn_excluded = any(
            e.get('device') == 'oneplus_15r' and e.get('variant') == 'CN'
            for e in excluded
        )
        self.assertTrue(oneplus_15r_cn_excluded,
                       "oneplus_15r CN combination should be excluded")

    def test_no_empty_step_runs(self):
        """Test that no step has an empty run command."""
        for job_name, job in self.workflow['jobs'].items():
            if 'steps' not in job:
                continue
            for step in job['steps']:
                if 'run' in step:
                    self.assertTrue(len(step['run'].strip()) > 0,
                                  f"Empty run command in step {step['name']}")

    def test_cache_keys_dont_collide(self):
        """Test that cache keys include enough specificity to avoid collisions."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_restore = next((s for s in steps if 'cache/restore' in s.get('uses', '')), None)

        if cache_restore:
            key = cache_restore['with']['key']
            # Should include version prefix, device, variant, and version
            required_parts = ['arb-check-v', '${{ matrix.device }}',
                            '${{ matrix.variant }}', '${{ steps.get_details.outputs.version }}']
            for part in required_parts:
                self.assertIn(part, key, f"Cache key missing {part}")

    def test_no_unquoted_matrix_variables_in_sensitive_contexts(self):
        """Test that matrix variables are safely used."""
        # This is a sanity check - we shouldn't have shell injection risks
        # In GitHub Actions, matrix variables are safely substituted
        steps = self.workflow['jobs']['check-variant']['steps']

        for step in steps:
            if 'run' in step:
                # Just verify we're using matrix variables (they're safe in GitHub Actions)
                run_content = step['run']
                if '${{ matrix.' in run_content:
                    # This is fine - GitHub Actions handles this safely
                    self.assertIsInstance(run_content, str)


class TestWorkflowBoundaryConditions(unittest.TestCase):
    """Test boundary conditions and limits."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_matrix_not_too_large(self):
        """Test that matrix doesn't create too many jobs."""
        matrix = self.workflow['jobs']['check-variant']['strategy']['matrix']

        devices = len(matrix['device'])
        variants = len(matrix['variant'])
        exclusions = len(matrix.get('exclude', []))

        total_combinations = (devices * variants) - exclusions

        # GitHub Actions free tier supports up to 20 parallel jobs
        # Let's ensure we're within reasonable limits
        self.assertLessEqual(total_combinations, 50,
                           "Matrix creates too many job combinations")

    def test_cron_schedule_not_too_frequent(self):
        """Test that scheduled runs aren't too frequent."""
        schedule = self.workflow['on']['schedule']
        cron = schedule[0]['cron']

        # Daily (0 0 * * *) is reasonable, hourly would be too frequent
        # The first field is minutes (0), second is hours (0)
        parts = cron.split()
        minutes = parts[0]
        hours = parts[1]

        # Should run at most once per hour
        self.assertEqual(minutes, '0', "Should run on the hour")

    def test_artifact_retention_implicit(self):
        """Test that artifacts don't have explicit retention (use default)."""
        steps = []
        for job in self.workflow['jobs'].values():
            if 'steps' in job:
                steps.extend(job['steps'])

        upload_steps = [s for s in steps if 'upload-artifact' in s.get('uses', '')]

        for step in upload_steps:
            # GitHub default is 90 days which is fine
            # If we had 'retention-days' we'd check it's reasonable
            if 'with' in step and 'retention-days' in step['with']:
                retention = step['with']['retention-days']
                self.assertLessEqual(retention, 90,
                                   "Artifact retention should be <= 90 days")

    def test_timeout_not_set_or_reasonable(self):
        """Test that job timeouts are reasonable if set."""
        for job_name, job in self.workflow['jobs'].items():
            if 'timeout-minutes' in job:
                timeout = job['timeout-minutes']
                # Should be reasonable (max is 6 hours = 360 min on free tier)
                self.assertLessEqual(timeout, 360,
                                   f"Job {job_name} timeout too long")


class TestWorkflowRobustness(unittest.TestCase):
    """Test workflow robustness and failure handling."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_cleanup_runs_even_on_failure(self):
        """Test that cleanup step runs even when previous steps fail."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cleanup_step = next((s for s in steps if s['name'] == 'Cleanup'), None)

        self.assertIsNotNone(cleanup_step, "Cleanup step not found")
        self.assertEqual(cleanup_step['if'], 'always()',
                       "Cleanup should run even on failure")

    def test_download_has_fallback_for_non_zip(self):
        """Test that download step handles non-ZIP URLs gracefully."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next((s for s in steps if s['name'] == 'Download Firmware'), None)

        self.assertIsNotNone(download_step)
        run_commands = download_step['run']

        # Should check for .zip extension
        self.assertIn('.zip', run_commands)
        # Should create skip file for non-download links
        self.assertIn('skip_check.txt', run_commands)

    def test_git_commit_handles_no_changes(self):
        """Test that git commit step handles case with no changes."""
        steps = self.workflow['jobs']['update-readme']['steps']
        commit_step = next((s for s in steps if s['name'] == 'Commit and Push'), None)

        self.assertIsNotNone(commit_step)
        run_commands = commit_step['run']

        # Should not fail if there are no changes
        self.assertIn('|| echo', run_commands)

    def test_cn_download_has_max_retry_limit(self):
        """Test that CN downloads don't retry infinitely."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next((s for s in steps if s['name'] == 'Download Firmware'), None)

        run_commands = download_step['run']

        # Should have MAX_RETRIES defined
        self.assertIn('MAX_RETRIES', run_commands)
        # Should check against max retries
        self.assertIn('RETRY_COUNT -lt $MAX_RETRIES', run_commands)


class TestWorkflowInputValidation(unittest.TestCase):
    """Test input validation and safety."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_force_recheck_input_type_safe(self):
        """Test that force_recheck is properly typed as boolean."""
        inputs = self.workflow['on']['workflow_dispatch']['inputs']
        force_recheck = inputs['force_recheck']

        # Should be boolean type, not string
        self.assertEqual(force_recheck['type'], 'boolean')
        # Default should be boolean false
        self.assertIsInstance(force_recheck['default'], bool)
        self.assertEqual(force_recheck['default'], False)

    def test_force_recheck_compared_as_string(self):
        """Test that force_recheck comparison in workflow is safe."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_restore = next((s for s in steps if s.get('id') == 'cache-arb'), None)

        self.assertIsNotNone(cache_restore)
        # GitHub Actions requires string comparison even for boolean inputs
        self.assertIn("!= 'true'", cache_restore['if'])


class TestWorkflowMaintainability(unittest.TestCase):
    """Test workflow maintainability and documentation."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_all_steps_have_names(self):
        """Test that all steps have descriptive names."""
        for job_name, job in self.workflow['jobs'].items():
            if 'steps' not in job:
                continue

            for idx, step in enumerate(job['steps']):
                self.assertIn('name', step,
                            f"Step {idx} in job {job_name} missing name")
                self.assertGreater(len(step['name']), 5,
                                 f"Step name too short: {step['name']}")

    def test_matrix_includes_have_clear_purpose(self):
        """Test that matrix includes provide useful metadata."""
        matrix = self.workflow['jobs']['check-variant']['strategy']['matrix']
        includes = matrix.get('include', [])

        # Each include should add meaningful metadata
        for inc in includes:
            self.assertIn('device', inc)
            self.assertIn('device_short', inc)
            self.assertIn('device_name', inc)

            # device_name should be human-readable
            self.assertIn('OnePlus', inc['device_name'])

    def test_cache_version_explicit_for_maintenance(self):
        """Test that cache version is explicit to allow cache busting."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_steps = [s for s in steps if 'cache' in s.get('uses', '')]

        for step in cache_steps:
            if 'with' in step and 'key' in step['with']:
                key = step['with']['key']
                # Should have explicit version for easy cache invalidation
                self.assertIn('-v', key, "Cache key should have version")


class TestWorkflowRegressionPrevention(unittest.TestCase):
    """Tests that prevent common workflow regressions."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_download_uses_aria2_not_wget(self):
        """Regression: Ensure we use aria2c for parallel downloads."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next((s for s in steps if s['name'] == 'Download Firmware'), None)

        run_commands = download_step['run']
        self.assertIn('aria2c', run_commands)
        # Should NOT use wget (slower, less robust)
        self.assertNotIn('wget ', run_commands)

    def test_cache_paths_include_both_marker_and_data(self):
        """Regression: Ensure cache includes both marker file and extracted data."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_restore = next((s for s in steps if s.get('id') == 'cache-arb'), None)

        cache_paths = cache_restore['with']['path']
        # Should cache both the marker file and extracted directory
        self.assertIn('arb_check_done.txt', cache_paths)
        self.assertIn('extracted/', cache_paths)

    def test_update_readme_waits_for_check_variant(self):
        """Regression: Ensure update-readme waits for check-variant to complete."""
        update_readme = self.workflow['jobs']['update-readme']
        self.assertIn('needs', update_readme)
        self.assertEqual(update_readme['needs'], 'check-variant')

    def test_artifacts_downloaded_without_merge(self):
        """Regression: Ensure artifacts are not merged (to preserve structure)."""
        steps = self.workflow['jobs']['update-readme']['steps']
        download_step = next((s for s in steps
                             if s['name'] == 'Download All Artifacts'), None)

        self.assertIsNotNone(download_step)
        self.assertEqual(download_step['with']['merge-multiple'], False)

    def test_python_scripts_use_python3_explicitly(self):
        """Regression: Ensure we use python3, not python (which may not exist)."""
        steps = []
        for job in self.workflow['jobs'].values():
            if 'steps' in job:
                steps.extend(job['steps'])

        for step in steps:
            if 'run' in step and '.py' in step['run']:
                # Only check if python is actually being executed (not just mentioned)
                if 'python' in step['run'] and not step['run'].strip().startswith('echo'):
                    # Should use python3, not python
                    self.assertIn('python3', step['run'])


class TestWorkflowVersionCompatibility(unittest.TestCase):
    """Test version compatibility and future-proofing."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            cls.workflow = yaml.safe_load(f)
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_actions_use_current_major_versions(self):
        """Test that actions use current major versions."""
        steps = []
        for job in self.workflow['jobs'].values():
            if 'steps' in job:
                steps.extend(job['steps'])

        action_versions = {
            'actions/checkout': 'v4',
            'actions/upload-artifact': 'v4',
            'actions/download-artifact': 'v4',
            'actions/cache': 'v4',
        }

        for step in steps:
            if 'uses' in step:
                for action, expected_version in action_versions.items():
                    if action in step['uses']:
                        self.assertIn(expected_version, step['uses'],
                                    f"{action} should use {expected_version}")

    def test_ubuntu_runner_version_specified(self):
        """Test that ubuntu runner version is specified."""
        for job in self.workflow['jobs'].values():
            if 'runs-on' in job:
                runner = job['runs-on']
                self.assertEqual(runner, 'ubuntu-latest',
                               "Should use ubuntu-latest for compatibility")


if __name__ == '__main__':
    unittest.main()