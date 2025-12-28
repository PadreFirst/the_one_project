#!/bin/bash
# Автоматический деплой THE WORLD'S FRAME на VPS (Aeza / Ubuntu)
# Запустите этот скрипт на чистом Ubuntu 22.04 сервере

set -e

echo "🚀 Starting deployment of THE WORLD'S FRAME..."

# 1. Обновление системы
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# 2. Установка Python 3.11 и pip
echo "🐍 Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# 3. Создание пользователя для приложения (если не существует)
if ! id -u theone > /dev/null 2>&1; then
    echo "👤 Creating application user..."
    sudo useradd -m -s /bin/bash theone
fi

# 4. Создание директории проекта
echo "📁 Setting up project directory..."
sudo mkdir -p /opt/the_worlds_frame
sudo chown theone:theone /opt/the_worlds_frame

# 5. Копирование файлов проекта
echo "📋 Copying project files..."
sudo cp -r /tmp/the_one_project/* /opt/the_worlds_frame/
sudo chown -R theone:theone /opt/the_worlds_frame

# 6. Создание виртуального окружения и установка зависимостей
echo "📚 Installing Python dependencies..."
cd /opt/the_worlds_frame
sudo -u theone python3.11 -m venv venv
sudo -u theone /opt/the_worlds_frame/venv/bin/pip install --upgrade pip
sudo -u theone /opt/the_worlds_frame/venv/bin/pip install -r requirements.txt

# 7. Настройка .env файла
echo "⚙️ Setting up environment variables..."
if [ ! -f /opt/the_worlds_frame/.env ]; then
    echo "❗ Please create .env file manually with your tokens!"
    echo "Template:"
    echo "BOT_TOKEN=your_bot_token"
    echo "GOOGLE_API_KEY=your_google_api_key"
    echo "CHANNEL_ID=@your_channel"
    echo "WEBAPP_URL=https://your-domain.com"
fi

# 8. Создание systemd сервисов
echo "🔧 Creating systemd services..."

# Bot service
sudo tee /etc/systemd/system/theone-bot.service > /dev/null <<EOF
[Unit]
Description=The World's Frame - Telegram Bot
After=network.target

[Service]
Type=simple
User=theone
WorkingDirectory=/opt/the_worlds_frame
Environment="PATH=/opt/the_worlds_frame/venv/bin"
ExecStart=/opt/the_worlds_frame/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Flask service
sudo tee /etc/systemd/system/theone-webapp.service > /dev/null <<EOF
[Unit]
Description=The World's Frame - Flask Web App
After=network.target

[Service]
Type=simple
User=theone
WorkingDirectory=/opt/the_worlds_frame
Environment="PATH=/opt/the_worlds_frame/venv/bin"
ExecStart=/opt/the_worlds_frame/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:5000 webapp:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 9. Установка gunicorn для продакшена
echo "📦 Installing gunicorn..."
sudo -u theone /opt/the_worlds_frame/venv/bin/pip install gunicorn

# 10. Настройка Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/theone > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Для Telegram WebApp
        add_header Access-Control-Allow-Origin *;
    }

    location /static {
        alias /opt/the_worlds_frame/static;
        expires 30d;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/theone /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 11. Перезагрузка systemd и запуск сервисов
echo "🎬 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable theone-bot theone-webapp
sudo systemctl start theone-bot theone-webapp

# 12. Проверка статуса
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service status:"
sudo systemctl status theone-bot --no-pager -l
sudo systemctl status theone-webapp --no-pager -l
echo ""
echo "🌐 Your app should be available at: http://$(curl -s ifconfig.me)"
echo ""
echo "⚙️ Next steps:"
echo "1. Edit /opt/the_worlds_frame/.env with your tokens"
echo "2. Restart services: sudo systemctl restart theone-bot theone-webapp"
echo "3. Check logs: sudo journalctl -u theone-bot -f"
echo ""
echo "🔒 Optional: Set up SSL with certbot for HTTPS"

