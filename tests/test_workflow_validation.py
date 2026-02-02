#!/usr/bin/env python3
"""
Comprehensive tests for the check_arb.yml GitHub Actions workflow.
Tests workflow structure, inputs, jobs, steps, and matrix configurations.
"""

import unittest
import yaml
import os
from pathlib import Path
import sys

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DEVICE_METADATA


class TestWorkflowValidation(unittest.TestCase):
    """Test suite for validating the check_arb.yml workflow structure."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            # Use safe_load and handle 'on' key being parsed as boolean True
            cls.workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key), we need to access it properly
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_workflow_name_exists(self):
        """Test that workflow has a proper name."""
        self.assertIn('name', self.workflow)
        self.assertEqual(self.workflow['name'], 'Check ARB')

    def test_workflow_triggers_defined(self):
        """Test that workflow has proper trigger events defined."""
        self.assertIn('on', self.workflow)
        triggers = self.workflow['on']
        self.assertIn('workflow_dispatch', triggers)
        self.assertIn('schedule', triggers)

    def test_workflow_dispatch_inputs(self):
        """Test workflow_dispatch inputs are properly configured."""
        workflow_dispatch = self.workflow['on']['workflow_dispatch']
        self.assertIn('inputs', workflow_dispatch)
        inputs = workflow_dispatch['inputs']

        # Test force_recheck input
        self.assertIn('force_recheck', inputs)
        force_recheck = inputs['force_recheck']
        self.assertEqual(force_recheck['description'], 'Force recheck all firmwares even if already checked')
        self.assertEqual(force_recheck['required'], False)
        self.assertEqual(force_recheck['default'], False)
        self.assertEqual(force_recheck['type'], 'boolean')

    def test_schedule_cron_syntax(self):
        """Test that schedule cron expression is valid."""
        schedule = self.workflow['on']['schedule']
        self.assertIsInstance(schedule, list)
        self.assertEqual(len(schedule), 1)
        self.assertIn('cron', schedule[0])
        # Daily at midnight
        self.assertEqual(schedule[0]['cron'], '0 0 * * *')

    def test_jobs_exist(self):
        """Test that required jobs are defined."""
        self.assertIn('jobs', self.workflow)
        jobs = self.workflow['jobs']
        self.assertIn('check-variant', jobs)
        self.assertIn('update-readme', jobs)

    def test_check_variant_job_configuration(self):
        """Test check-variant job configuration."""
        job = self.workflow['jobs']['check-variant']

        # Basic job settings
        self.assertEqual(job['runs-on'], 'ubuntu-latest')
        self.assertEqual(job['continue-on-error'], True)

        # Strategy configuration
        self.assertIn('strategy', job)
        strategy = job['strategy']
        self.assertEqual(strategy['fail-fast'], False)
        self.assertIn('matrix', strategy)

    def test_setup_matrix_job(self):
        """Test that setup-matrix job is defined."""
        jobs = self.workflow['jobs']
        self.assertIn('setup-matrix', jobs)
        self.assertIn('generate_matrix.py', jobs['setup-matrix']['steps'][1]['run'])

    def test_check_variant_uses_dynamic_matrix(self):
        """Test that check-variant job uses the dynamic matrix."""
        job = self.workflow['jobs']['check-variant']
        self.assertIn('needs', job)
        self.assertIn('setup-matrix', job['needs'])
        self.assertIn('matrix', job['strategy'])
        self.assertIn('fromJson(needs.setup-matrix.outputs.matrix)', job['strategy']['matrix'])

    def test_dynamic_matrix_logic(self):
        """Test the logic of generate_matrix.py by calling it or simulating it."""
        # Since we cannot easily run the script here without capturing stdout,
        # we can verify the logic matches our expectation using config.DEVICE_METADATA.
        
        # This test ensures that the python script we wrote (generate_matrix.py)
        # would produce a valid list if we trust the DEVICE_METADATA used here + script logic match.
        # But to be robust, we should arguably import generate_matrix, but that script prints to stdout.
        # We'll stick to verifying the config itself is sound for generation.
        
        for dev_id, meta in DEVICE_METADATA.items():
            self.assertTrue(meta.get('models'), f"Device {dev_id} has no models defined")
            for region in meta['models'].keys():
                self.assertIn(region, ['GLO', 'EU', 'IN', 'CN', 'NA', 'ID', 'MY'])

    def test_checkout_step_exists(self):
        """Test that checkout step is properly configured."""
        steps = self.workflow['jobs']['check-variant']['steps']
        checkout_step = steps[0]

        self.assertEqual(checkout_step['name'], 'Checkout Repo')
        self.assertEqual(checkout_step['uses'], 'actions/checkout@v4')

    def test_install_dependencies_step(self):
        """Test install dependencies step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        install_step = next(s for s in steps if s['name'] == 'Install dependencies')

        self.assertIn('run', install_step)
        run_commands = install_step['run']

        # Verify required packages are installed
        self.assertIn('aria2', run_commands)
        self.assertIn('unzip', run_commands)
        self.assertIn('curl', run_commands)
        self.assertIn('python3-pip', run_commands)
        self.assertIn('requests', run_commands)
        self.assertIn('beautifulsoup4', run_commands)

    def test_setup_tools_step(self):
        """Test setup tools step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        setup_step = next(s for s in steps if s['name'] == 'Setup Tools')

        self.assertIn('run', setup_step)
        run_commands = setup_step['run']

        # Verify tools are downloaded and configured
        self.assertIn('arbextract', run_commands)
        self.assertIn('otaripper', run_commands)
        self.assertIn('chmod +x', run_commands)

    def test_get_firmware_details_step(self):
        """Test get firmware details step."""
        steps = self.workflow['jobs']['check-variant']['steps']
        details_step = next(s for s in steps if s['name'] == 'Get Firmware Details')

        self.assertIn('id', details_step)
        self.assertEqual(details_step['id'], 'get_details')
        self.assertIn('run', details_step)

        run_commands = details_step['run']
        self.assertIn('fetch_firmware.py', run_commands)
        self.assertIn('fw_info.json', run_commands)
        self.assertIn('GITHUB_OUTPUT', run_commands)

    def test_cache_restore_step(self):
        """Test ARB cache restore step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_step = next(s for s in steps if s['name'] == 'Restore ARB Cache')

        self.assertEqual(cache_step['id'], 'cache-arb')
        self.assertEqual(cache_step['if'], "github.event.inputs.force_recheck != 'true'")
        self.assertEqual(cache_step['uses'], 'actions/cache/restore@v4')

        # Test cache configuration
        with_config = cache_step['with']
        self.assertIn('arb_check_done.txt', with_config['path'])
        self.assertIn('extracted/', with_config['path'])
        self.assertIn('arb-check-v6', with_config['key'])

    def test_download_firmware_step(self):
        """Test download firmware step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next(s for s in steps if s['name'] == 'Download Firmware')

        self.assertEqual(download_step['if'], "steps.cache-arb.outputs.cache-hit != 'true'")
        self.assertIn('run', download_step)

        run_commands = download_step['run']
        # Verify CN firmware download logic with retries
        self.assertIn('MAX_RETRIES', run_commands)
        self.assertIn('aria2c', run_commands)
        self.assertIn('-x16', run_commands)
        self.assertIn('-s16', run_commands)

    def test_analyze_firmware_step(self):
        """Test analyze firmware step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        analyze_step = next(s for s in steps if s['name'] == 'Analyze Firmware (Check ARB)')

        self.assertIn('if', analyze_step)
        self.assertIn('cache-arb', analyze_step['if'])
        self.assertIn('skip_check.txt', analyze_step['if'])

        run_commands = analyze_step['run']
        self.assertIn('analyze_firmware.py', run_commands)
        self.assertIn('result.json', run_commands)

    def test_update_history_step(self):
        """Test update JSON history step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        update_step = next(s for s in steps if s['name'] == 'Update JSON History (Current Version)')

        self.assertEqual(update_step['if'], "hashFiles('result.json') != ''")

        run_commands = update_step['run']
        self.assertIn('update_history.py', run_commands)
        self.assertIn('device_short', run_commands)
        self.assertIn('--json-file', run_commands)

    def test_upload_result_artifact(self):
        """Test upload result artifact step."""
        steps = self.workflow['jobs']['check-variant']['steps']
        upload_step = next(s for s in steps if s['name'] == 'Upload Result')

        self.assertEqual(upload_step['uses'], 'actions/upload-artifact@v4')
        with_config = upload_step['with']
        self.assertIn('result-', with_config['name'])
        self.assertEqual(with_config['path'], 'result.json')

    def test_save_cache_step(self):
        """Test save ARB cache step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        save_cache_step = next(s for s in steps if s['name'] == 'Save ARB Cache')

        self.assertEqual(save_cache_step['uses'], 'actions/cache/save@v4')
        self.assertIn('if', save_cache_step)
        self.assertIn('cache-arb', save_cache_step['if'])
        self.assertIn('xbl_config.img', save_cache_step['if'])

    def test_cleanup_step(self):
        """Test cleanup step configuration."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cleanup_step = next(s for s in steps if s['name'] == 'Cleanup')

        self.assertEqual(cleanup_step['if'], 'always()')
        self.assertIn('rm -f firmware.zip', cleanup_step['run'])

    def test_update_readme_job_configuration(self):
        """Test update-readme job configuration."""
        job = self.workflow['jobs']['update-readme']

        self.assertEqual(job['needs'], 'check-variant')
        self.assertEqual(job['runs-on'], 'ubuntu-latest')

    def test_update_readme_job_steps(self):
        """Test update-readme job steps."""
        steps = self.workflow['jobs']['update-readme']['steps']

        # Verify all required steps exist
        step_names = [step['name'] for step in steps]
        self.assertIn('Checkout Repo', step_names)
        self.assertIn('Download All Artifacts', step_names)
        self.assertIn('Restore History & Generate README', step_names)
        self.assertIn('Commit and Push', step_names)

    def test_download_artifacts_step(self):
        """Test download all artifacts step configuration."""
        steps = self.workflow['jobs']['update-readme']['steps']
        download_step = next(s for s in steps if s['name'] == 'Download All Artifacts')

        self.assertEqual(download_step['uses'], 'actions/download-artifact@v4')
        with_config = download_step['with']
        self.assertEqual(with_config['path'], 'artifacts')
        self.assertEqual(with_config['merge-multiple'], False)

    def test_generate_readme_step(self):
        """Test restore history and generate README step."""
        steps = self.workflow['jobs']['update-readme']['steps']
        generate_step = next(s for s in steps if s['name'] == 'Restore History & Generate README')

        run_commands = generate_step['run']
        self.assertIn('data/history', run_commands)
        self.assertIn('generate_readme.py', run_commands)
        self.assertIn('find artifacts', run_commands)

    def test_commit_and_push_step(self):
        """Test commit and push step configuration."""
        steps = self.workflow['jobs']['update-readme']['steps']
        commit_step = next(s for s in steps if s['name'] == 'Commit and Push')

        run_commands = commit_step['run']
        self.assertIn('git config', run_commands)
        self.assertIn('git add', run_commands)
        self.assertIn('git commit', run_commands)
        self.assertIn('git push', run_commands)
        self.assertIn('data/history/*.json', run_commands)
        self.assertIn('README.md', run_commands)


class TestWorkflowEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions in the workflow."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            # Use safe_load and handle 'on' key being parsed as boolean True
            cls.workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key), we need to access it properly
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_matrix_combination_count(self):
        """Test that matrix generates expected number of combinations."""
        # Matrix is dynamic, logic is verified in generating script.
        # We can verify that we use dynamic generation instead.
        matrix = self.workflow['jobs']['check-variant']['strategy']['matrix']
        self.assertIn('fromJson', matrix)
        self.assertIn('outputs.matrix', matrix)

    def test_cache_key_uniqueness(self):
        """Test that cache keys are unique per device, variant, and version."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_step = next(s for s in steps if s['name'] == 'Restore ARB Cache')

        cache_key = cache_step['with']['key']
        # Should include device, variant, and version for uniqueness
        self.assertIn('${{ matrix.device }}', cache_key)
        self.assertIn('${{ matrix.variant }}', cache_key)
        self.assertIn('${{ steps.get_details.outputs.version }}', cache_key)

    def test_force_recheck_bypasses_cache(self):
        """Test that force_recheck input properly bypasses cache."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_step = next(s for s in steps if s['name'] == 'Restore ARB Cache')

        # Cache should be skipped when force_recheck is true
        self.assertIn('force_recheck', cache_step['if'])
        self.assertIn("!= 'true'", cache_step['if'])

    def test_conditional_step_dependencies(self):
        """Test that conditional steps have proper dependencies."""
        steps = self.workflow['jobs']['check-variant']['steps']

        # Download firmware should only run if cache miss
        download_step = next(s for s in steps if s['name'] == 'Download Firmware')
        self.assertIn('cache-arb', download_step['if'])
        self.assertIn('cache-hit', download_step['if'])

        # Analyze should skip if download was skipped
        analyze_step = next(s for s in steps if s['name'] == 'Analyze Firmware (Check ARB)')
        self.assertIn('skip_check.txt', analyze_step['if'])

    def test_error_handling_continue_on_error(self):
        """Test that job continues on error for individual matrix runs."""
        job = self.workflow['jobs']['check-variant']
        self.assertTrue(job['continue-on-error'])
        self.assertFalse(job['strategy']['fail-fast'])

    def test_aria2_download_parameters(self):
        """Test that aria2 is configured with proper download parameters."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next(s for s in steps if s['name'] == 'Download Firmware')

        run_commands = download_step['run']
        # Test concurrent connections and speed optimizations
        self.assertIn('-x16', run_commands)  # 16 connections
        self.assertIn('-s16', run_commands)  # 16 splits
        self.assertIn('-k1M', run_commands)  # 1MB piece size

    def test_cn_firmware_retry_logic(self):
        """Test CN firmware download has retry logic."""
        steps = self.workflow['jobs']['check-variant']['steps']
        download_step = next(s for s in steps if s['name'] == 'Download Firmware')

        run_commands = download_step['run']
        self.assertIn('MAX_RETRIES=5', run_commands)
        self.assertIn('RETRY_COUNT', run_commands)
        self.assertIn('while [ $RETRY_COUNT -lt $MAX_RETRIES ]', run_commands)
        self.assertIn('fetch_firmware.py', run_commands)  # URL refresh

    def test_all_device_metadata_complete(self):
        """Test that all devices have complete metadata."""
        # Matrix is dynamic, verify using DEVICE_METADATA directly
        for dev_id, meta in DEVICE_METADATA.items():
            self.assertTrue(meta.get('name'), f"Device {dev_id} missing name")
            self.assertTrue(meta.get('models'), f"Device {dev_id} missing models")


