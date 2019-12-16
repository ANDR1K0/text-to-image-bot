import telebot
import cv2
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import image_to_string, pytesseract

bot_token = '855417336:AAFcgumGuhrJlqgyNyc0YFa4s7J_jCLCspQ'
bot = telebot.TeleBot(bot_token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard1.row('What has happenned?')
LANGUAGE = 'eng'
keyboard2 = telebot.types.InlineKeyboardMarkup()
for lang in [('Ukrainian', 'ukr'), ('English', 'eng'), ('Japanese','jpn'), ('Hindi','hin')]:
    keyboard2.add(telebot.types.InlineKeyboardButton(text=lang[0], callback_data=lang[1]))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Hi! I can extract text from the photos you send me!', reply_markup=keyboard1)

@bot.message_handler(commands=['changelang'])
def send_text(message):
    bot.send_message(message.chat.id, text='Choose language', reply_markup=keyboard2)

@bot.callback_query_handler(func=lambda c:True)
def ans(c):
    cid = c.message.chat.id
    keyboard2 = telebot.types.InlineKeyboardMarkup()
    global LANGUAGE
    LANGUAGE = c.data
    bot.send_message(cid, 'You have changed the language! Your lang is now: ' + c.data)
    
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'Hello, send me a photo and i will send you text from it')
    elif message.text.lower() == 'bye':
        bot.send_message(message.chat.id, 'Good luck!)')
    elif message.text == 'What has happenned?':
        bot.send_message(message.chat.id, 'Last time i was sent this photo:')
        bot.send_photo(message.chat.id, open('image.jpg', 'rb'))
        bot.send_message(message.chat.id, 'I made it look like this:')
        bot.send_photo(message.chat.id, open('improved.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Then i used Tesseract-OCR to extract text from it. The text is:')
        text = take_text('improved.jpg')
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Send me a photo and i will send you text from it')
        
def monochrome(image):
    image = cv2.imread(image,cv2.IMREAD_COLOR) 
    grayed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayed_image = cv2.threshold(grayed_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('improved.jpg', grayed_image)

def clean_image(image):
    monochrome(image)
    img = Image.open('improved.jpg')
    img = img.convert('RGBA')
    pix = img.load() 
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                pix[x, y] = (0, 0, 0, 255)
            else:
                pix[x, y] = (255, 255, 255, 255)
    img = img.filter(ImageFilter.MedianFilter())
    enhancer1 = ImageEnhance.Contrast(img)
    img = enhancer1.enhance(2)
    enhancer2 = ImageEnhance.Sharpness(img)
    img = enhancer2.enhance(2)
    img = img.convert('1')
    img.save('improved.jpg')

def take_text(image):
    clean_image(image)
    text = pytesseract.image_to_string('improved.jpg', lang=LANGUAGE)
    if text == '':
        text = pytesseract.image_to_string('image.jpg',lang=LANGUAGE)
    if text == '':
        text = "Sorry, I can't recognize that. Try another photo"
    return text

@bot.message_handler(content_types=['photo'])
def receive_photo(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = 'image.jpg'
    text = take_text(image)
    bot.send_message(message.chat.id, text)


bot.polling()

