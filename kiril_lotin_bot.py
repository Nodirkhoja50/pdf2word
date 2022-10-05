import telebot
import PyPDF2
import pdf2docx
import textract
from telebot import types
from docx import Document

from transliterate import to_latin,to_cyrillic
TOKEN = "5658176485:AAGcoMV9XovJ8rMiC5-VZpg7GgjHRVRyKec"
bot = telebot.TeleBot(TOKEN,parse_mode = "HTML")
tb = telebot.TeleBot(TOKEN)

convert_to_ = True

def _count_user_(id):
    result = True
    with open("users_id.txt",'r') as user_id:
        for line in user_id:
            if line.strip() == id:
                result = False
        with open("users_id.txt", 'a') as user_id:
            if result:
                user_id.write(str(id)+"\n")


def converter(msg):
    ans = lambda msg: to_cyrillic(msg) if msg.isascii() else to_latin(msg)
    return ans(msg)

#START SENDING DOCUMENT
def _send_Document_to_cy_la(message):
    document = Document()
    #it takes file id
    document_id = message.document.file_id

    #file_info gives information about file like:file_size,file_path
    file_info = tb.get_file(document_id)

    #bot.download_file downloads file from client from file_path
    downloaded_file = bot.download_file(file_info.file_path)

    #src is path where file is located
    #message.document.file_name is file name user is sending
    src = 'D:/python/kiril_lotin' + message.document.file_name



    with open(src,'wb') as new_file:
        new_file.write(downloaded_file)

    #convert doc file to text
    text = textract.process(src).decode('utf-8')

    is_isascii = text[:1] #takes first alpabet of text

    #first it chakes it isascii or not
    #then it convert to_cyrillic or to_latin
    ans = lambda text1:to_cyrillic(text1) if is_isascii.isascii() else to_latin(text1)

    #wirte text file to doc file
    paragraph = document.add_paragraph(ans(text))

    #save doc file with its name
    document.save('D:/python/kiril_lotin/ibots.docx')

    with open('D:/python/kiril_lotin/ibots.docx', "rb") as file:
        f = file.read()

    #send document to clients id
    bot.send_document(message.chat.id,f)
#END OF SEND DOCUMENT

def convert_pdf_docx(message):

    #it takes file id
    document_id = message.document.file_id

    #file_info gives information about file like:file_size,file_path
    file_info = tb.get_file(document_id)

    #bot.download_file downloads file from client from file_path
    downloaded_file = bot.download_file(file_info.file_path)
    #src is path where file is located
    #message.document.file_name is file name user is sending
    src = 'D:/python/kiril_lotin' + message.document.file_name

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    FILE_PATH = src

    with open(FILE_PATH, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)

        page = reader.getPage(0)

        print(page.extractText())


    pdf_file = src
    docx_file = "C:\\Users\\asus\\Desktop\\pythonProject3\\filenamedoc.docx"
    pdf2docx.parse(pdf_file, docx_file, start=0, end=None)

    with open("C:\\Users\\asus\\Desktop\\pythonProject3\\filenamedoc.docx", "rb") as file:
        f = file.read()

    #send document to clients id
    bot.send_document(message.chat.id,f,visible_file_name="@lotin_kiril_boti_bot")


@bot.message_handler(commands=['start'])
def send_welcome(message):

    _count_user_(str(message.from_user.id))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("PDF ➡ DOCX")
    btn1 = types.KeyboardButton("Cencel")
    markup.add(btn,btn1)
    bot.send_message(message.chat.id,text="assalomu aleykum <b>{0.first_name}</b>".format(message.from_user),reply_markup=markup)
    bot.send_message(message.chat.id,text="BU BOT:\n\nPDF ➡ DOCX\n\nlotin ➡ kiril\n\nkiril ➡ lotin\n\nDocx faylni yozuvlarini kirilchadan ➡ lotinchaga,lotinchadan ➡ kirilchaga")
@bot.message_handler(func=lambda message: True)
def echo_all(message):


    global convert_to_
    msg = message.text
    if str(msg) != "PDF ➡ DOCX" and str(msg) != "Cencel":
        bot.reply_to(message,"<code>"+converter(msg)+"</code>")

    elif str(msg) == "Cencel":
        convert_to_ = True
        bot.send_message(message.chat.id, text="Endi word(docx ) yoki so'z fayl jonatishingiz mumkin")

    else:
        bot.send_message(message.chat.id, text="BOT FAYLDI KUTYAPTI!")
        convert_to_ = False


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):

    if convert_to_:
        try:
            _send_Document_to_cy_la(message)
        except:
            bot.send_message(message.chat.id, text="PDF ➡ DOCX shu tugmani bosing va qayta urinb ko'ring")
    else:
        try:
            convert_pdf_docx(message)
        except:
            bot.send_message(message.chat.id, text="Cancel tugmasini bosing va qayta urinib koring")



bot.polling(none_stop=True)