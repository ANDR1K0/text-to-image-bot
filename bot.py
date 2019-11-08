import telebot
import cv2
from PIL import Image, ImageEnhance, ImageFilter
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
    else:
        bot.send_message(message.chat.id, 'Send me a photo and i will send you text from it')

def improve(imgname):
    image = cv2.imread(imgname,cv2.IMREAD_COLOR) 
    grayedimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayedimg = cv2.threshold(grayedimg, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("newim.jpg", grayedimg)

def improve_photo(image):
    improve(image)
    img = Image.open("newim.jpg")
    img = img.convert('RGBA')
    pix = img.load() 
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                pix[x, y] = (0, 0, 0, 255)
            else:
                pix[x, y] = (255, 255, 255, 255)
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1')
    img.save('improved.jpg')
     
def take_text(image):
    improve_photo(image)
    text = pytesseract.image_to_string('improved.jpg')
    if text == '':
        text = pytesseract.image_to_string('image.jpg')
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
    text =  take_text(image)
    bot.send_message(message.chat.id, text)


bot.polling()




