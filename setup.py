from setuptools import setup
import os, sys

if os.geteuid() != 0:
    sys.exit("ERROR: You must run this installer as root (use sudo).")

setup(
    name="runbook",
    version="0.0.1",
    py_modules=["runbook"],
    entry_points={
        "console_scripts": [
            "runbook=runbook:main",
        ],
    },
    author="Your Name",
    description="Minimal Python-based runbook executor",
    python_requires=">=3.8",
)
