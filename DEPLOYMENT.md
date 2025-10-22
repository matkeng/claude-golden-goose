# Deployment Guide

This guide covers deploying Claude Golden Goose to production.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- PostgreSQL 12+
- Redis 5+
- Nginx (recommended)
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)

## Step 1: Server Setup

### Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Redis
sudo apt install -y redis-server

# Install Nginx
sudo apt install -y nginx

# Install system tools
sudo apt install -y git supervisor
```

## Step 2: Database Setup

```bash
# Create database and user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE claude_goose_db;
CREATE USER claude_goose_user WITH PASSWORD 'secure_password';
ALTER ROLE claude_goose_user SET client_encoding TO 'utf8';
ALTER ROLE claude_goose_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE claude_goose_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE claude_goose_db TO claude_goose_user;
\q
```

## Step 3: Application Deployment

```bash
# Create application directory
sudo mkdir -p /opt/claude-goose
sudo chown $USER:$USER /opt/claude-goose
cd /opt/claude-goose

# Clone repository
git clone https://github.com/matkeng/claude-golden-goose.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # WSGI server
```

## Step 4: Configure Environment

```bash
# Copy production environment template
cp .env.production.example .env

# Edit .env with your production settings
nano .env
```

**Important**: Update these values:
- `SECRET_KEY`: Generate a new one (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `ALLOWED_HOSTS`: Your domain name
- `DATABASE_URL`: PostgreSQL connection string
- API keys for Gemini and Claude
- Tailscale settings if using

## Step 5: Collect Static Files

```bash
# Create directories
sudo mkdir -p /var/www/claude-goose/static
sudo mkdir -p /var/www/claude-goose/media
sudo chown -R $USER:$USER /var/www/claude-goose

# Collect static files
python manage.py collectstatic --no-input
```

## Step 6: Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Step 7: Configure Gunicorn

Create `/opt/claude-goose/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5
errorlog = "/opt/claude-goose/logs/gunicorn-error.log"
accesslog = "/opt/claude-goose/logs/gunicorn-access.log"
loglevel = "info"
```

## Step 8: Configure Supervisor

Create `/etc/supervisor/conf.d/claude-goose.conf`:

```ini
[program:claude-goose]
directory=/opt/claude-goose
command=/opt/claude-goose/venv/bin/gunicorn claude_goose.wsgi:application -c /opt/claude-goose/gunicorn_config.py
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/claude-goose/logs/supervisor.log

[program:claude-goose-celery]
directory=/opt/claude-goose
command=/opt/claude-goose/venv/bin/celery -A claude_goose worker --loglevel=info
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/claude-goose/logs/celery.log
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start claude-goose
sudo supervisorctl start claude-goose-celery
```

## Step 9: Configure Nginx

Create `/etc/nginx/sites-available/claude-goose`:

```nginx
upstream claude_goose {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 100M;
    
    location /static/ {
        alias /var/www/claude-goose/static/;
        expires 30d;
    }
    
    location /media/ {
        alias /var/www/claude-goose/media/;
        expires 30d;
    }
    
    location / {
        proxy_pass http://claude_goose;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/claude-goose /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 10: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

## Step 11: Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Step 12: Tailscale Setup (Optional)

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to your tailnet
sudo tailscale up --authkey=<your-auth-key>
```

## Monitoring and Maintenance

### View Logs

```bash
# Gunicorn logs
tail -f /opt/claude-goose/logs/gunicorn-error.log

# Celery logs
tail -f /opt/claude-goose/logs/celery.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Restart application
sudo supervisorctl restart claude-goose
sudo supervisorctl restart claude-goose-celery

# Restart Nginx
sudo systemctl restart nginx
```

### Update Application

```bash
cd /opt/claude-goose
source venv/bin/activate

# Pull latest changes
git pull

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Restart services
sudo supervisorctl restart claude-goose
sudo supervisorctl restart claude-goose-celery
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS correctly
- [ ] Use HTTPS (SSL/TLS)
- [ ] Enable security headers
- [ ] Configure firewall
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity
- [ ] Use strong passwords for database
- [ ] Rotate API keys periodically
- [ ] Enable Django security features (HSTS, etc.)

## Backup Strategy

```bash
# Database backup
pg_dump -U claude_goose_user claude_goose_db > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /opt/claude-goose
```

## Performance Tuning

### Gunicorn Workers

Rule of thumb: `(2 x $num_cores) + 1`

```bash
# Check CPU cores
nproc
```

### PostgreSQL

Edit `/etc/postgresql/*/main/postgresql.conf`:

```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
```

### Redis

Edit `/etc/redis/redis.conf`:

```
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## Support

For issues specific to deployment, check:
- Server logs
- Application logs
- Django documentation
- GitHub issues

Happy deploying! 🚀
