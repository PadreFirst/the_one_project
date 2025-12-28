# 🚀 БЫСТРЫЙ СТАРТ НА AEZA VPS

## 1️⃣ Купи VPS на Aeza.net
- Тариф: START-1 (200₽/мес)
- ОС: Ubuntu 22.04
- Получи IP и пароль root

## 2️⃣ Подключись к серверу
```bash
ssh root@YOUR_IP
```

## 3️⃣ Загрузи проект
**Если есть Git репозиторий:**
```bash
cd /tmp
git clone https://github.com/YOUR_USERNAME/the_one_project.git
```

**Если НЕТ Git (загрузи через SCP с твоего ПК):**
```powershell
# На твоем Windows компе:
cd C:\Users\range\Desktop
scp -r the_one_project root@YOUR_IP:/tmp/
```

## 4️⃣ Запусти автодеплой
```bash
cd /tmp/the_one_project
chmod +x deploy.sh
./deploy.sh
```

## 5️⃣ Настрой токены
```bash
nano /opt/the_worlds_frame/.env
```

Вставь:
```
BOT_TOKEN=твой_токен
GOOGLE_API_KEY=твой_ключ
CHANNEL_ID=@твой_канал
WEBAPP_URL=http://YOUR_IP
```

Сохрани: `Ctrl+O`, `Enter`, `Ctrl+X`

## 6️⃣ Перезапусти
```bash
systemctl restart theone-bot theone-webapp
```

## 7️⃣ Проверь
Открой в браузере: `http://YOUR_IP`

## ✅ ГОТОВО!

---

## 📊 Проверить статус:
```bash
systemctl status theone-bot theone-webapp
```

## 📜 Логи:
```bash
journalctl -u theone-bot -f
```

## 🔄 Обновить код:
```bash
cd /opt/the_worlds_frame
git pull
systemctl restart theone-bot theone-webapp
```

---

**Полная инструкция:** `DEPLOY_INSTRUCTIONS.md`

