import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен твоего бота
TOKEN = "7909234577:AAFq9CMjzlEgnhO_Uz2bKYbCGudbqhAWoX8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Имитация базы данных маршрутов
ROUTES_DATA = {
    f"route_{i}": {
        "text": f"📍 **Маршрут №{i}**\n\n🚛 Порядок: 1. Склад -> 2. Точка А\n🔐 Сигнализация: Код 1234\n🗺 [Навигатор](https://google.com/maps)",
        "keys": ["FILE_ID_1", "FILE_ID_2"] # Сюда вставим ID фото ключей
    } for i in range(1, 11)
}

# 1. Главное меню (10 кнопок)
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.button(text=f"Маршрут-{i}", callback_data=f"route_{i}")
    
    builder.adjust(2) # Кнопки в два ряда
    await message.answer("Выберите маршрут:", reply_markup=builder.as_markup())

# 2. Обработка нажатия на маршрут
@dp.callback_query(F.data.startswith("route_"))
async def show_route(callback: types.CallbackQuery):
    route_id = callback.data
    data = ROUTES_DATA.get(route_id)
    
    # Кнопка для просмотра ключей
    builder = InlineKeyboardBuilder()
    builder.button(text="📸 Посмотреть фото ключей", callback_data=f"keys_{route_id}")
    
    await callback.message.answer(data["text"], parse_mode="Markdown", reply_markup=builder.as_markup())
    await callback.answer()

# 3. Отправка фото ключей (альбомом)
@dp.callback_query(F.data.startswith("keys_"))
async def show_keys(callback: types.CallbackQuery):
    route_id = callback.data.replace("keys_", "")
    photos = ROUTES_DATA[route_id]["keys"]
    
    # Формируем группу медиа (альбом)
    media_group = [types.InputMediaPhoto(media=photo_id) for photo_id in photos]
    
    await callback.message.answer_media_group(media=media_group)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
