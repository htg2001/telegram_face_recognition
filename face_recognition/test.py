# import telebot

# bot = telebot.TeleBot('5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4')

# @bot.message_handler(commands=['start'])
# def start(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button1 = telebot.types.InlineKeyboardButton(text='Button 1', callback_data='btn1')
#     button2 = telebot.types.InlineKeyboardButton(text='Button 2', callback_data='btn2')
#     button3 = telebot.types.InlineKeyboardButton(text='Button 3', callback_data='btn3')
#     button4 = telebot.types.InlineKeyboardButton(text='Button 4', callback_data='btn4')
#     keyboard.row(button1, button2)
#     keyboard.row(button3, button4)
#     bot.send_message(message.chat.id, 'Chọn một button:', reply_markup=keyboard)

# bot.polling()


# import telebot

# # Khởi tạo đối tượng bot
# bot = telebot.TeleBot('5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4')

# # Đăng ký hàm xử lý tin nhắn
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     # Xử lý tin nhắn
#     chat_id = message.chat.id
#     text = message.text

#     # Gửi tin nhắn phản hồi mà không hiển thị đoạn chat gốc
#     bot.reply_to(message, "Xin chào từ bot Telegram!")

# # Khởi động bot
# bot.polling()


# import os
# import cv2
# import face_recognition
# import pickle

# def encode_images(folder_path, data_file):
#     # Tạo một từ điển để lưu trữ mã hóa khuôn mặt và tên bức ảnh tương ứng
#     encodings = {}

#     # Danh sách đường dẫn của tất cả các ảnh trong thư mục
#     image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith((".jpg", ".jpeg", ".png"))]

#     for image_path in image_paths:
#         img = face_recognition.load_image_file(image_path)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         face_loc = face_recognition.face_locations(img)
#         if len(face_loc) > 0:
#             face_loc = face_loc[0]
#             encoding = face_recognition.face_encodings(img, [face_loc])[0]
#             image_name = os.path.basename(image_path)
#             encodings[tuple(encoding)] = image_name

#     # Ghi từ điển mã hóa vào tệp dữ liệu
#     with open(data_file, "wb") as f:
#         pickle.dump(encodings, f)

#     print("Ready")

# # Sử dụng hàm encode_images để mã hóa ảnh và tên ảnh vào tệp pickle
# folder_path = "face_data"
# data_file = "face_data_encoded/face_encoded.pickle"

# encode_images(folder_path, data_file)




# import face_recognition
# import cv2
# import pickle
# import os

# def compare_face(image_path, file_encoding_in_folder):
#     with open(file_encoding_in_folder, 'rb') as f:
#         encodings = pickle.load(f)

#     image_input = face_recognition.load_image_file(image_path)
#     image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
#     face_locations_input = face_recognition.face_locations(image_input)
    
#     if len(face_locations_input) > 0:
#         face_location_input = face_locations_input[0]
#         encoding_face_input = face_recognition.face_encodings(image_input, [face_location_input])[0]

#         isMatch = False
#         matching_image_name = None
#         for encoding, image_name in encodings.items():
#             faceDis = face_recognition.face_distance([encoding], encoding_face_input)
#             if faceDis < 0.35:
#                 isMatch = True
#                 matching_image_name = os.path.splitext(image_name)[0]  # Lấy tên tệp không có phần mở rộng
#                 break

#         if isMatch:
#             print("yes")
#             # Hiển thị tên bức ảnh
#             if matching_image_name:
#                 print("Matching image name:", matching_image_name)
#             else:
#                 print("No matching image name found.")

#         else:
#             print("no")
#             # send_image_to_telegram(image_path)
#             # send_open_door_prompt(user_id)

#     else:
#         print("no face")

# compare_face(image_path="face_input/thuy.jpg",file_encoding_in_folder="face_data_encoded/face_encoded.pickle")




# import cv2

# def capture_image():
#     cap = cv2.VideoCapture(0)  # Chọn thiết bị camera, 0 là camera mặc định

#     while True:
#         ret, frame = cap.read()  # Đọc frame từ camera

#         cv2.imshow('Camera', frame)  # Hiển thị frame lên cửa sổ

#         if cv2.waitKey(1) == ord('c'):  # Chờ người dùng nhấn phím 'c'
#             cv2.imwrite('face_input/captured_image.jpg', frame)  # Lưu hình ảnh đã chụp
#             break

#     cap.release()  # Giải phóng thiết bị camera
#     cv2.destroyAllWindows()  # Đóng cửa sổ

# # Gọi hàm capture_image khi nhấn phím 'c'
# if __name__ == '__main__':
#     capture_image()


# import telebot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# bot = telebot.TeleBot('5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4')

# @bot.message_handler(commands=['start'])
# def start(message):
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton(text='Button 1', callback_data='button1')
#     keyboard.add(button)
    
#     bot.send_message(message.chat.id, 'Hello!', reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: True)
# def handle_button_click(call):
#     if call.data == 'button1':
#         # Xử lý logic khi người dùng nhấn vào Button 1
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id) # Ẩn nút sau khi người dùng nhấn vào nó
#         bot.send_message(call.message.chat.id, 'ban da chon button 1')
# bot.polling()


# import os
# import face_recognition
# import cv2
# import pickle
# import telebot
# import library

# API_bot = '5849637989:AAFHdCl6-3gd1rqoqUaye4OwyiF7mzhU0b4'
# bot = telebot.TeleBot(API_bot)
# user_id = 2067566824
# def send_alert_message(bot,chat_id, message):
#     try:
#         bot.send_message(chat_id, message)
#         print("Đã gửi tin nhắn cảnh báo thành công")
#     except Exception as e:
#         print("Gửi tin nhắn cảnh báo không thành công:", str(e))

# def compare_face(image_path, file_encoding_in_folder):
#     with open(file_encoding_in_folder, 'rb') as f:
#         encodings = pickle.load(f)

#     image_input = face_recognition.load_image_file(image_path)
#     image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
#     face_locations_input = face_recognition.face_locations(image_input)

#     if len(face_locations_input) > 0:
#         face_location_input = face_locations_input[0]
#         encoding_face_input = face_recognition.face_encodings(image_input, [face_location_input])[0]

#         matching_image_names = []
#         for encoding, image_name in encodings.items():
#             faceDis = face_recognition.face_distance([encoding], encoding_face_input)
#             if faceDis < 0.35:
#                 matching_image_names.append(os.path.splitext(image_name)[0])

#         if len(matching_image_names) > 0:
#             return matching_image_names, len(face_locations_input)
#         else:
#             return None, len(face_locations_input)
#     else:
#         return None, 0

# matching_image_names, face_locations_len = compare_face(image_path="face_input/giang.jpg", file_encoding_in_folder="face_data_encoded/face_encoded.pickle")

# if matching_image_names is not None:
#     print("Các khuôn mặt trùng khớp:")
#     for name in matching_image_names:
#         print(name)
#     send_alert_message(bot=bot,chat_id=user_id, message=f"hom nay {name} da den luc ")  
#     print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
# else:
#     if face_locations_len > 0:
#         print("Không có khuôn mặt trùng khớp")
#         library.send_image_to_telegram(image_path="face_input/giang.jpg",bot= bot, user_id=user_id)
#         library.send_open_door_prompt(bot=bot, chat_id=user_id)
#         print("Số lượng khuôn mặt tìm thấy:", face_locations_len)
#     else:
#         print("Không tìm thấy khuôn mặt trong hình ảnh")
