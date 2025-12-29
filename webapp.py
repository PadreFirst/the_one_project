import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv
from database import get_game_state_sync, get_hall_of_fame_sync
from functools import wraps
from time import time

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)  # Разрешаем кросс-доменные запросы для Telegram Mini App

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Simple rate limiting
request_history = {}

def rate_limit(max_requests=30, window=60):
    """Rate limiter: max_requests per window seconds"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time()
            # Clean old entries
            for ip in list(request_history.keys()):
                request_history[ip] = [req for req in request_history[ip] if now - req < window]
            
            # Check current IP
            from flask import request
            ip = request.remote_addr
            if ip not in request_history:
                request_history[ip] = []
            
            if len(request_history[ip]) >= max_requests:
                return jsonify({"success": False, "error": "Rate limit exceeded. Please try again later."}), 429
            
            request_history[ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def index():
    """Главная страница Mini App"""
    return send_from_directory('static', 'index.html')

@app.route('/api/current', methods=['GET'])
@rate_limit(max_requests=60, window=60)
def api_current():
    """API: Получить текущего короля и цену"""
    try:
        state = get_game_state_sync()
        
        # Рассчитываем "симулированную" цену для UI (растет на 10%)
        # Но реальная оплата всегда 1 XTR в тестовом режиме
        simulated_price = state['current_price']
        
        return jsonify({
            "success": True,
            "data": {
                "user_id": state['user_id'],
                "user_link": state['user_link'],
                "photo_id": state['photo_id'],
                "text": state['text'],  # Текст пользователя (до 40 символов)
                "simulated_price": simulated_price,  # Показываем в UI
                "real_payment_price": 1,  # Реальная цена для оплаты (тестовый режим)
                "usd_estimate": round(simulated_price * 0.013, 2)  # 1 XTR ≈ $0.013
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/hall-of-fame', methods=['GET'])
@rate_limit(max_requests=60, window=60)
def api_hall_of_fame():
    """API: Получить топ-N самых дорогих покупок"""
    try:
        limit = int(request.args.get('limit', 10))
        hall = get_hall_of_fame_sync(limit=limit)
        return jsonify({
            "success": True,
            "data": hall
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/photo/<photo_id>')
def get_photo(photo_id):
    """API: Прокси для получения фото напрямую из Telegram"""
    import requests
    try:
        # Безопасная валидация photo_id
        if not photo_id or len(photo_id) > 200:
            return "Invalid photo_id", 400
        
        # Получаем file_path
        file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={photo_id}"
        response = requests.get(file_url, timeout=10)
        data = response.json()
        
        if not data.get('ok'):
            return "Photo not found", 404
        
        file_path = data['result']['file_path']
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        
        # Скачиваем и возвращаем картинку напрямую
        photo_response = requests.get(photo_url, timeout=10, stream=True)
        photo_response.raise_for_status()
        
        # Возвращаем как image
        from flask import Response
        return Response(
            photo_response.iter_content(chunk_size=8192),
            mimetype='image/jpeg',
            headers={
                'Cache-Control': 'public, max-age=3600',
                'Content-Type': 'image/jpeg'
            }
        )
    except requests.RequestException as e:
        return f"Network error: {str(e)}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/health')
def health():
    """Проверка работоспособности сервера"""
    return jsonify({"status": "ok", "service": "THE ONE Mini App"})

if __name__ == '__main__':
    print("Flask server starting...")
    print("Mini App will be available at: http://localhost:5000")
    print("Use ngrok to expose it for Telegram: ngrok http 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
