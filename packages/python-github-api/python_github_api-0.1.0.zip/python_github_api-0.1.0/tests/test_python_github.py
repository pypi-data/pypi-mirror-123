#!/usr/bin/env python

"""Tests for `python_github` package."""


import unittest

from python_github.python_github import Github


class TestPython_github(unittest.TestCase):
    """Tests for `python_github` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.github = Github()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_pull_request(self):
        """Test something."""
        self.github.pull_request.get("OUXT-Polaris/dynamixel_hardware_interface", state="closed")
        self.github.pull_request.get("OUXT-Polaris/dynamixel_hardware_interface", state="open")

    def test_get_workflow(self):
        self.github.workflow.get("OUXT-Polaris/dynamixel_hardware_interface")

    def test_licence(self):
        self.assertEqual(self.github.license.get("OUXT-Polaris/dynamixel_hardware_interface"), "Apache License 2.0")
        self.assertEqual(self.github.license.get("OUXT-Polaris/ouxt_common"), None)
    
    def test_issue(self):
        self.github.issue.get("OUXT-Polaris/ouxt_automation")

if __name__ == "__main__":
    unittest.main()