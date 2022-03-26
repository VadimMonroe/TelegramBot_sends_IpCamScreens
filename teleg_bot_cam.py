#!/Users/vadimmonroe/Desktop/Programming/_WORK_PROJECTS/8_telegram_bot_cam/venv/bin/python3.9

import os

from settings import *
from telebot import TeleBot, types
from cv2 import VideoCapture, imwrite


def show_must_go_on() -> None:
    bot = TeleBot(token=TELEGRAM_BOT_TOKEN)

    cameras = [f'rtsp://{ip_cam[0]}:554/user={login}&password={password}&channel={_}&stream=0.sdp' for _ in range(1, 5)]
    cameras.append(f'rtsp://{ip_cam[1]}:554/user={login}&password={password}&channel=1&stream=0.sdp')
    list_cam = [VideoCapture(_) for _ in cameras]
    list_of_imgs = []
    for num, cam in enumerate(list_cam):
        _, img = list_cam[num].read()
        path = f'file{num}.jpg'
        imwrite(path, img)
        list_of_imgs.append(types.InputMediaPhoto(open(path, 'rb')))
        os.remove(path)
    bot.send_media_group(chat_id=TELEGRAM_CHAT_ID, media=list_of_imgs, disable_notification=True)


if __name__ == '__main__':
    show_must_go_on()
