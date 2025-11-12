"""
Runbook for Hello World

Prints out "Hello" and "World" to the console.
Used for testing the Runbook framework.

Usage:
  sudo runbook <file>
"""

step("Hello")
shell("echo 'Hello'")

step("World")
shell("echo 'World'")
