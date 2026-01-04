### **1. Initial Server Setup**

```bash
# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git build-essential nginx

# Setup app directory
sudo chown ubuntu:ubuntu /opt
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
./jassas init
./jassas seed "https://my.gov.sa"
./jassas crawl --max-pages 500
./jassas clean
./jassas tokenize
./jassas build-index
```

### **3. Production Service**

Create service file:

```bash
sudo nano /etc/systemd/system/jassas.service
```

Service configuration:

```ini
[Unit]
Description=Jassas Search API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/jassas
Environment="PATH=/opt/jassas/venv/bin"
ExecStart=/opt/jassas/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl daemon-reload
sudo systemctl start jassas
sudo systemctl enable jassas
sudo systemctl status jassas
```

### **4. Continuous Deployment**

Generate SSH key:

```bash
ssh-keygen -t ed25519 -C "github-action" -f ~/.ssh/jassas_deploy
```

Add public key to VPS:

```bash
nano ~/.ssh/authorized_keys
# Paste the public key content
```

Add GitHub secrets:

-   `HOST`: VPS IP address
-   `USERNAME`: VPS username
-   `KEY`: Private key content

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
                      sudo systemctl restart jassas
```
