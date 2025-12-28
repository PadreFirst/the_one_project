import aiosqlite
import os

DB_NAME = "game_database.db"

async def init_db():
    """Создает таблицу, если её нет, и добавляет первую запись"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS game_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                current_price INTEGER,
                photo_id TEXT,
                text TEXT,
                user_link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем индексы для быстрого поиска
        await db.execute("CREATE INDEX IF NOT EXISTS idx_price ON game_state(current_price DESC)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_user ON game_state(user_id)")
        
        # Проверяем, есть ли хоть одна запись. Если нет - создаем "нулевого царя"
        async with db.execute("SELECT COUNT(*) FROM game_state") as cursor:
            count = await cursor.fetchone()
            if count[0] == 0:
                print("Database empty, creating initial entry...")
                await db.execute("""
                    INSERT INTO game_state (user_id, current_price, photo_id, text, user_link)
                    VALUES (0, 1, '', 'Throne awaits its first ruler', '')
                """)
        await db.commit()

async def get_game_state():
    """Возвращает последнюю (актуальную) запись игры"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT current_price, user_id, photo_id, text, user_link FROM game_state ORDER BY id DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if row:
                return row
            return (1, 0, "", "", "")

async def update_game_state(user_id, photo_id, text, user_link, new_price):
    """Добавляет нового Царя в историю"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO game_state (user_id, current_price, photo_id, text, user_link)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, new_price, photo_id, text, user_link))
        await db.commit()

async def get_hall_of_fame(limit=10):
    """Возвращает топ-10 самых дорогих покупок с фото и текстом"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT user_id, user_link, current_price, photo_id, text
            FROM game_state
            WHERE user_id > 0
            ORDER BY current_price DESC
            LIMIT ?
        """, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [
                {
                    "user_id": row[0],
                    "user_link": row[1],
                    "price": row[2],
                    "photo_id": row[3],
                    "text": row[4]
                }
                for row in rows
            ]

# Синхронные версии для Flask (т.к. Flask не async)
def get_game_state_sync():
    """Синхронная версия get_game_state для Flask"""
    import sqlite3
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT current_price, user_id, photo_id, text, user_link FROM game_state ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "current_price": row[0],
            "user_id": row[1],
            "photo_id": row[2],
            "text": row[3],
            "user_link": row[4]
        }
    return {"current_price": 1, "user_id": 0, "photo_id": "", "text": "", "user_link": ""}

def get_hall_of_fame_sync(limit=10):
    """Синхронная версия get_hall_of_fame для Flask с фото и текстом"""
    import sqlite3
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, user_link, current_price, photo_id, text
        FROM game_state
        WHERE user_id > 0
        ORDER BY current_price DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "user_id": row[0],
            "user_link": row[1],
            "price": row[2],
            "photo_id": row[3],
            "text": row[4]
        }
        for row in rows
    ]
