# ✅ DEPLOYMENT CHECKLIST

## 📋 Pre-Deployment

- [ ] All code changes reviewed and tested locally
- [ ] `.env` file updated with `ADMIN_PASSWORD`
- [ ] `.env` file updated with correct `WEBAPP_URL`
- [ ] Git repository is up to date

---

## 🚀 Deployment Steps

### 1. Local Machine (Cursor)

- [ ] Update `.env` file:
  ```env
  ADMIN_PASSWORD=your_secure_password
  WEBAPP_URL=https://setup-holes-blocking-ferrari.trycloudflare.com
  ```

- [ ] Stage all changes:
  ```bash
  git add .
  ```

- [ ] Commit changes:
  ```bash
  git commit -m "Added admin panel, 10x/100x multipliers, improved share"
  ```

- [ ] Push to GitHub:
  ```bash
  git push origin main
  ```

---

### 2. Server (Aeza VPS)

- [ ] Connect to server:
  ```bash
  ssh root@77.221.155.152
  ```
  Password: `IYRZlbVilRaO`

- [ ] Navigate to project:
  ```bash
  cd ~/the_one_project
  ```

- [ ] Pull latest code:
  ```bash
  git pull origin main
  ```

- [ ] Update `.env` on server:
  ```bash
  nano .env
  ```
  Add line: `ADMIN_PASSWORD=your_secure_password`
  
  Save: `Ctrl+O`, `Enter`, `Ctrl+X`

- [ ] Restart services:
  ```bash
  systemctl restart theone_bot theone_webapp
  ```

- [ ] Verify services are running:
  ```bash
  systemctl status theone_bot theone_webapp --no-pager
  ```

- [ ] Check Cloudflare tunnel URL:
  ```bash
  journalctl -u cloudflared -n 30 --no-pager | grep "https://"
  ```

---

### 3. BotFather Configuration

- [ ] Open [@BotFather](https://t.me/BotFather)
- [ ] Send `/mybots`
- [ ] Select `the_worlds_frame_bot`
- [ ] Click `Bot Settings`
- [ ] Click `Menu Button`
- [ ] Click `Edit Menu Button URL`
- [ ] Enter: `https://setup-holes-blocking-ferrari.trycloudflare.com`
- [ ] Confirm

---

## 🧪 Testing

### Basic Functionality
- [ ] Bot responds to `/start`
- [ ] Mini App opens from button
- [ ] Current King's photo displays
- [ ] Hall of Fame loads

### New Features: Multipliers
- [ ] Send `/buy` to bot
- [ ] Verify 3 buttons appear:
  - [ ] ⚡ 1 ⭐ Star (Standard)
  - [ ] 🔥 10 ⭐ Stars (10x Boost)
  - [ ] 💎 100 ⭐ Stars (100x VIP)
- [ ] Test payment with 1x multiplier
- [ ] Verify invoice shows correct amount

### New Features: Admin Panel
- [ ] Send `/admin` to bot
- [ ] Enter admin password
- [ ] Verify admin menu appears:
  - [ ] 📊 View History
  - [ ] ↩️ Rollback Last
  - [ ] 🚫 Block User
- [ ] Test "View History" - should show last 10 entries
- [ ] Test "Rollback" (only if safe to do so)
- [ ] Test "Block User" with test ID

### New Features: Share
- [ ] Open Mini App
- [ ] Click Share button (arrow icon)
- [ ] Verify share text includes:
  - [ ] Current King's name/username
  - [ ] Current price
  - [ ] King's caption/message (if present)
  - [ ] Call to action

---

## 🔍 Monitoring

- [ ] Check bot logs for errors:
  ```bash
  journalctl -u theone_bot -n 50 --no-pager
  ```

- [ ] Check webapp logs:
  ```bash
  journalctl -u theone_webapp -n 50 --no-pager
  ```

- [ ] Check cloudflared status:
  ```bash
  systemctl status cloudflared --no-pager
  ```

---

## 🚨 Emergency Rollback

If something goes wrong:

1. **Revert code:**
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **On server:**
   ```bash
   cd ~/the_one_project
   git pull origin main
   systemctl restart theone_bot theone_webapp
   ```

---

## 📊 Post-Deployment

- [ ] Monitor bot for 15 minutes
- [ ] Check for any error messages
- [ ] Verify payments are working
- [ ] Test with real users (if available)
- [ ] Update documentation if needed
- [ ] Notify team/stakeholders

---

## 🎉 Success Criteria

✅ All services running (green status)  
✅ Bot responds to commands  
✅ Mini App loads correctly  
✅ Payments work (1x, 10x, 100x)  
✅ Admin panel accessible  
✅ Share button includes King's message  
✅ No errors in logs  

---

**Deployment Complete!** 🚀

Date: __________  
Deployed by: __________  
Notes: __________

