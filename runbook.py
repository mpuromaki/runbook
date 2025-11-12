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
import datetime
from pathlib import Path


# ----------------------------
# Global state
# ----------------------------

_current_step = 0


# UI stuff

_h1 = 70
_h2 = 65

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

    print(f">> STEP {_current_step}: {name}")
    print(f"-" * _h2)

    return True

def shell(cmd: str):
    """
    Execute a shell command as root.
    """

    print("$ "+cmd)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    stdout, stderr = result.stdout, result.stderr

    if stdout:
        for row in stdout.splitlines():
            print(row)
    if stderr:
        print(stderr, file=sys.stderr)

    if result.returncode != 0:
        error(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    else:
        success()

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

def error(message: str = None):
    """
    Print an error message.
    """
    if message:
        print(f"❌ ERROR ({message.capitalize()})")
    else:
        print(f"❌ ERROR")
    print(flush=True)

def success(message: str = None):
    """
    Print an success message.
    """
    if message:
        print(f"✅ SUCCESS ({message.capitalize()})")
    else:
        print(f"✅ SUCCESS")
    print(flush=True)

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
        error(f"Runbook not found: {runbook_path}")
        sys.exit(1)

    # Set up execution environment
    _require_root()
    _setup_environment()

    # Execute the runbook
    print(f"=" * _h1)
    print(f"RUNBOOK - {runbook_path}")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"=" * _h1)
    print()

    try:
        runpy.run_path(runbook_path, run_name="__main__")
    except KeyboardInterrupt:
        print()
        error("Interrupted by user")
        sys.exit(2)

    # Done
    print(f"=" * _h1)
    print(f"RUNBOOK COMPLETE")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Steps: {_current_step}")
    print(f"=" * _h1)


# ----------------------------
# Entrypoint
# ----------------------------

if __name__ == "__main__":
    main()
