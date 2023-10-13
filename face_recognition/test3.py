import os
import datetime

# Đường dẫn tới thư mục chứa các folder theo ngày
folder_path = "history"

# Tạo tên thư mục theo ngày
date_folder = datetime.datetime.now().strftime("%Y-%m-%d")

# Đường dẫn đến thư mục theo ngày
date_folder_path = os.path.join(folder_path, date_folder)

# Tạo thư mục theo ngày nếu chưa tồn tại
if not os.path.exists(date_folder_path):
    os.makedirs(date_folder_path)

# Tạo thư mục "nguoi_quen" và "nguoi_la" trong thư mục theo ngày
nguoi_quen_folder = os.path.join(date_folder_path, "nguoi_quen")
nguoi_la_folder = os.path.join(date_folder_path, "nguoi_la")

# Tạo thư mục "nguoi_quen" nếu chưa tồn tại
if not os.path.exists(nguoi_quen_folder):
    os.makedirs(nguoi_quen_folder)

# Tạo thư mục "nguoi_la" nếu chưa tồn tại
if not os.path.exists(nguoi_la_folder):
    os.makedirs(nguoi_la_folder)