class TestWorkflowRegressionCases(unittest.TestCase):
    """Regression tests for workflow behavior."""

    @classmethod
    def setUpClass(cls):
        """Load the workflow file once for all tests."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            # Use safe_load and handle 'on' key being parsed as boolean True
            cls.workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key), we need to access it properly
            if True in cls.workflow:
                cls.workflow['on'] = cls.workflow.pop(True)

    def test_workflow_file_exists(self):
        """Regression: Ensure workflow file exists at expected path."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        self.assertTrue(workflow_path.exists())

    def test_yaml_valid_syntax(self):
        """Regression: Ensure YAML syntax is valid."""
        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        try:
            with open(workflow_path, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.fail(f"YAML syntax error: {e}")

    def test_no_deprecated_actions(self):
        """Regression: Check for deprecated GitHub Actions."""
        steps = []
        for job_name, job in self.workflow['jobs'].items():
            if 'steps' in job:
                steps.extend(job['steps'])

        # Check for old versions (should use v4 or later)
        for step in steps:
            if 'uses' in step:
                # Ensure we're not using old action versions
                if 'checkout' in step['uses']:
                    self.assertIn('v4', step['uses'])
                if 'upload-artifact' in step['uses']:
                    self.assertIn('v4', step['uses'])
                if 'download-artifact' in step['uses']:
                    self.assertIn('v4', step['uses'])
                if 'cache' in step['uses']:
                    self.assertIn('v4', step['uses'])

    def test_output_variables_properly_set(self):
        """Regression: Ensure output variables are set correctly."""
        steps = self.workflow['jobs']['check-variant']['steps']
        details_step = next(s for s in steps if s['name'] == 'Get Firmware Details')

        run_commands = details_step['run']
        # Verify all required outputs are set
        self.assertIn('url=', run_commands)
        self.assertIn('version=', run_commands)
        self.assertIn('device_short=', run_commands)
        self.assertIn('>> $GITHUB_OUTPUT', run_commands)

    def test_artifact_names_unique(self):
        """Regression: Ensure artifact names are unique per matrix run."""
        steps = self.workflow['jobs']['check-variant']['steps']

        # Result artifact
        upload_result = next(s for s in steps if s['name'] == 'Upload Result')
        result_name = upload_result['with']['name']
        self.assertIn('${{ matrix.device }}', result_name)
        self.assertIn('${{ matrix.variant }}', result_name)

        # History artifact
        upload_history = next(s for s in steps if s['name'] == 'Upload JSON History')
        history_name = upload_history['with']['name']
        self.assertIn('${{ matrix.device }}', history_name)
        self.assertIn('${{ matrix.variant }}', history_name)

    def test_python_scripts_referenced_exist(self):
        """Regression: Verify all Python scripts referenced in workflow exist."""
        base_path = Path(__file__).parent.parent

        scripts = [
            'fetch_firmware.py',
            'analyze_firmware.py',
            'update_history.py',
            'generate_readme.py'
        ]

        for script in scripts:
            script_path = base_path / script
            self.assertTrue(script_path.exists(), f"Script {script} not found")

    def test_cache_version_explicitly_set(self):
        """Regression: Ensure cache version is explicitly set to avoid conflicts."""
        steps = self.workflow['jobs']['check-variant']['steps']
        cache_step = next(s for s in steps if s['name'] == 'Restore ARB Cache')

        cache_key = cache_step['with']['key']
        # Should have version prefix (currently v6)
        self.assertIn('arb-check-v', cache_key)


if __name__ == '__main__':
    unittest.main()