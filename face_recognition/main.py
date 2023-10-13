import library
import threading
import telebot
import cv2
import datetime
import os
from pynput import keyboard
API_bot = '5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4'
bot = telebot.TeleBot(API_bot)
url = 0
user_id = 2067566824


def capture_image(url):
    cam = cv2.VideoCapture(url)
    ret, frame = cam.read()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    return frame

def run_face_processing():
    capture_active = False
    capture_count = 1

    def on_key_press(key):
        nonlocal capture_active, capture_count

        if key == keyboard.KeyCode.from_char('c') and not capture_active:
            capture_active = True
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
            print("Bật chế độ chụp ảnh")
            frame = capture_image(url=url)
            file_name = f"face_input/anh_chup{capture_count}.jpg"
            cv2.imwrite(file_name, frame)
            print(f"Đã chụp ảnh {file_name}")
            capture_count += 1
            #tao thu muc tu dong
            folder_path = "history"
            date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
            date_folder_path = os.path.join(folder_path, date_folder)
            if not os.path.exists(date_folder_path):
                os.makedirs(date_folder_path)

            matching_image_names, face_locations_len = library.compare_face(image_path=file_name, file_encoding_in_folder="face_data_encoded/face_encoded.pickle")
            if matching_image_names is not None:
                print("Các khuôn mặt trùng khớp:")
                for name in matching_image_names:
                    print(name)
                    #tao thu muc nguoi quen
                    nguoi_quen_folder = os.path.join(date_folder_path, "nguoi_quen")
                    if not os.path.exists(nguoi_quen_folder):
                        os.makedirs(nguoi_quen_folder)
                    file_path = os.path.join(nguoi_quen_folder, f"anh_chup_thu_la_{name}.jpg")
                    cv2.imwrite(file_path, frame)
                    #
                    # library.send_alert_message(bot=bot, chat_id=user_id, message=f" Hôm nay {name} đã đến lúc {current_time}")
                print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
            else:
                if face_locations_len > 0:
                    print("Không có khuôn mặt trùng khớp")
                    library.send_image_to_telegram(image_path=file_name, bot=bot, user_id=user_id)
                    library.send_open_door_prompt(bot=bot, chat_id=user_id)
                    #thu muc nguoi la
                    nguoi_la_folder = os.path.join(date_folder_path, "nguoi_la")
                    if not os.path.exists(nguoi_la_folder):
                        os.makedirs(nguoi_la_folder)
                    file_path = os.path.join(nguoi_la_folder, f"anh_chup_nguoi_la_luc{current_time}.jpg")
                    cv2.imwrite(file_path, frame)
                    print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
            
            capture_active = False
            print("Tắt chế độ chụp ảnh")

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()
    listener.join()


def run_telegram_processing():
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        if 'hello' in message.text.lower():
            bot.reply_to(message, 'Xin chào!')
        elif message.text == '/start':
            bot.reply_to(message, 'Chào mừng bạn đến với dịch vụ của tôi')
        elif message.text == '/menu':
            keyboard=library.create_button_menu()
            bot.send_message(message.chat.id, 'Mời chọn một yêu cầu:', reply_markup=keyboard)
        else:
            bot.reply_to(message, 'Tôi không hiểu ý bạn. Hãy thử lại.')   
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data == "menu1":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            keyboard1 = library.create_button_menu1()
            bot.send_message(call.message.chat.id, 'Bạn đã chắc chắn?', reply_markup=keyboard1)
        elif call.data =="menu1_sub1":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Mời nhập tên của anh:')
            bot.register_next_step_handler(call.message, handle_name)
        elif call.data =="menu1_sub2":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Bạn đã hủy')
        elif call.data == "menu2":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Vui lòng đợi')
            library.send_all_images(bot=bot,folder_image="face_data",chat_id=user_id)
            bot.send_message(call.message.chat.id, 'Đã tải xong')
        elif call.data == "menu3":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            keyboard3 = library.create_button_menu3()
            bot.send_message(call.message.chat.id, 'Mời bạn chọn ngày', reply_markup=keyboard3)
        elif call.data == "menu3_sub1":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            keyboard4 = library.create_buton_menu3_option1()
            bot.send_message(call.message.chat.id, 'Người lạ hay người quen', reply_markup=keyboard4)
        elif call.data =="menu3_sub1_op1":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Vui lòng đợi')
            date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
            nguoi_la_folder = os.path.join("history", date_folder, "nguoi_la")
            library.send_all_images(bot=bot,folder_image=nguoi_la_folder,chat_id=user_id)
        elif call.data =="menu3_sub1_op2":
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Vui lòng đợi')

            date_folder = choose_day()
            nguoi_la_folder = os.path.join("history", date_folder, "nguoi_la")
            library.send_all_images(bot=bot,folder_image=nguoi_la_folder,chat_id=user_id)

        

        elif call.data == "open_door_yes":
            print("mo cua trong 5s")
            bot.send_message(call.message.chat.id, 'Đã mở cửa')
        elif call.data == "open_door_no":
            print("khong mo cua")
            bot.send_message(call.message.chat.id, 'Đã khóa cửa')
    
    
    def handle_name(message):
        name = message.text
        bot.send_message(message.chat.id, 'Vui lòng gửi ảnh của bạn.')
        bot.register_next_step_handler(message, handle_photo, name)

    def handle_photo(message, name):
        file_name = ""
        photo = message.photo[-1]
        if not name:
            name = photo.file_id
        file_name = f"{name}.jpg"
        save_path = "face_data/" + file_name
        library.download_photo(bot, photo, save_path)
        library.encode_images(folder_path="face_data", data_file="face_data_encoded/face_encoded.pickle")
        bot.send_message(message.chat.id, 'Đã tải xuống ảnh thành công.')


def bot_polling():
    bot.polling(none_stop = True)

theard1 = threading.Thread(target=run_face_processing)
theard2 = threading.Thread(target=run_telegram_processing)
theard3 = threading.Thread(target=bot_polling)

theard1.start()
theard2.start()
theard3.start()



