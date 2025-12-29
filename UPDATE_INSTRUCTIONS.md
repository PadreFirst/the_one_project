# 🚀 UPDATE INSTRUCTIONS

## ✅ Changes Made:

### 1. **Multipliers Added (10x and 100x)**
- Users can now pay **1x**, **10x**, or **100x** the base price
- Higher multipliers = higher rank in Hall of Fame
- Command `/buy` now shows buttons with multipliers

### 2. **Admin Panel**
- New command: `/admin` (requires password)
- **Features:**
  - 📊 View History (last 10 entries)
  - ↩️ Rollback Last Entry (undo if AI moderation failed)
  - 🚫 Block User by ID

### 3. **Improved Share Button**
- Share text now includes current King's message/caption
- More viral and engaging text
- Better formatting

---

## 📝 Deployment Steps:

### Step 1: Update `.env` Files

**On your local machine (Cursor):**
Add this line to your `.env` file:
```env
ADMIN_PASSWORD=your_secure_password_here
WEBAPP_URL=https://setup-holes-blocking-ferrari.trycloudflare.com
```

**On the server:**
```bash
ssh root@77.221.155.152
cd ~/the_one_project
nano .env
```

Add this line:
```env
ADMIN_PASSWORD=your_secure_password_here
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Step 2: Push to Git

**In Cursor terminal:**
```bash
git add .
git commit -m "Added admin panel, multipliers (10x, 100x), and improved share"
git push origin main
```

---

### Step 3: Deploy on Server

**In SSH terminal:**
```bash
cd ~/the_one_project
git pull origin main
systemctl restart theone_bot theone_webapp
systemctl status theone_bot theone_webapp --no-pager
```

---

### Step 4: Update BotFather (Menu Button URL)

1. Open [@BotFather](https://t.me/BotFather)
2. `/mybots` → `the_worlds_frame_bot`
3. `Bot Settings` → `Menu Button` → `Edit Menu Button URL`
4. Enter: `https://setup-holes-blocking-ferrari.trycloudflare.com`
5. Confirm

---

## 🎮 Testing:

### Test Multipliers:
1. Open bot: `/start`
2. Click "⚡ Quick Purchase" or `/buy`
3. You should see 3 buttons:
   - ⚡ 1 ⭐ Star (Standard)
   - 🔥 10 ⭐ Stars (10x Boost)
   - 💎 100 ⭐ Stars (100x VIP)

### Test Admin Panel:
1. Send `/admin` to bot
2. Enter your admin password
3. Try:
   - 📊 View History
   - ↩️ Rollback Last (if needed)
   - 🚫 Block User (test with fake ID)

### Test Share:
1. Open Mini App
2. Click Share button (arrow icon)
3. Check that the text includes current King's caption

---

## 📋 Admin Commands Reference:

| Command | Description |
|---------|-------------|
| `/admin` | Enter admin panel (requires password) |
| 📊 View History | See last 10 entries with IDs |
| ↩️ Rollback Last | Delete last entry (undo) |
| 🚫 Block User | Block user by ID (prevents future payments) |

---

## 🔐 Security Notes:

- **Change** `ADMIN_PASSWORD` to something secure!
- **Don't share** your admin password
- Use `/admin` only from your private chat with the bot
- Blocked users cannot make payments (even if they try)

---

## 🐛 If Something Goes Wrong:

### Bot not starting:
```bash
journalctl -u theone_bot -n 50 --no-pager
```

### Check if services are running:
```bash
systemctl status cloudflared theone_bot theone_webapp --no-pager
```

### Restart everything:
```bash
systemctl restart cloudflared theone_bot theone_webapp
```

---

## 📞 Next Steps:

1. ✅ Update `.env` (local + server)
2. ✅ Push to Git
3. ✅ Pull on server and restart
4. ✅ Update BotFather Menu Button URL
5. ✅ Test everything
6. 🎉 Launch!

---

**Good luck! 🚀**

