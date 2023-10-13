import telebot
import os
import glob

API_bot = '5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4'
user_id = 2067566824
def create_button(text, callback_data):
    button = telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data)
    return button

def create_button_menu(title1, title2, title3, title4):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = create_button(text=title1, callback_data='option1')
    button2 = create_button(text=title2, callback_data='option2')
    button3 = create_button(text=title3, callback_data='option3')
    button4 = create_button(text=title4, callback_data='option4')
    keyboard.row(button1, button2)
    keyboard.row(button3, button4)
    return keyboard

# Khởi tạo bot Telegram
bot = telebot.TeleBot(API_bot)

# Đường dẫn đến thư mục chứa ảnh
image_directory = "face_data"

# Hàm gửi tất cả các ảnh trong thư mục
def send_all_images(directory, chat_id):
    # Lấy danh sách các tệp tin ảnh trong thư mục
    image_files = glob.glob(os.path.join(directory, "*.jpg")) + glob.glob(os.path.join(directory, "*.jpeg")) + glob.glob(os.path.join(directory, "*.png"))

    # Gửi từng ảnh
    for image_file in image_files:
        with open(image_file, "rb") as f:
            # Trích xuất tên file từ đường dẫn và loại bỏ phần mở rộng
            file_name = os.path.splitext(os.path.basename(image_file))[0]
            # Gửi ảnh lên Telegram với caption không bao gồm đuôi file
            bot.send_photo(chat_id, f, caption=file_name)
# Xử lý callback khi nhấn vào button gợi ý
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "option1":
        # Gửi tất cả các ảnh trong thư mục
        send_all_images(image_directory, chat_id= user_id)

# Xử lý khi nhận tin nhắn từ người dùng
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '/menu':
        a = 'Thêm khuôn mặt'
        b = 'Lịch sử ra vào'
        c = 'Khác'
        keyboard = create_button_menu(title1=a, title2=b, title3=c, title4='')
        bot.send_message(message.chat.id, 'Mời chọn một yêu cầu:', reply_markup=keyboard)
    else:
        bot.reply_to(message, 'Tôi không hiểu ý bạn. Hãy thử lại.')

# Tiếp tục chạy bot
bot.polling(none_stop=True)



# import cv2
# import library
# import keyboard
# import time
# import datetime

# capture_active = False
# capture_count = 1

# def capture_image(url):
#     cam = cv2.VideoCapture(url)
#     ret, frame = cam.read()
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
#     cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
#     return frame

# url = 0

# while True:
#     try:
#         if keyboard.is_pressed("c") and not capture_active:
#             # Bật chế độ chụp ảnh khi nhận được tín hiệu từ nút "C"
#             capture_active = True
#             print("Bật chế độ chụp ảnh")

#             frame = capture_image(url=url)
#             file_name = f"face_input/anh_chup{capture_count}.jpg"
#             cv2.imwrite(file_name, frame)
#             print(f"Đã chụp ảnh {file_name}")
#             capture_count += 1
#             library.compare_face(image_path=file_name, file_encoding_in_folder="face_data_encoded/face_encoded.pickle")
            
#             # Ngừng ghi hình sau khi đã chụp ảnh
#             capture_active = False
#             print("Tắt chế độ chụp ảnh")
            
#             # Chờ phím "C" được nhả ra trước khi chụp ảnh tiếp theo
#             while keyboard.is_pressed("c"):
#                 pass
                
#     except Exception as e:
#         print(e)
# while True:
#     try:
#         if keyboard.is_pressed("c") and not capture_active:
#             capture_active:True
#             current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
#             print("Bật chế độ chụp ảnh")
#             frame = library.capture_image(url=url)
#             file_name = f"face_input/anh_chup{capture_count}.jpg"
#             cv2.imwrite(file_name, frame)
#             print(f"Đã chụp ảnh {file_name}")
#             capture_count += 1

#             matching_image_names, face_locations_len = library.compare_face(image_path=file_name, file_encoding_in_folder="face_data_encoded/face_encoded.pickle")
#             if matching_image_names is not None:
#                 print("Các khuôn mặt trùng khớp:")
#                 for name in matching_image_names:
#                     print(name)
#                     library.send_alert_message(bot=bot,chat_id=user_id, message=f"hom nay {name} da den")
#                 print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
#             else:
#                 if face_locations_len > 0:
#                     print("Không có khuôn mặt trùng khớp")
#                     library.send_image_to_telegram(image_path=file_name,bot= bot, user_id=user_id)
#                     library.send_open_door_prompt(bot=bot, chat_id=user_id)
#                     print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
#                 capture_active = False
#                 print("Tắt chế độ chụp ảnh")
#                 while keyboard.is_pressed("c"):
#                     pass
#     except Exception as e:
#         print(e)