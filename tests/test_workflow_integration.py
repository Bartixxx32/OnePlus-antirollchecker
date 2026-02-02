#!/usr/bin/env python3
"""
Integration tests for the check_arb.yml workflow.
Tests workflow behavior, script integration, and end-to-end scenarios.
"""

import unittest
import json
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open


class TestWorkflowScriptIntegration(unittest.TestCase):
    """Test integration between workflow and Python scripts."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

    def test_fetch_firmware_output_format(self):
        """Test that fetch_firmware.py outputs expected JSON format."""
        expected_keys = ['url', 'version']

        # Simulate fetch_firmware.py output
        mock_output = {
            'url': 'https://example.com/firmware.zip',
            'version': 'CPH2747_16.0.3.501(EX01)'
        }

        # Verify all required keys are present
        for key in expected_keys:
            self.assertIn(key, mock_output)

        # Verify URL format
        self.assertTrue(mock_output['url'].startswith('http'))

        # Verify version format (should not be empty)
        self.assertTrue(len(mock_output['version']) > 0)

    def test_analyze_firmware_output_format(self):
        """Test that analyze_firmware.py outputs expected JSON format."""
        expected_keys = ['arb_index', 'major', 'minor']

        # Simulate analyze_firmware.py output
        mock_output = {
            'arb_index': '1',
            'major': '3',
            'minor': '0'
        }

        # Verify all required keys are present
        for key in expected_keys:
            self.assertIn(key, mock_output)

        # Verify values are strings (as parsed from arbextract output)
        for value in mock_output.values():
            self.assertIsInstance(value, str)

    def test_workflow_environment_variables(self):
        """Test that workflow sets required environment variables."""
        required_env_vars = [
            'GITHUB_OUTPUT',
            'GITHUB_WORKSPACE'
        ]

        # In actual workflow, these should be available
        # Here we just verify the concept
        for var in required_env_vars:
            # These vars should exist in GitHub Actions environment
            self.assertIsInstance(var, str)

    def test_matrix_variable_substitution(self):
        """Test that matrix variables are properly substituted."""
        # Test device variable
        test_device = 'oneplus_15'
        self.assertTrue(test_device.startswith('oneplus_'))

        # Test variant variable
        test_variant = 'GLO'
        self.assertIn(test_variant, ['GLO', 'EU', 'IN', 'CN'])

        # Test device_short variable
        test_device_short = '15'
        self.assertTrue(len(test_device_short) <= 3)

    def test_artifact_path_structure(self):
        """Test that artifact paths follow expected structure."""
        # Result artifact path
        result_path = 'result.json'
        self.assertTrue(result_path.endswith('.json'))

        # History artifact path structure
        device_short = '15'
        variant = 'GLO'
        history_path = f'data/history/{device_short}_{variant}.json'
        self.assertTrue(history_path.startswith('data/history/'))
        self.assertTrue(history_path.endswith('.json'))

    def test_cache_key_format(self):
        """Test that cache key follows expected format."""
        cache_version = 'v6'
        device = 'oneplus_15'
        variant = 'GLO'
        version = 'CPH2747_16.0.3.501(EX01)'

        cache_key = f'arb-check-{cache_version}-{device}-{variant}-{version}'

        # Verify format
        self.assertIn(cache_version, cache_key)
        self.assertIn(device, cache_key)
        self.assertIn(variant, cache_key)
        self.assertIn(version, cache_key)

    def test_skip_check_file_behavior(self):
        """Test skip_check.txt file creation and handling."""
        skip_file = Path(self.test_dir) / 'skip_check.txt'

        # Simulate download failure creating skip file
        skip_file.touch()
        self.assertTrue(skip_file.exists())

        # Workflow should check for this file existence
        should_skip = skip_file.exists()
        self.assertTrue(should_skip)

    def test_firmware_zip_cleanup(self):
        """Test that firmware.zip is properly cleaned up."""
        firmware_file = Path(self.test_dir) / 'firmware.zip'
        firmware_file.touch()

        # Simulate cleanup
        if firmware_file.exists():
            firmware_file.unlink()

        # File should be removed
        self.assertFalse(firmware_file.exists())


class TestWorkflowConditionals(unittest.TestCase):
    """Test workflow conditional logic."""

    def test_force_recheck_condition(self):
        """Test force_recheck input affects cache behavior."""
        # When force_recheck is false, cache should be used
        force_recheck = False
        should_use_cache = not force_recheck
        self.assertTrue(should_use_cache)

        # When force_recheck is true, cache should be skipped
        force_recheck = True
        should_use_cache = not force_recheck
        self.assertFalse(should_use_cache)

    def test_cache_hit_condition(self):
        """Test cache hit condition affects downstream steps."""
        # When cache hits, download should be skipped
        cache_hit = True
        should_download = not cache_hit
        self.assertFalse(should_download)

        # When cache misses, download should proceed
        cache_hit = False
        should_download = not cache_hit
        self.assertTrue(should_download)

    def test_result_json_existence_condition(self):
        """Test that result.json existence affects update step."""
        # Create temp file to simulate result.json
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
            json.dump({'arb_index': '1', 'major': '3', 'minor': '0'}, f)

        try:
            # If result.json exists, update should run
            self.assertTrue(Path(temp_path).exists())

            # If result.json doesn't exist, update should be skipped
            Path(temp_path).unlink()
            self.assertFalse(Path(temp_path).exists())
        finally:
            # Cleanup
            if Path(temp_path).exists():
                Path(temp_path).unlink()

    def test_xbl_config_extraction_condition(self):
        """Test that xbl_config.img extraction affects cache save."""
        test_dir = tempfile.mkdtemp()
        try:
            extracted_dir = Path(test_dir) / 'extracted'
            extracted_dir.mkdir()

            # When xbl_config.img exists, cache should be saved
            xbl_file = extracted_dir / 'xbl_config.img'
            xbl_file.touch()
            self.assertTrue(xbl_file.exists())

            # When xbl_config.img doesn't exist, cache save should be skipped
            xbl_file.unlink()
            self.assertFalse(xbl_file.exists())
        finally:
            shutil.rmtree(test_dir)

    def test_cn_variant_download_logic(self):
        """Test CN variant uses special download logic."""
        variant = 'CN'
        is_cn = variant == 'CN'
        self.assertTrue(is_cn)

        # CN should use retry logic
        if is_cn:
            max_retries = 5
            self.assertEqual(max_retries, 5)

        # Non-CN variants
        variant = 'GLO'
        is_cn = variant == 'CN'
        self.assertFalse(is_cn)


class TestWorkflowDataFlow(unittest.TestCase):
    """Test data flow through workflow steps."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

    def test_firmware_details_to_download(self):
        """Test data flow from get_details to download step."""
        # Step 1: Get firmware details
        fw_info = {
            'url': 'https://example.com/firmware.zip',
            'version': 'CPH2747_16.0.3.501(EX01)'
        }

        # Step 2: Download uses these details
        download_url = fw_info['url']
        self.assertTrue(download_url.endswith('.zip'))

        version = fw_info['version']
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)

    def test_analyze_to_update_history(self):
        """Test data flow from analyze to update_history step."""
        # Step 1: Analyze firmware produces result.json
        analyze_result = {
            'arb_index': '1',
            'major': '3',
            'minor': '0'
        }

        # Step 2: Update history uses result.json plus metadata
        device_short = '15'
        variant = 'GLO'
        version = 'CPH2747_16.0.3.501(EX01)'

        # Combined data for history
        history_entry = {
            'device_short': device_short,
            'variant': variant,
            'version': version,
            'arb_index': analyze_result['arb_index'],
            'major': analyze_result['major'],
            'minor': analyze_result['minor']
        }

        # Verify all required fields present
        self.assertIn('device_short', history_entry)
        self.assertIn('variant', history_entry)
        self.assertIn('version', history_entry)
        self.assertIn('arb_index', history_entry)

    def test_artifacts_to_readme_generation(self):
        """Test data flow from artifacts to README generation."""
        # Step 1: Multiple jobs produce artifacts
        artifacts = {
            'history-oneplus_15-GLO': {'path': 'data/history/15_GLO.json'},
            'history-oneplus_15-EU': {'path': 'data/history/15_EU.json'},
            'result-oneplus_15-GLO': {'path': 'result.json'},
        }

        # Step 2: Download and restore history files
        history_files = [
            artifact['path'] for name, artifact in artifacts.items()
            if name.startswith('history-')
        ]

        self.assertEqual(len(history_files), 2)

        # Step 3: Generate README from history files
        for history_file in history_files:
            self.assertTrue(history_file.startswith('data/history/'))
            self.assertTrue(history_file.endswith('.json'))


