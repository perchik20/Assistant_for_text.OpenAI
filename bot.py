from aiogram import Bot, Dispatcher, executor, types
import datetime
import pytesseract
import cv2
import sqlite3
from PIL import Image
import imagehash as imagehash

from edit_data import add_data, get_data
from random_word import RandomWords


TOKEN = "yout:TOKEN"

active_users = {}
active_photos = {}
counter = 0

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = sqlite3.connect('test.db')


async def db_get_albums(album_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM albums WHERE album_name = '{album_name}'")
    result = cursor.fetchall()
    for line in result:
        if album_name in line:
            return False
    return album_name


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    global active_users
    global active_photos

    if message.from_user.id not in active_users:
        active_users[message.from_user.id] = 0
        await message.answer(f"Added {message.from_user.id} to active users")

    if message.from_user.id not in active_photos:
        active_photos[message.from_user.id] = []
        await message.answer(f"Added {message.from_user.id} to active photos")

    await bot.send_message(message.chat.id, "Send me photos, at the end send name of the album")
    active_users[message.from_user.id] = 1


@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    global active_users
    print(message)
    if message.from_user.id in active_users and active_users[message.from_user.id] == 1:
        await bot.send_message(message.chat.id, "Photo received")

        new_image_name = f"{message.from_user.id}_{message.photo[-1]['file_id']}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"

        active_photos[message.from_user.id].append(new_image_name)
        await message.photo[-1].download(f"static/photos/{new_image_name}")


@dp.message_handler(commands=['album'])
async def gen_album_name(message: types.Message):
    r = RandomWords()
    album_name = r.get_random_word()

    cur = db.cursor()
    while True:
        check_result = await db_get_albums(album_name)
        if not check_result:
            album_name = r.get_random_word()
        else:
            break

    await bot.send_message(message.chat.id, f"{album_name} album name is free")


@dp.message_handler()
async def album(message: types.Message):
    global active_users

    if message.from_user.id in active_users and active_users[message.from_user.id] == 1:
        await bot.send_message(message.chat.id, "Album received")

        for image_filename in active_photos[message.from_user.id]:
            await parse_photo(image_filename, message.text)

        active_users[message.from_user.id] = 0


async def parse_photo(photo_filename, album_name):
    global counter

    img = cv2.imread(f'static/photos/{photo_filename}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    config = "--oem 3 --psm 6"
    lang = 'rus+eng'
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

    question1 = pytesseract.image_to_string(img, lang=lang, config=config)
    question = question1.split(':')

    all_hash = get_data(f"SELECT hash FROM Answers WHERE album_name='{album_name}'")
    hash = imagehash.average_hash(Image.open(f'static/photos/{photo_filename}'))

    for i in all_hash:
        if i[0] == str(hash):
            print(f'{hash}->{i[0]}')
            return 0

    add_data(question[0], f'static/photos/{photo_filename}', album_name, hash)


if __name__ == '__main__':
    executor.start_polling(dp)
