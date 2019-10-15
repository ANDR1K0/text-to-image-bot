import telebot
from PIL import Image
from pytesseract import image_to_string, pytesseract

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

bot_token = '855417336:AAFcgumGuhrJlqgyNyc0YFa4s7J_jCLCspQ'
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hi, send me a photo!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'Hello, send me a photo and i will send you text from it')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, 'Good luck!')

        
def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    image.save(newFilePath)
    return image


@bot.message_handler(content_types=['photo'])
def receive_photo(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = cleanFile('image.jpg', 'cleaned_image.jpg')
    #bot.send_photo(message.chat.id, photo=open("image.jpg", 'rb'))
    text = image_to_string(image, lang='eng')
    bot.send_message(message.chat.id, text)


bot.polling()