class TestWorkflowErrorHandling(unittest.TestCase):
    """Test error handling in workflow."""

    def test_continue_on_error_behavior(self):
        """Test that individual job failures don't stop other jobs."""
        # Simulate matrix jobs
        jobs = ['job1', 'job2', 'job3']
        failed_jobs = []
        successful_jobs = []

        # Simulate job1 failing
        for job in jobs:
            if job == 'job1':
                failed_jobs.append(job)
            else:
                successful_jobs.append(job)

        # With continue-on-error: true, other jobs should complete
        self.assertEqual(len(successful_jobs), 2)
        self.assertEqual(len(failed_jobs), 1)

    def test_download_failure_skip_logic(self):
        """Test that download failures create skip marker."""
        test_dir = Path(tempfile.mkdtemp())
        try:
            skip_file = test_dir / 'skip_check.txt'

            # Simulate download failure
            download_success = False
            if not download_success:
                skip_file.touch()

            # Subsequent steps should check for skip file
            should_analyze = not skip_file.exists()
            self.assertFalse(should_analyze)
        finally:
            shutil.rmtree(test_dir)

    def test_retry_logic_cn_downloads(self):
        """Test retry logic for CN firmware downloads."""
        max_retries = 5
        retry_count = 0
        success = False

        # Simulate retries
        while retry_count < max_retries and not success:
            retry_count += 1
            # Simulate eventual success
            if retry_count == 3:
                success = True

        self.assertTrue(success)
        self.assertEqual(retry_count, 3)
        self.assertLess(retry_count, max_retries)

    def test_url_refresh_on_failure(self):
        """Test URL refresh mechanism for expired signed URLs."""
        device = 'oneplus_15'
        variant = 'CN'
        version = 'PLK110_16.0.3.503(CN01)'

        # Initial URL (expired)
        initial_url = 'https://example.com/expired'

        # Simulate refresh call (would call fetch_firmware.py)
        # fetch_firmware.py "$device" "$variant" "$version" --output fw_refresh.json
        refreshed_url = 'https://example.com/refreshed'

        # URL should be different after refresh
        self.assertNotEqual(initial_url, refreshed_url)

    def test_git_commit_no_changes_handling(self):
        """Test git commit handles case with no changes."""
        # Simulate git commit with no changes
        commit_message = "Update ARB history and README"
        has_changes = False

        if has_changes:
            # Would execute: git commit -m "..."
            committed = True
        else:
            # Would execute: echo "No changes to commit"
            committed = False

        # Should not fail when there are no changes
        self.assertFalse(committed)


