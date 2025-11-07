import tkinter as tk
from tkinter import messagebox
import os
import sys

# ฟังก์ชันสำหรับจัดการเมื่อผู้ใช้กดปุ่ม 'Sign Up' (ลงทะเบียนใบหน้า)
def handle_sign_up():
    """
    ฟังก์ชันสำหรับเปิดหน้าต่างหรือเริ่มกระบวนการลงทะเบียนใบหน้าใหม่
    คุณสามารถเพิ่มโค้ดเพื่อเปิดหน้าต่าง Tkinter ใหม่สำหรับลงทะเบียนได้ที่นี่
    """
    print("--- ลงทะเบียนใบหน้าถูกเลือก ---")
    messagebox.showinfo("ลงทะเบียน", "ฟังก์ชันลงทะเบียนยังไม่ถูกพัฒนา กรุณาเพิ่มโค้ดลงทะเบียนที่นี่")
    # ตัวอย่าง: หากคุณต้องการเรียกใช้สคริปต์ลงทะเบียน:
    # root.destroy()
    # os.system("python registration_script.py")

# ฟังก์ชันสำหรับจัดการเมื่อผู้ใช้กดปุ่ม 'Sign In' (เข้าสู่ระบบ)
def handle_sign_in():
    """
    ฟังก์ชันสำหรับปิดหน้าต่าง GUI และเรียกใช้สคริปต์หลัก (main.py)
    """
    print("--- เข้าสู่ระบบถูกเลือก ---")
    
    # 1. ปิดหน้าต่าง Tkinter ก่อน เพื่อไม่ให้ GUI ค้างเมื่อเปิดกล้อง
    root.destroy()
    
    # 2. เรียกใช้สคริปต์ main.py โดยใช้ subprocess หรือ os.system
    # ตรวจสอบให้แน่ใจว่า main.py อยู่ในไดเร็กทอรีเดียวกัน
    
    # ใช้ os.system เพื่อเรียกใช้สคริปต์ภายนอก
    try:
        # ตรวจสอบว่าระบบปฏิบัติการปัจจุบันคืออะไร (Windows/Linux/macOS)
        if sys.platform.startswith('win'):
            command = 'python main.py'
        else:
            command = 'python3 main.py'

        print(f"กำลังรันคำสั่ง: {command}")
        # คำสั่งนี้จะทำงานในเชลล์และรัน main.py
        os.system(command)
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการรัน main.py: {e}")


# --- การตั้งค่าหน้าต่าง GUI หลัก ---
root = tk.Tk()
root.title("ระบบเข้าออกด้วยใบหน้า (Face Attendance System)")
root.geometry("450x300")
root.resizable(False, False)

# ปรับปรุงสไตล์ให้ดูดีขึ้นเล็กน้อย
font_style = ('Helvetica', 12)
button_style = {'font': font_style, 'bg': '#4CAF50', 'fg': 'white', 'activebackground': '#45a049', 'width': 30, 'height': 2, 'bd': 0, 'relief': 'flat'}
frame_style = {'padx': 15, 'pady': 15}

# เฟรมหลักสำหรับการจัดกึ่งกลาง
main_frame = tk.Frame(root, **frame_style)
main_frame.pack(expand=True)

# ป้ายข้อความต้อนรับ
welcome_label = tk.Label(main_frame, text="ยินดีต้อนรับสู่ระบบเข้าออก", font=('Helvetica', 16, 'bold'), fg='#333333')
welcome_label.pack(pady=(10, 20))

# ปุ่ม Sign Up (ลงทะเบียน)
signup_button = tk.Button(main_frame, text="ลงทะเบียนใบหน้า (Sign Up)", command=handle_sign_up, **button_style)
signup_button.pack(pady=10)

# เปลี่ยนสีปุ่ม Sign In
signin_button_style = button_style.copy()
signin_button_style['bg'] = '#2196F3'
signin_button_style['activebackground'] = '#1e88e5'

# ปุ่ม Sign In (เข้าสู่ระบบ/เริ่มการตรวจจับ)
signin_button = tk.Button(main_frame, text="เข้าสู่ระบบ (Start Attendance)", command=handle_sign_in, **signin_button_style)
signin_button.pack(pady=10)

# เริ่ม Tkinter main loop
root.mainloop()