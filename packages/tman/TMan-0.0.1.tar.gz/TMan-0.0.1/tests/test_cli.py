#!/usr/bin/env python
"""Tests for the command-line interface."""

#  Copyright (c) 2021, Daniel Mouritzen.

from click.testing import CliRunner

from tman import cli


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "TMan" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
