import cv2
import telebot
import os
import datetime
import pickle
import glob
import face_recognition


#---------------------------------------------------------------------------------------------------------------------------------------------------------


def capture_image(url):
    cam = cv2.VideoCapture(url)
    ret, frame = cam.read()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    cv2.putText(frame, current_time,(10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)
    cam.release()
    return cam


def encode_images(folder_path,data_file ):
    # Tạo một từ điển để lưu trữ mã hóa khuôn mặt và tên bức ảnh tương ứng
    encodings = {}

    # Danh sách đường dẫn của tất cả các ảnh trong thư mục
    image_paths = [os.path.join("face_data", file) for file in os.listdir(folder_path) if file.endswith((".jpg", ".jpeg", ".png"))]

    for image_path in image_paths:
        img = face_recognition.load_image_file(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(img)
        if len(face_loc) > 0:
            face_loc = face_loc[0]
            encoding = face_recognition.face_encodings(img, [face_loc])[0]
            image_name = os.path.basename(image_path)
            encodings[tuple(encoding)] = image_name

    # Ghi từ điển mã hóa vào tệp dữ liệu
    with open(data_file, "wb") as f:
        pickle.dump(encodings, f)

    print("Ready")



def compare_face(image_path, file_encoding_in_folder):
    with open(file_encoding_in_folder, 'rb') as f:
        encodings = pickle.load(f)

    image_input = face_recognition.load_image_file(image_path)
    image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
    face_locations_input = face_recognition.face_locations(image_input)

    if len(face_locations_input) > 0:
        face_location_input = face_locations_input[0]
        encoding_face_input = face_recognition.face_encodings(image_input, [face_location_input])[0]

        matching_image_names = []
        for encoding, image_name in encodings.items():
            faceDis = face_recognition.face_distance([encoding], encoding_face_input)
            if faceDis < 0.35:
                matching_image_names.append(os.path.splitext(image_name)[0])

        if len(matching_image_names) > 0:
            return matching_image_names, len(face_locations_input)
        else:
            return None, len(face_locations_input)
    else:
        return None, 0




# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_button(text, callback_data):
    button = telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data)
    return button

def create_button_menu():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text="Thêm khuôn mặt", callback_data="menu1")
    button2 = create_button(text="Danh sách khuôn mặt", callback_data="menu2")
    button3 = create_button(text="Lịch sử ra vào", callback_data= "menu3")
    button4 = create_button(text="Khác", callback_data= "menu4")
    keyboard.row(button1, button2)
    keyboard.row(button3, button4)
    return keyboard
def create_button_menu1():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text="có", callback_data="menu1_sub1")
    button2 = create_button(text="không", callback_data="menu1_sub2")
    keyboard.row(button1, button2)
    return keyboard

def create_button_menu3():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text="Hôm nay", callback_data="menu3_sub1")
    button2 = create_button(text="Ngày khác", callback_data="menu3_sub2")
    keyboard.row(button1, button2)
    return keyboard

def create_buton_menu3_option1():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text="người lạ", callback_data="menu3_sub1_op1")
    button2 = create_button(text="người quen", callback_data="menu3_sub2_op2")
    keyboard.row(button1, button2)
    return keyboard


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download_photo(bot, photo, save_path):
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

def choose_day(bot,message):
    name = message.text
    bot.send_message(message.chat.id, 'Mời bạn chọn ngày theo dạng sau YYYY-MM-DD')
    bot.register_next_step_handler(message, name)


def handle_name(bot,message):
    name = message.text
    bot.send_message(message.chat.id, 'Vui lòng gửi ảnh của bạn.')
    bot.register_next_step_handler(message, handle_photo, name)


def handle_photo(bot,message, name):
    file_name = ""
    photo = message.photo[-1]
    if not name:
        name = photo.file_id
    file_name = f"{name}.jpg"
    save_path = "face_data/" + file_name
    download_photo(bot, photo, save_path)
    encode_images(folder_path="face_data", data_file="face_data_encoded/face_encoded.pickle")
    bot.send_message(message.chat.id, 'Đã tải xuống ảnh thành công.')


def send_image_to_telegram(bot,image_path,user_id):
    photo = open(image_path, 'rb')
    bot.send_photo(user_id, photo)

def send_open_door_prompt(bot,chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton(text='Có', callback_data='open_door_yes')
    no_button = telebot.types.InlineKeyboardButton(text='Không', callback_data='open_door_no')
    keyboard.add(yes_button, no_button)
    bot.send_message(chat_id, 'Bạn có muốn mở cửa không?', reply_markup=keyboard)



def send_alert_message(bot,chat_id, message):
    try:
        bot.send_message(chat_id, message)
        print("Đã gửi tin nhắn cảnh báo thành công")
    except Exception as e:
        print("Gửi tin nhắn cảnh báo không thành công:", str(e))


def download_photo(bot, photo, save_path):
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)



def send_all_images(folder_image, chat_id, bot):

    image_files = glob.glob(os.path.join(folder_image, "*.jpg")) + glob.glob(os.path.join(folder_image, "*.jpeg")) + glob.glob(os.path.join(folder_image, "*.png"))
    for image_file in image_files:
        with open(image_file, "rb") as f:
            file_name = os.path.splitext(os.path.basename(image_file))[0]
            bot.send_photo(chat_id, f, caption=file_name)