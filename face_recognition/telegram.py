import telebot
import os
import face_recognition
import cv2
import pickle




def create_button(text, callback_data):
    button = telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data)
    return button

def create_button_menu(title1, title2, title3, title4):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text= title1, callback_data= 'option1')
    button2 = create_button(text= title2, callback_data= 'option2')
    button3 = create_button(text= title3, callback_data= 'option3')
    button4 = create_button(text= title4, callback_data= 'option4')
    keyboard.row(button1,button2)
    keyboard.row(button3,button4)
    return keyboard

def encode_image(folder_path):
    encodings=[]

    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file andswith ((".jpg",".png",".jpeg"))]
    for image_path in image_paths:
        img = face_recognition.load_image_file(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_lock = face_recognition.face_locations(img)
        if len(face_lock) > 0:
            face_lock = face_lock[0]
            encoding = face_recognition.face_encodings(img, [face_lock])[0]
            image_name = os.path.basename(image_path)
            encodings[tuple(encoding)] = image_name
    
    data_file_encoded = "face_data_encoded/face_encoded.pickle"
    with open( data_file_encoded, "wb") as f:
        pickle.dump(encodings, f)

    print(" da ma hoa xong")



def run_telegram_processing(API_bot):
    bot = telebot.TeleBot(API_bot)

    @bot.message_handler(func = lambda, massage: True)
    def handle_message(message): 
        if "hello" or "Hello" in message.text.lower():
            bot.



    @bot.callback_query_handler()

    bot.polling(None)