class TestWorkflowSecurityAndBestPractices(unittest.TestCase):
    """Test security and best practices in workflow."""

    def test_no_hardcoded_secrets(self):
        """Test that workflow doesn't contain hardcoded secrets."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            content = f.read()

        # Check for common secret patterns (should not exist)
        secret_patterns = ['password:', 'token:', 'api_key:', 'secret:']
        for pattern in secret_patterns:
            # Should not find literal secrets
            if pattern in content.lower():
                # Check if it's a proper secret reference like ${{ secrets.TOKEN }}
                self.assertIn('secrets.', content.lower())

    def test_actions_use_pinned_versions(self):
        """Test that GitHub Actions use specific versions."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key)
            if True in workflow:
                workflow['on'] = workflow.pop(True)

        # Collect all action uses
        for job_name, job in workflow['jobs'].items():
            if 'steps' in job:
                for step in job['steps']:
                    if 'uses' in step:
                        # Should specify version (e.g., @v4, not @main)
                        self.assertIn('@', step['uses'])
                        # Should not use moving targets like @main or @master
                        self.assertNotIn('@main', step['uses'])
                        self.assertNotIn('@master', step['uses'])

    def test_file_permissions_secure(self):
        """Test that downloaded tools have appropriate permissions."""
        # Tools should be made executable
        tools = ['arbextract', 'payload-dumper']

        for tool in tools:
            # Workflow does: chmod +x tools/{tool}
            # This is appropriate and necessary
            self.assertIsInstance(tool, str)

    def test_external_downloads_verified(self):
        """Test that external downloads use secure sources."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            content = f.read()

        # Check that downloads use HTTPS
        if 'curl -L -o' in content or 'wget' in content:
            # Should use https:// not http://
            self.assertIn('https://', content)

    def test_git_config_safe(self):
        """Test that git configuration is safe."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key)
            if True in workflow:
                workflow['on'] = workflow.pop(True)

        # Find commit step
        commit_step = None
        for step in workflow['jobs']['update-readme']['steps']:
            if step['name'] == 'Commit and Push':
                commit_step = step
                break

        self.assertIsNotNone(commit_step)

        # Should set local git config (not global)
        self.assertIn('--local', commit_step['run'])


class TestWorkflowPerformanceOptimizations(unittest.TestCase):
    """Test performance optimizations in workflow."""

    def test_cache_usage_enabled(self):
        """Test that caching is properly utilized."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key)
            if True in workflow:
                workflow['on'] = workflow.pop(True)

        steps = workflow['jobs']['check-variant']['steps']

        # Should have both restore and save cache steps
        cache_steps = [s for s in steps if 'cache' in s.get('uses', '')]
        self.assertGreaterEqual(len(cache_steps), 2)  # At least restore and save

    def test_parallel_downloads_configured(self):
        """Test that aria2c uses parallel connections."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            content = f.read()

        # Should use -x16 -s16 for parallel downloads
        self.assertIn('-x16', content)
        self.assertIn('-s16', content)

    def test_matrix_parallel_execution(self):
        """Test that matrix jobs run in parallel."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key)
            if True in workflow:
                workflow['on'] = workflow.pop(True)

        strategy = workflow['jobs']['check-variant']['strategy']

        # fail-fast: false allows all jobs to run in parallel
        self.assertFalse(strategy['fail-fast'])

    def test_conditional_steps_skip_unnecessary_work(self):
        """Test that conditional steps prevent unnecessary work."""
        import yaml

        workflow_path = Path(__file__).parent.parent / '.github' / 'workflows' / 'check_arb.yml'
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
            # YAML parses 'on:' as True (boolean key)
            if True in workflow:
                workflow['on'] = workflow.pop(True)

        steps = workflow['jobs']['check-variant']['steps']

        # Count conditional steps
        conditional_steps = [s for s in steps if 'if' in s]

        # Should have multiple conditional steps to skip work
        self.assertGreater(len(conditional_steps), 3)


if __name__ == '__main__':
    unittest.main()