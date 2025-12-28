# 👑 THE ONE - Telegram Mini App

**King of the Hill** game where users compete for vanity! Pay Telegram Stars, upload your photo, become THE ONE. Watch as the price grows 10% with each new king!

## 🎮 Game Concept

1. **Pay to Win**: Users pay Telegram Stars (XTR) to become the current King
2. **Upload Photo**: After payment, upload a photo that represents you
3. **AI Moderation**: All photos are checked by Google Gemini AI for prohibited content
4. **Price Growth**: Each new king pays 10% more than the previous one
5. **Hall of Fame**: Top 10 biggest spenders are immortalized

## 🛠 Tech Stack

- **Backend**: Python, aiogram 3.x, Flask
- **Frontend**: HTML/CSS/JS, Telegram WebApp API
- **Database**: SQLite (aiosqlite)
- **AI**: Google Gemini API (content moderation)
- **Payments**: Telegram Stars (XTR)

## 📁 Project Structure

```
the_one_project/
├── bot.py              # Telegram Bot (handles payments & photos)
├── webapp.py           # Flask server (API for Mini App)
├── database.py         # SQLite database logic
├── ai_check.py         # Google Gemini AI moderation
├── static/             # Frontend files
│   ├── index.html      # Mini App UI
│   ├── style.css       # Styling
│   └── app.js          # Frontend logic
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (create from .env.example)
└── game_database.db    # SQLite database (auto-created)
```

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create `.env` file (copy from `.env.example`):
```bash
# Telegram Bot Token (from @BotFather)
BOT_TOKEN=your_bot_token_here

# Google AI API Key (from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=your_google_api_key_here

# Telegram Channel ID (for posting winners, format: -1001234567890)
CHANNEL_ID=your_channel_id_here

# Mini App URL (use ngrok during development)
WEBAPP_URL=https://your-ngrok-url.ngrok.io
```

### 3. Setup Telegram Channel
1. Create a public channel
2. Add bot as administrator
3. Get channel ID using @userinfobot

### 4. Run the Backend

**Terminal 1: Start Telegram Bot**
```bash
python bot.py
```

**Terminal 2: Start Flask Web Server**
```bash
python webapp.py
```

### 5. Expose Flask Server (for Testing)

Use **ngrok** to expose your local Flask server:
```bash
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and:
1. Add it to `.env` as `WEBAPP_URL`
2. Set it in BotFather Mini App settings

### 6. Configure Mini App in BotFather

1. Open @BotFather
2. Select your bot
3. Go to **Bot Settings** → **Menu Button** → **Edit Menu Button URL**
4. Enter your ngrok URL: `https://your-ngrok-url.ngrok.io`

## 🎯 How to Use

### For Players:
- **`/start`** - See current king and price, open Mini App
- **`/buy`** - Quick purchase (pay 1 XTR in test mode)
- **`/app`** - Open Mini App directly
- **Mini App** - View current king, Hall of Fame, and dethrone button

### For Developers:
- **Test Mode**: Payment is fixed at 1 XTR for testing
- **Production**: Remove `TESTING MODE` in `bot.py` line 40-41

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve Mini App (index.html) |
| `/api/current` | GET | Get current king data |
| `/api/hall-of-fame` | GET | Get top 10 kings |
| `/api/photo/<photo_id>` | GET | Get photo URL by file_id |
| `/health` | GET | Server health check |

## 📸 Features

### ✅ Implemented
- Payment system (Telegram Stars)
- Photo upload & AI moderation
- Mini App UI (responsive design)
- Hall of Fame (Top 10)
- Share button
- Channel posting

### 🚧 Test Mode
- **Payment**: Fixed at 1 XTR (for testing)
- **UI**: Shows simulated price growth

### 🔮 Future Enhancements
- Real price growth (remove test mode)
- User profiles
- Leaderboard animations
- Push notifications
- Refund system

## ⚠️ Important Notes

### Security
- Never commit `.env` file to git
- In production, don't expose bot token in frontend
- Use proper authentication for API endpoints

### AI Moderation
Gemini checks for:
- Politics & War (Putin, Ukraine, weapons)
- Pornography & Gore
- Racism & Hate Speech

### Testing
1. Use ngrok for local testing
2. Test payments with small amounts
3. Monitor bot logs for errors

## 🎨 Frontend Customization

Edit `static/style.css` to customize:
- Colors
- Fonts
- Animations
- Layout

Edit `static/app.js` to add:
- New features
- Analytics
- Error handling

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token |
| `GOOGLE_API_KEY` | ✅ | Google AI API Key |
| `CHANNEL_ID` | ✅ | Telegram Channel ID |
| `WEBAPP_URL` | ⚠️ | Mini App URL (ngrok in dev) |

## 🐛 Troubleshooting

### Bot doesn't start
- Check `BOT_TOKEN` in `.env`
- Ensure database is initialized

### Mini App not loading
- Verify `WEBAPP_URL` is correct
- Check if Flask is running
- Ensure ngrok is active

### Photos not displaying
- Check if bot token is correct in `webapp.py`
- Verify photo_id is valid

### AI moderation fails
- Check `GOOGLE_API_KEY`
- Verify API quota
- Check model name (gemini-3-flash-preview)

## 🚀 Deployment (Production)

### Recommended Stack:
- **Server**: VPS (DigitalOcean, Hetzner, etc.)
- **Web Server**: Nginx + Gunicorn
- **Process Manager**: systemd or supervisor
- **SSL**: Let's Encrypt (certbot)

### Quick Deploy:
1. Get a VPS with public IP
2. Install Python & dependencies
3. Set up domain/SSL
4. Update `WEBAPP_URL` in `.env`
5. Use supervisor to keep processes running

## 📞 Support

- Issues: GitHub Issues
- Questions: Telegram @your_username
- Updates: Follow the channel

## 🎉 Ready to Go!

Start both servers and test the Mini App! 👑⭐

```bash
# Terminal 1
python bot.py

# Terminal 2
python webapp.py

# Terminal 3
ngrok http 5000
```

Good luck, and may the best King win! 🏆




