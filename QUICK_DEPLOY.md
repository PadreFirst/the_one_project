# ⚡ QUICK DEPLOY CHEAT SHEET

## 🔧 Local Setup (Cursor)

### 1. Update `.env` file:
```env
ADMIN_PASSWORD=your_secure_password
WEBAPP_URL=https://setup-holes-blocking-ferrari.trycloudflare.com
```

### 2. Push to Git:
```bash
git add .
git commit -m "Added admin panel, multipliers, improved share"
git push origin main
```

---

## 🚀 Server Deployment (SSH)

### Connect to server:
```bash
ssh root@77.221.155.152
```

Password: `IYRZlbVilRaO`

### Deploy:
```bash
cd ~/the_one_project
git pull origin main
systemctl restart theone_bot theone_webapp
systemctl status theone_bot theone_webapp --no-pager
```

---

## 📱 Update BotFather

1. Open [@BotFather](https://t.me/BotFather)
2. `/mybots` → `the_worlds_frame_bot`
3. `Bot Settings` → `Menu Button` → `Edit Menu Button URL`
4. Enter: `https://setup-holes-blocking-ferrari.trycloudflare.com`

---

## ✅ Test

1. Open bot: `/start`
2. Try `/buy` - should see 3 multiplier buttons
3. Try `/admin` - enter password
4. Open Mini App - test Share button

---

## 🆘 Emergency Commands

```bash
# View logs
journalctl -u theone_bot -n 50 --no-pager

# Restart everything
systemctl restart cloudflared theone_bot theone_webapp

# Check status
systemctl status cloudflared theone_bot theone_webapp --no-pager

# Get current Cloudflare URL
journalctl -u cloudflared -n 30 --no-pager | grep "https://"
```

---

## 🎯 New Features:

✅ Multipliers (1x, 10x, 100x)  
✅ Admin Panel (`/admin`)  
✅ Improved Share (includes King's message)  
✅ Block User functionality  
✅ Rollback last entry  
✅ View history  

---

**Done!** 🎉

