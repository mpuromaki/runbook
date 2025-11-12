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
_completed_count = 0
_skipped_count = 0
_failed_count = 0

# UI stuff

_h1 = 70
_h2 = 65

# ----------------------------
# Helper functions
# ----------------------------

def step(name: str):
    """
    Keep track of different steps of the runbook.
    """

    global _current_step
    _current_step += 1

    print(f">> STEP {_current_step}: {name}")

def shell(cmd: str):
    """
    Execute a shell command as root.
    """

    print(f"-" * _h2)
    print("$ "+cmd)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    stdout, stderr = result.stdout, result.stderr

    if stdout:
        for row in stdout.splitlines():
            print(row)
    if stderr:
        print(stderr, file=sys.stderr)

    print(f"-" * _h2)

    if result.returncode != 0:
        global _failed_count
        _failed_count += 1
        error(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    else:
        global _completed_count
        _completed_count += 1
        success()

def manual(instruction: str):
    """
    Print instructions for manual step. Wait for confirmation.
    """

    print(f"-" * _h2)
    print("✨ MANUAL TASK")
    print(instruction)
    print(f"-" * _h2)

    global _completed_count
    global _skipped_count
    global _failed_count

    while True:
        choice = input("[c]ontinue or [s]kip or [a]bort: ")
        if choice in ("", "c", "continue"):
            _completed_count += 1
            success()
            return
        elif choice in ["s", "skip"]:
            _skipped_count += 1
            print("❎ SKIPPED BY USER")
            print(flush=True)
            return
        elif choice in ["a", "abort"]:
            _failed_count += 1
            error("ABORTED BY USER")
            sys.exit(1)
        else:
            print("[c]ontinue or [s]kip or [a]bort: ")

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
    builtins.manual = manual

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
    print(f"Success: {_completed_count}, Skipped: {_skipped_count}, Failed: {_failed_count}")
    print(f"=" * _h1)


# ----------------------------
# Entrypoint
# ----------------------------

if __name__ == "__main__":
    main()
