"""
Runbook for updating Runbook

Fetches latest version from Github and upgrades to it.
"""

step("Fetch latest Runbook version")
shell("git pull origin main")

step("Upgrade Runbook")
shell("pipx install --force --global .")
