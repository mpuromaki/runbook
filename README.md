# runbook
Simple python based runbook automation.

:warning: Atleast for now, this runbook automation is meant for lightweight system administration.
This means that he user of this system is expected to run everything as root, so that the runbooks
actually have permission to do their work. This likely will be improved down the line.
But for now, root.

You can test the runbook system with included hello_world.py script.

```
sudo runbook hello_world.py
```

## Installing Runbook

1. Clone this project

```
sudo git clone https://github.com/mpuromaki/runbook.git
```

Root user often does not have git set up, and SSH remotes need that even for public repositories.
So use the HTTPS repository to make life easier.

2. Install runbook

```
cd runbook
sudo pip install .
```

## Updating Runbook

1. Run the included update runbook

```
cd runbook
sudo runbook update.py
```