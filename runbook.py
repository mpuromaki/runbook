#!/usr/bin/env python3
"""
runbook — Minimal Python-based runbook executor

Usage:
  sudo runbook <file>
"""

import os
import sys
import subprocess
import runpy
import builtins
from pathlib import Path


# ----------------------------
# Global state
# ----------------------------

_current_step = 0

# ----------------------------
# Helper functions
# ----------------------------

def step(name: str):
    """
    Keep track of different steps of the runbook.
    
    Returns:
      - True, if the step should be executed.
      - False, if the step should be skipped.
    """

    global _current_step
    _current_step += 1
    print(f"\nRUNBOOK - STEP {_current_step}: {name}")

    return True

def shell(cmd: str):
    """
    Execute a shell command as root.
    """

    print("$ "+cmd, flush=True)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    stdout, stderr = result.stdout, result.stderr

    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def _require_root():
    """
    Ensure the script runs as root.
    """

    if os.geteuid() != 0:
        print("ERROR: This command must be run as root (use sudo).")
        sys.exit(1)

def _setup_environment():
    """
    Inject Runbook helpers into the global scope.
    This allows the runbook scripts to stay clean and lean.
    """
    builtins.step = step
    builtins.shell = shell


# ----------------------------
# Main
# ----------------------------

def main():
    # Handle arguments
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    runbook_path = Path(sys.argv[1])
    if not runbook_path.exists():
        print(f"ERROR: Runbook not found: {runbook_path}")
        sys.exit(1)

    # Set up execution environment
    _require_root()
    _setup_environment()

    # Execute the runbook
    print(f"RUNBOOK - EXECUTE: {runbook_path}")
    try:
        runpy.run_path(runbook_path, run_name="__main__")
    except KeyboardInterrupt:
        print("\nERROR: Interrupted by user")
        sys.exit(130)

    # Done
    print(f"\nRUNBOOK - COMPLETE")


# ----------------------------
# Entrypoint
# ----------------------------

if __name__ == "__main__":
    main()
