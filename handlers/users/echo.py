from loader import dp
from loader import bot
from data.config import BOT_TOKEN
from states.state import SomeState

TOKEN=BOT_TOKEN
import json
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram import types
import requests


# Instagram API linki
INSTAGRAM_API_URL = 'https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index'
RAPIDAPI_API_KEY = "e153a591c6msha6643ab1f726b81p16ed02jsn6695f1292a25"

async def upload_video_from_instagram(link: str, chat_id: int):
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_API_KEY,
        'X-RapidAPI-Host': 'instagram-downloader-download-instagram-videos-stories.p.rapidapi.com',
    }
    params = {
        'url': link
    }
    response = requests.get(INSTAGRAM_API_URL, headers=headers, params=params)
    json_response = json.loads(response.text)

    if 'media' in json_response:
        video_url = json_response['media']
        video_filename = 'videos/new.mp4'
        response = requests.get(video_url)

        with open(video_filename, 'wb') as f:
            f.write(response.content)

        with open(video_filename, 'rb') as f:
            await bot.send_video(chat_id, f)

    else:
        await bot.send_message(chat_id, 'Video yuklashda xatolik yuz berdi.')




# Foydalanuvchi tomonidan yuborilgan linkni qabul qilish

@dp.message_handler()
async def process_instagram_link(message: types.Message, state: FSMContext):
    # Linkni olish
    link = message.text
    await message.answer('⏬ Yuklash boshlandi ⏬')
    await upload_video_from_instagram(link, message.chat.id)
    try:
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        headers = {
            "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
            "X-RapidAPI-Host": "shazam-api6.p.rapidapi.com"
        }
        files = {"upload_file": open('videos/new.mp4', "rb")}
        response = requests.request("POST", url, headers=headers, files=files)
        import json
        if str(response.status_code)==str(200):
            res = json.loads(response.text)['result']['track']
            cap='<b>Qo\'shiq:</b> '+ res['title'] + '\n' + '<b>Artist:</b> ' + res['subtitle']
            await message.answer_photo(res['images']['background'],caption=cap,parse_mode=ParseMode.HTML)

            cdn_youtube = res['sections'][1]['youtubeurl']

            res = requests.get(cdn_youtube)
            json = json.loads(res.text)
            youtube_url = json['actions'][0]['uri'].split('?')[0]

            url = "https://t-one-youtube-converter.p.rapidapi.com/api/v1/createProcess"
            querystring = {"url": youtube_url, "format": "mp3"}
            headers = {
                "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
                "X-RapidAPI-Host": "t-one-youtube-converter.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json().get('file'):
                await message.answer_audio(response.json().get('file'))
            else:
                await message.answer('❗️ Qo\'shiq yuklanmadi qayta urinib kuring')
        else:
            await message.answer('Qo\'shiq topilmadi ❌')
    except Exception as error:
        print("Errorjon: ",error)
        await message.answer('Topip bo\'lmadi.')


@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def video_send(message: types.Message):
    await message.video.download(destination='videos/vid.mp4')
    await bot.send_message(chat_id=message.chat.id, text='Video qabul qilindi, izlash boshlandi...')
    try:
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        headers = {
            "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
            "X-RapidAPI-Host": "shazam-api6.p.rapidapi.com"
        }
        files = {"upload_file": open('videos/vid.mp4', "rb")}
        response = requests.request("POST", url, headers=headers, files=files)
        import json
        if str(response.status_code) == str(200):
            res = json.loads(response.text)['result']['track']
            cap = '<b>Qo\'shiq:</b> ' + res['title'] + '\n' + '<b>Artist:</b> ' + res['subtitle']
            await message.answer_photo(res['images']['background'], caption=cap, parse_mode=ParseMode.HTML)

            cdn_youtube = res['sections'][1]['youtubeurl']
            print(response.text)

            res = requests.get(cdn_youtube)
            json = json.loads(res.text)
            youtube_url = json['actions'][0]['uri'].split('?')[0]
            print(youtube_url)

            url = "https://t-one-youtube-converter.p.rapidapi.com/api/v1/createProcess"
            querystring = {"url": youtube_url, "format": "mp3"}
            headers = {
                "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
                "X-RapidAPI-Host": "t-one-youtube-converter.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json().get('file'):
                await message.answer_audio(response.json().get('file'))
            else:
                await message.answer('❗️ Qo\'shiq yuklanmadi qayta urinib kuring')
        else:
            await message.answer('Qo\'shiq topilmadi ❌')
    except Exception as error:
        print("Errorjon: ",error)
        await message.answer('Topip bo\'lmadi.')

@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def voise_send(message: types.Message):
    await message.voice.download(destination='videos/voise.mp3')
    await bot.send_message(chat_id=message.chat.id, text='Audio qabul qilindi, izlash boshlandi...')
    try:
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        headers = {
            "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
            "X-RapidAPI-Host": "shazam-api6.p.rapidapi.com"
        }
        files = {"upload_file": open('videos/voise.mp3', "rb")}
        response = requests.request("POST", url, headers=headers, files=files)
        import json
        if str(response.status_code) == str(200):
            res = json.loads(response.text)['result']['track']
            cap = '<b>Qo\'shiq:</b> ' + res['title'] + '\n' + '<b>Artist:</b> ' + res['subtitle']
            await message.answer_photo(res['images']['background'], caption=cap, parse_mode=ParseMode.HTML)

            cdn_youtube = res['sections'][1]['youtubeurl']

            res = requests.get(cdn_youtube)
            json = json.loads(res.text)
            youtube_url = json['actions'][0]['uri'].split('?')[0]

            url = "https://t-one-youtube-converter.p.rapidapi.com/api/v1/createProcess"
            querystring = {"url": youtube_url, "format": "mp3"}
            headers = {
                "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
                "X-RapidAPI-Host": "t-one-youtube-converter.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json().get('file'):
                await message.answer_audio(response.json().get('file'))
            else:
                await message.answer('❗️ Qo\'shiq yuklanmadi qayta urinib kuring')
        else:
            await message.answer('Qo\'shiq topilmadi ❌')
    except Exception as error:
        print("Errorjon: ",error)
        await message.answer('Topip bo\'lmadi.')

@dp.message_handler(content_types=types.ContentTypes.AUDIO)
async def audio_send(message: types.Message):
    await message.audio.download(destination='videos/audio.mp3')
    await bot.send_message(chat_id=message.chat.id, text='Audio qabul qilindi, izlash boshlandi...')
    try:
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        headers = {
            "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
            "X-RapidAPI-Host": "shazam-api6.p.rapidapi.com"
        }
        files = {"upload_file": open('videos/audio.mp3', "rb")}
        response = requests.request("POST", url, headers=headers, files=files)
        import json
        if str(response.status_code) == str(200):
            res = json.loads(response.text)['result']['track']
            cap = '<b>Qo\'shiq:</b> ' + res['title'] + '\n' + '<b>Artist:</b> ' + res['subtitle']
            await message.answer_photo(res['images']['background'], caption=cap, parse_mode=ParseMode.HTML)

            cdn_youtube = res['sections'][1]['youtubeurl']

            res = requests.get(cdn_youtube)
            json = json.loads(res.text)
            youtube_url = json['actions'][0]['uri'].split('?')[0]

            url = "https://t-one-youtube-converter.p.rapidapi.com/api/v1/createProcess"
            querystring = {"url": youtube_url, "format": "mp3"}
            headers = {
                "X-RapidAPI-Key": "0e377137camsh447b37d006e9f6ap1a7bf2jsnd42ba89ecfdc",
                "X-RapidAPI-Host": "t-one-youtube-converter.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.json().get('file'):
                await message.answer_audio(response.json().get('file'))
            else:
                await message.answer('❗️ Qo\'shiq yuklanmadi qayta urinib kuring')
        else:
            await message.answer('Qo\'shiq topilmadi ❌')
    except Exception as error:
        print("Errorjon: ",error)
        await message.answer('Topip bo\'lmadi.')




