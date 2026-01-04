This is **ArchitectAI**.

Since you have decided to proceed as **root**, I have modified the setup scripts to remove `sudo` usage, eliminate dependencies on the `ubuntu` user, and ensure permissions align with the root account.

### **1. Initial Server Setup**

```bash
# Install dependencies
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git build-essential nginx

# Setup app directory (Owned by root)
cd /opt
git clone https://github.com/y3fai/jassas.git
cd jassas

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### **2. Bootstrap Data**

```bash
# Initialize and seed data
./jassas init
./jassas seed "https://my.gov.sa"

# Crawl (Adjust pages as needed)
./jassas crawl --max-pages 500

# Process data
./jassas clean
./jassas tokenize
./jassas build-index

```

### **3. Production Service**

Create service file:

```bash
nano /etc/systemd/system/jassas.service

```

Service configuration:

```ini
[Unit]
Description=Jassas Search API
After=network.target

[Service]
# Security Warning: Running as root grants full system access if compromised.
User=root
WorkingDirectory=/opt/jassas
Environment="PATH=/opt/jassas/venv/bin"
ExecStart=/opt/jassas/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target

```

Start service:

```bash
systemctl daemon-reload
systemctl start jassas
systemctl enable jassas
systemctl status jassas

```

### **4. Continuous Deployment**

Generate SSH key (stored in `/root/.ssh/`):

```bash
ssh-keygen -t ed25519 -C "github-action" -f ~/.ssh/jassas_deploy

```

Add public key to VPS:

```bash
nano ~/.ssh/authorized_keys
# Paste the content of jassas_deploy.pub here

```

Add GitHub secrets:

-   `HOST`: VPS IP address
-   `USERNAME`: **root**
-   `KEY`: Private key content (from `jassas_deploy`)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to VPS

on:
    push:
        branches: ["main"]

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - name: Deploy via SSH
              uses: appleboy/ssh-action@master
              with:
                  host: ${{ secrets.HOST }}
                  username: ${{ secrets.USERNAME }}
                  key: ${{ secrets.KEY }}
                  script: |
                      cd /opt/jassas
                      git pull origin main
                      source venv/bin/activate
                      pip install -r requirements.txt
                      systemctl restart jassas
```
