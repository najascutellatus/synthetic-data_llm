#!/usr/bin/env python

"""Tests for `synthetic_data_llm` package."""


import unittest
from click.testing import CliRunner

from synthetic_data_llm import synthetic_data_llm
from synthetic_data_llm import cli


class TestSynthetic_data_llm(unittest.TestCase):
    """Tests for `synthetic_data_llm` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'synthetic_data_llm.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
