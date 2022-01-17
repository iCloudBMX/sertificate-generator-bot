import telebot
from config.settings import BOT_TOKEN
from PIL import Image, ImageDraw, ImageFont
import qrcode

from django.core.exceptions import ObjectDoesNotExist

from .models import BotUser, RegisteredUser
from telegram_bot import step, excel_reader
import os

from pathlib import Path

bot = telebot.TeleBot(BOT_TOKEN)

class BotController:
    def __init__(self, message):
        self.message = message
        self.chat_id = message.from_user.id
        self.user, _ = BotUser.objects.get_or_create(chat_id=self.chat_id)
        self.message_id = message.message_id if hasattr(message, "message_id") else message.message.message_id

    def start(self):
        bot.send_message(self.chat_id, "<text for user>", parse_mode='html')
        self.set_step(step.ZERO)

    def send_existing_sertificate(self):
        bot.send_photo(self.chat_id, self.user.file_id)

    def generate_sertificate(self):
        bot.send_message(self.chat_id, "Foyalanuvchi tekshirilmoqda...")
        if self.user.file_id != None and self.user.file_id != "":
            bot.send_message(self.chat_id, "Tayyorlanmoqda...")
            return self.send_existing_sertificate()

        user = RegisteredUser.objects.filter(email=self.message.text).first()
        
        if user is None:
            return self.email_not_registered()

        bot.send_message(self.chat_id, "Tayyorlanmoqda...")

        path = user.name

        self.save_image(path)

        file = bot.send_photo(chat_id=self.chat_id, photo=open(f'{path}.png', 'rb'))

        os.remove(f'{path}.png')

        self.user.file_id = file.photo[0].file_id
        
        self.user.save()

    def save_image(self, name):
        image = Image.open('<image file path>')

        draw = ImageDraw.Draw(image)
        
        font = ImageFont.truetype('<font style path>', 130)
        
        draw.text(((220, 1800)), name, (255, 255, 255), font=font)

        qr_code = qrcode.QRCode(box_size=20)
        
        qr_code.add_data('<qr code link>')
        
        qr_code.make()   
        
        img_qr = qr_code.make_image()

        pos = (image.size[0] - img_qr.size[0], image.size[1] - img_qr.size[1])

        image.paste(img_qr, pos)

        image.save("{}.png".format(name))        

    def email_not_registered(self):
        bot.send_message(self.chat_id, "<text for user>")

    def change_database(self):
        excel_reader.locate_users()
        bot.send_message(self.chat_id, "Changed")

    def set_step(self, step):
        self.user.step = step
        self.user.save()   

    