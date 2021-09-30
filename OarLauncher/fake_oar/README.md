# Simulating oarsub to debug

```bash
sudo nano /usr/local/bin/oarsub
sudo chmod +x /usr/local/bin/oarsub
sudo ln -s /usr/local/bin/oarsub /usr/local/bin/oarctl
```

In `/usr/local/bin/oarsub`:
```bash
#!/bin/bash

source <path-to>/venv/bin/activate

python <path-to>/OarLauncher/fake_oar/oarsub.py "$@"
```