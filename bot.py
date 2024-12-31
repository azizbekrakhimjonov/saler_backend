from aiogram import Bot, Dispatcher, executor, types
import aiohttp

API_URL_REGISTER = "https://30e0-84-54-72-253.ngrok-free.app/api/register/"
API_URL_PROMOCODE = "https://30e0-84-54-72-253.ngrok-free.app/api/code/"
TOKEN = "7939706206:AAEiTpATrT9-_l5SyKj0_E5yp8soBXPQDws"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    telegram_id = str(message.from_user.id)

    # Check if the user is already registered
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json={"telegram_id": telegram_id}) as response:
            if response.status == 200:
                data = await response.json()
                total_points = data.get('total_points', 0)  # Assuming the API returns the user's points
                await message.answer(f"Assalomu alaykum! Siz avval ro'yxatdan o'tgansiz.\nJami ballaringiz: {total_points}")
                # Send a button for the user to apply a promocode
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                promocode_button = types.KeyboardButton("Promokod yuborish")
                markup.add(promocode_button)
                await message.answer("Iltimos, 'Promokod yuborish' tugmasini bosing.", reply_markup=markup)
            else:
                # If the user is not registered, ask for registration information
                await message.answer("Assalomu alaykum! To'liq ismingizni kiriting.")
                user_data[message.from_user.id] = {}

@dp.message_handler(lambda message: message.from_user.id in user_data and 'fullname' not in user_data[message.from_user.id])
async def get_fullname(message: types.Message):
    user_data[message.from_user.id]['fullname'] = message.text
    await message.answer("Telefon raqamingizni kiriting (misol: +998901234567).")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'phone_number' not in user_data[message.from_user.id])
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone_number'] = message.text
    await message.answer("Manzilingizni kiriting.")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'address' not in user_data[message.from_user.id])
async def get_address(message: types.Message):
    user_data[message.from_user.id]['address'] = message.text
    telegram_id = str(message.from_user.id)
    fullname = user_data[message.from_user.id]['fullname']
    phone_number = user_data[message.from_user.id]['phone_number']
    address = user_data[message.from_user.id]['address']

    # Send data to the API for registration
    payload = {
        "telegram_id": telegram_id,
        "fullname": fullname,
        "phone_number": phone_number,
        "address": address
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_REGISTER, json=payload) as response:
            if response.status == 200:
                await message.answer("Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            else:
                error_message = (await response.json()).get('error', 'Xato yuz berdi.')
                await message.answer(f"Xatolik: {error_message}")

    user_data.pop(message.from_user.id)

@dp.message_handler(lambda message: message.text == "Promokod yuborish")
async def promocode_start(message: types.Message):
    await message.answer("Promokodingizni kiriting.")

@dp.message_handler()
async def check_promocode(message: types.Message):
    # Promokodni API ga yuborish
    telegram_id = str(message.from_user.id)
    promocode = message.text

    payload = {
        "telegram_id": telegram_id,
        "code": promocode
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_PROMOCODE, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                added_points = data.get('added_points', 0)
                total_points = data.get('total_points', 0)
                await message.answer(f"Promokod muvaffaqiyatli qo'llandi!\nQo'shilgan ballar: {added_points}\nJami ballaringiz: {total_points}")
            else:
                error_message = (await response.json()).get('error', 'Xato yuz berdi.')
                await message.answer(f"Xatolik: {error_message}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
