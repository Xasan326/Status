import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import UserStatusOnline

# Ваши данные API
api_id = '20768912'
api_hash = 'f4c84f85a1a62402f9b290b1c4cd2ff2'
phone = '+998339388185'

# Пути к вашим фотографиям профиля
online_photo = '/data/data/com.termux/files/home/Status/status/1.jpg'
offline_photo = '/data/data/com.termux/files/home/Status/status/0.jpg'

# Создаем клиент и подключаемся
client = TelegramClient('session_name', api_id, api_hash)

# Переменные для хранения предыдущего статуса и фото, установленного программой
previous_status_online = None
previous_uploaded_photo = None  # Хранит ссылку на загруженное программой фото

async def main():
    global previous_status_online, previous_uploaded_photo
    await client.start()
    
    while True:
        # Получаем информацию о себе
        me = await client.get_me()

        # Определяем текущий статус (онлайн или оффлайн)
        is_online = isinstance(me.status, UserStatusOnline)
        
        # Если статус изменился, обновляем фото профиля
        if is_online != previous_status_online:
            if is_online:
                print("Вы в сети, обновляем фото профиля на онлайн изображение.")
                new_photo = online_photo
            else:
                print("Вы оффлайн, обновляем фото профиля на оффлайн изображение.")
                new_photo = offline_photo
            
            # Обновляем фото профиля и удаляем предыдущее фото, установленное программой
            await update_profile_photo(new_photo)
            
            # Обновляем предыдущий статус
            previous_status_online = is_online
        else:
            print("Статус не изменился, фото профиля не обновляется.")

        # Ждем заданное время перед следующей проверкой
        await asyncio.sleep(1)  # Проверять каждую минуту

async def update_profile_photo(photo_path):
    global previous_uploaded_photo

    # Проверяем, что файл существует
    if not os.path.isfile(photo_path):
        print(f"Файл не найден: {photo_path}")
        return

    # Загружаем файл изображения на сервер Telegram
    file = await client.upload_file(photo_path)
    
    # Устанавливаем новое фото профиля и сохраняем ссылку на него
    result = await client(UploadProfilePhotoRequest(file=file))
    print(f"Фото профиля обновлено на {photo_path}")
    
    # Удаляем предыдущее фото, если оно было установлено программой
    if previous_uploaded_photo:
        await client(DeletePhotosRequest(id=[previous_uploaded_photo]))  # Удаляем только предыдущее фото
        print("Предыдущее фото профиля, установленное программой, удалено.")

    # Сохраняем новое фото как предыдущее, чтобы удалить его при следующей смене
    previous_uploaded_photo = result.photo

# Запускаем клиента
with client:
    client.loop.run_until_complete(main())
