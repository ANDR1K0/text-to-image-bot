import telebot
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import image_to_string, pytesseract

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

bot_token = ''
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
        
def take_text(image):
    path = image
    img = Image.open(path)
    img = img.convert('RGBA')
    pix = img.load() 
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                pix[x, y] = (0, 0, 0, 255)
            else:
                pix[x, y] = (255, 255, 255, 255)
    im = img
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('temp2.jpg')
    text = pytesseract.image_to_string(Image.open('temp2.jpg'))
    return text

@bot.message_handler(content_types=['photo'])
def receive_photo(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = 'image.jpg'
    text =  take_text(image)
    if text == '':
        text = pytesseract.image_to_string('image.jpg')
    if text == '':
        text = "Sorry, I can't recognize that. Try another photo"
    bot.send_message(message.chat.id, text)


bot.polling()


