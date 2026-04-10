#!/usr/bin/env python3
"""
Test runner script for media acquisition system.
Provides convenient commands for running different test suites.

Usage:
    python scripts/run_tests.py              # Run all tests
    python scripts/run_tests.py unit         # Run unit tests only
    python scripts/run_tests.py integration  # Run integration tests
    python scripts/run_tests.py coverage     # Run with coverage report
    python scripts/run_tests.py ci           # Run CI test suite
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Test configuration
TEST_DIR = Path(__file__).parent.parent / "tests"
UNIT_TEST_DIR = TEST_DIR / "unit"
INTEGRATION_TEST_DIR = TEST_DIR / "integration"


def run_command(cmd: list, description: str) -> int:
    """Run a command and return exit code."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"{'=' * 60}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent.parent,
            check=False
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Test run interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1


def run_all_tests():
    """Run all tests."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(TEST_DIR),
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "All Tests")


def run_unit_tests():
    """Run unit tests only."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(UNIT_TEST_DIR),
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(INTEGRATION_TEST_DIR),
        "-v",
        "--tb=short",
        "-m", "integration"
    ]
    return run_command(cmd, "Integration Tests")


def run_coverage():
    """Run tests with coverage report."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(TEST_DIR),
        "-v",
        "--tb=short",
        "--cov=media_acquisition",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]
    code = run_command(cmd, "Tests with Coverage")
    
    if code == 0:
        print(f"\n✅ Coverage report generated: htmlcov/index.html")
    
    return code


def run_ci_suite():
    """Run CI test suite (what runs in GitHub Actions)."""
    # First run unit tests
    code = run_unit_tests()
    if code != 0:
        return code
    
    # Then run integration tests
    code = run_integration_tests()
    if code != 0:
        return code
    
    # Finally run coverage
    return run_coverage()


def setup_test_environment():
    """Setup test environment."""
    print("Setting up test environment...")
    
    # Check if pytest is installed
    try:
        import pytest
        print(f"✓ pytest {pytest.__version__} installed")
    except ImportError:
        print("❌ pytest not installed. Installing test dependencies...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"]
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        if result.returncode != 0:
            return False
    
    # Setup test database
    setup_script = Path(__file__).parent / "setup_test_db.py"
    if setup_script.exists():
        print("✓ Running test database setup...")
        result = subprocess.run([sys.executable, str(setup_script)])
        if result.returncode != 0:
            print("⚠️  Test database setup failed, continuing anyway...")
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run media acquisition tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              Run all tests
  %(prog)s unit         Run unit tests only
  %(prog)s integration  Run integration tests
  %(prog)s coverage     Run with coverage report
  %(prog)s ci           Run CI test suite
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "coverage", "ci"],
        help="Test command to run (default: all)"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup test environment before running tests"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Setup if requested
    if args.setup:
        if not setup_test_environment():
            return 1
    
    # Run requested tests
    if args.command == "all":
        code = run_all_tests()
    elif args.command == "unit":
        code = run_unit_tests()
    elif args.command == "integration":
        code = run_integration_tests()
    elif args.command == "coverage":
        code = run_coverage()
    elif args.command == "ci":
        code = run_ci_suite()
    else:
        code = run_all_tests()
    
    # Summary
    print(f"\n{'=' * 60}")
    if code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code {code}")
    print(f"{'=' * 60}\n")
    
    return code


if __name__ == "__main__":
    sys.exit(main())
