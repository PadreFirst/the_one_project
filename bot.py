import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from database import init_db, get_game_state, update_game_state, rollback_last_entry, get_history, block_user, is_user_blocked
from ai_check import check_image

logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-ngrok-url.ngrok.io")  # URL твоего Mini App
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Админ пароль

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class GameStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_admin_password = State()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Check if user came with deep link (e.g. /start buy)
    args = message.text.split(maxsplit=1)
    if len(args) > 1 and args[1] == "buy":
        # User clicked "CLAIM THE THRONE" from Mini App
        await cmd_buy(message)
        return
    
    state = await get_game_state()
    # state = (current_price, current_king_id, photo_id, text, user_link)
    price = state[0]
    
    # Создаем кнопку для открытия Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Enter The World's Frame", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="⚡ Quick Purchase", callback_data="quick_buy")]
    ])
    
    await message.answer(
        f"<b>THE WORLD'S FRAME</b>\n\n"
        f"One photo. One message. Only ONE person in the world.\n\n"
        f"Current throne price: <b>{price} ⭐ Stars</b>\n\n"
        f"Can you take their place?",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.message(Command("buy"))
async def cmd_buy(message: Message):
    # Показываем кнопки с множителями
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ 1 ⭐ Star (Standard)", callback_data="buy_1")],
        [InlineKeyboardButton(text="🔥 10 ⭐ Stars (10x Boost)", callback_data="buy_10")],
        [InlineKeyboardButton(text="💎 100 ⭐ Stars (100x VIP)", callback_data="buy_100")]
    ])
    
    state = await get_game_state()
    price = state[0]
    
    await message.answer(
        f"<b>Choose Your Entry</b>\n\n"
        f"Current base price: {price} ⭐\n\n"
        f"🎯 <b>Multipliers:</b>\n"
        f"• <b>1x</b> - Standard entry\n"
        f"• <b>10x</b> - Boost visibility\n"
        f"• <b>100x</b> - VIP dominance\n\n"
        f"Higher multipliers = Higher rank in Hall of Fame!",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# Обработчики для множителей
@dp.callback_query(F.data.in_(["buy_1", "buy_10", "buy_100"]))
async def callback_buy_multiplier(callback: CallbackQuery):
    multiplier = int(callback.data.split("_")[1])
    price_to_pay = 1 * multiplier  # TESTING: всегда 1 * multiplier Stars
    
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"The World's Frame ({multiplier}x)",
        description=f"Become THE ONE. Multiplier: {multiplier}x = {price_to_pay} Stars",
        payload=f"king_buy_{multiplier}",
        currency="XTR",
        prices=[LabeledPrice(label=f"Throne Access {multiplier}x", amount=price_to_pay)],
        provider_token=""
    )

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    # Проверка блокировки
    if await is_user_blocked(message.from_user.id):
        await message.answer(
            "❌ <b>Access Denied</b>\n\n"
            "Your account has been restricted from using this service.",
            parse_mode="HTML"
        )
        return
    
    paid_amount = message.successful_payment.total_amount
    
    await state.update_data(paid_amount=paid_amount)
    await state.set_state(GameStates.waiting_for_photo)
    
    # Кнопки для выбора приватности
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Show my @username", callback_data="privacy_show")],
        [InlineKeyboardButton(text="🔒 Stay Anonymous", callback_data="privacy_hide")]
    ])
    
    await message.answer(
        "✅ <b>Payment Successful!</b>\n\n"
        "📸 Send your photo now (this will represent you as THE ONE)\n\n"
        "💬 <b>OPTIONAL:</b> Add caption (max 100 chars)\n"
        "Links are clickable — perfect for brands & ads.\n\n"
        "⛔ <b>FORBIDDEN:</b>\n"
        "• Politics, War, Weapons\n"
        "• Adult Content\n"
        "• Hate Speech\n\n"
        "Everything else is allowed.\n\n"
        "👤 <b>Privacy:</b> Choose below:",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# Обработчик callback для приватности
@dp.callback_query(F.data.in_(["privacy_show", "privacy_hide"]))
async def callback_privacy(callback: CallbackQuery, state: FSMContext):
    show_username = callback.data == "privacy_show"
    await state.update_data(show_username=show_username)
    
    status = "✅ Your @username will be visible" if show_username else "🔒 You will remain anonymous"
    
    await callback.answer(status, show_alert=False)
    await callback.message.edit_text(
        "✅ <b>Payment Successful!</b>\n\n"
        "📸 Send your photo now (this will represent you as THE ONE)\n\n"
        "⚠️ <b>IMPORTANT:</b> Non-square photos will be auto-cropped to fit.\n"
        "Best format: Square (1:1 ratio)\n\n"
        "💬 <b>OPTIONAL:</b> Add caption (max 100 chars)\n"
        "Links are clickable — perfect for brands & ads.\n\n"
        "⛔ <b>FORBIDDEN:</b>\n"
        "• Politics, War, Weapons\n"
        "• Adult Content\n"
        "• Hate Speech\n\n"
        f"👤 <b>Privacy:</b> {status}",
        parse_mode="HTML"
    )

@dp.message(GameStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Получаем текст (caption) если есть
    user_caption = message.caption if message.caption else ""
    
    # Ограничиваем до 100 символов
    if len(user_caption) > 100:
        await message.answer("⚠️ Caption too long! Max 100 characters. Please try again.")
        return
    
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    downloaded_file = await bot.download_file(file_path)
    local_path = f"temp_{message.from_user.id}.jpg"
    
    with open(local_path, "wb") as new_file:
        new_file.write(downloaded_file.read())
        
    msg = await message.answer("🤖 AI is checking your photo... (Wait 3 sec)")
    
    is_allowed, reason = await check_image(local_path)
    
    # Clean up
    if os.path.exists(local_path):
        os.remove(local_path)
    
    if not is_allowed:
        await msg.delete() # Remove "Checking..." message
        await message.answer(
            f"❌ <b>Submission Rejected</b>\n\n"
            f"Reason: {reason}\n\n"
            "Please submit a different image. Your payment remains secure.",
            parse_mode="HTML"
        )
        return

    data = await state.get_data()
    paid_amount = data.get("paid_amount", 1)
    show_username = data.get("show_username", True)  # По умолчанию показываем
    
    user_name = message.from_user.username or message.from_user.first_name
    
    # Решаем показывать ли username
    if show_username and message.from_user.username:
        user_link = f"@{message.from_user.username}"
    else:
        user_link = "Anonymous"  # Анонимный пользователь
    
    # Сохраняем в БД с текстом пользователя
    await update_game_state(
        user_id=message.from_user.id,
        photo_id=file_id,
        text=user_caption,  # Сохраняем текст пользователя
        user_link=user_link,
        new_price=paid_amount
    )
    
    # Формируем caption для канала с кликабельными ссылками
    channel_caption = f"👑 <b>THE ONE</b>\n\n"
    
    if user_caption:
        channel_caption += f"💬 {user_caption}\n\n"
    
    # Показываем username только если не анонимный
    if user_link != "Anonymous":
        channel_caption += f"{user_link} • {paid_amount} ⭐"
    else:
        channel_caption += f"Anonymous • {paid_amount} ⭐"
    
    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=file_id,
            caption=channel_caption,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Channel Error: {e}")
        await message.answer(f"(Dev info: Channel post failed: {e})")

    await msg.delete()
    await message.answer(
        f"👑 <b>You are now THE ONE.</b>\n\nYour presence is now visible to the world.",
        parse_mode="HTML"
    )
    await state.clear()

@dp.message(GameStates.waiting_for_photo)
async def process_not_photo(message: Message):
    await message.answer("Please send an image file.")

# Обработчик callback для Quick Buy
from aiogram.types import CallbackQuery

@dp.callback_query(F.data == "quick_buy")
async def callback_quick_buy(callback: CallbackQuery):
    await callback.answer()
    await cmd_buy(callback.message)

# Команда /app для открытия Mini App
@dp.message(Command("app"))
async def cmd_app(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Enter THE ONE", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    
    await message.answer(
        "<b>THE ONE</b>\n\nAccess the exclusive platform where prestige meets competition.",
        parse_mode="HTML",
        reply_markup=keyboard
    )

# ============ ADMIN COMMANDS ============

@dp.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    """Команда для входа в админ панель"""
    await state.set_state(GameStates.waiting_for_admin_password)
    await message.answer(
        "🔐 <b>Admin Access</b>\n\nEnter admin password:",
        parse_mode="HTML"
    )

@dp.message(GameStates.waiting_for_admin_password)
async def process_admin_password(message: Message, state: FSMContext):
    """Проверка пароля админа"""
    if message.text == ADMIN_PASSWORD:
        await state.clear()
        await state.update_data(is_admin=True)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 View History", callback_data="admin_history")],
            [InlineKeyboardButton(text="↩️ Rollback Last", callback_data="admin_rollback")],
            [InlineKeyboardButton(text="🚫 Block User", callback_data="admin_block")]
        ])
        
        await message.answer(
            "✅ <b>Admin Access Granted</b>\n\n"
            "Choose action:",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await state.clear()
        await message.answer("❌ Incorrect password.")

@dp.callback_query(F.data == "admin_history")
async def callback_admin_history(callback: CallbackQuery):
    """Показать историю последних 10 записей"""
    history = await get_history(limit=10)
    
    if not history:
        await callback.answer("No history yet.", show_alert=True)
        return
    
    text = "<b>📊 Last 10 Entries:</b>\n\n"
    for i, entry in enumerate(history, 1):
        user_link = entry['user_link'] if entry['user_link'] else "Anonymous"
        text += f"{i}. {user_link} - {entry['price']} ⭐\n"
        if entry['text']:
            text += f"   💬 \"{entry['text'][:50]}...\"\n"
        text += f"   🆔 ID: {entry['id']}\n\n"
    
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_rollback")
async def callback_admin_rollback(callback: CallbackQuery):
    """Откатить последнюю запись"""
    success = await rollback_last_entry()
    
    if success:
        await callback.answer("✅ Last entry rolled back!", show_alert=True)
        await callback.message.answer(
            "✅ <b>Rollback Successful</b>\n\n"
            "The previous entry has been restored.",
            parse_mode="HTML"
        )
    else:
        await callback.answer("❌ Cannot rollback. No entries or only initial entry left.", show_alert=True)

@dp.callback_query(F.data == "admin_block")
async def callback_admin_block(callback: CallbackQuery, state: FSMContext):
    """Запросить ID пользователя для блокировки"""
    await callback.answer()
    await callback.message.answer(
        "🚫 <b>Block User</b>\n\n"
        "Send user ID to block (numeric):",
        parse_mode="HTML"
    )
    await state.set_state(GameStates.waiting_for_admin_password)  # Reusing state
    await state.update_data(admin_action="block")

# Обработчик для блокировки пользователя
@dp.message(lambda message: message.text and message.text.isdigit())
async def process_admin_block_user(message: Message, state: FSMContext):
    """Блокировка пользователя по ID"""
    data = await state.get_data()
    
    if data.get("admin_action") == "block":
        user_id = int(message.text)
        await block_user(user_id)
        await message.answer(
            f"✅ User {user_id} has been blocked.",
            parse_mode="HTML"
        )
        await state.clear()

# Проверка блокировки перед успешной оплатой
async def check_if_blocked(user_id: int) -> bool:
    """Проверяет, заблокирован ли пользователь"""
    return await is_user_blocked(user_id)

async def main():
    await init_db()
    print("Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stop")