import tkinter as tk
from tkinter import messagebox
import os
import sys


# --- ฟังก์ชันควบคุม (Handlers) ---

def handle_sign_up():
    """
    ฟังก์ชันสำหรับเปิดหน้าต่างหรือเริ่มกระบวนการลงทะเบียนใบหน้าใหม่
    """
    print("--- ลงทะเบียนใบหน้าถูกเลือก ---")


    # messagebox.showinfo(
    #     "ลงทะเบียน (Sign Up)",
    #     "ฟังก์ชันลงทะเบียนยังไม่ถูกพัฒนา\n(Registration function is not yet implemented)"
    # )
    # หากต้องการเรียกสคริปต์อื่น:
    # root.destroy()
    # os.system("python registration_script.py")


def handle_sign_in():
    """
    ฟังก์ชันสำหรับปิดหน้าต่าง GUI และเรียกใช้สคริปต์หลัก (main.py)
    """
    print("--- เข้าสู่ระบบถูกเลือก ---")

    # 1. ปิดหน้าต่าง Tkinter ก่อน
    try:
        root.destroy()
    except tk.TclError:
        # อาจเกิดข้อผิดพลาดหากหน้าต่างถูกปิดไปแล้ว
        pass

    # 2. เรียกใช้สคริปต์ main.py
    try:
        # ตรวจสอบระบบปฏิบัติการเพื่อใช้คำสั่ง python ที่ถูกต้อง
        command = 'python3 main.py' if sys.platform != 'win32' else 'python main.py'

        print(f"กำลังรันคำสั่ง: {command}")
        os.system(command)

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการรัน main.py: {e}")
        # ในแอปจริง ควรแสดงข้อผิดพลาดนี้ใน GUI
        # messagebox.showerror("Error", f"Failed to run main.py: {e}")


# --- การตั้งค่า GUI หลัก ---

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ระบบเช็คชื่อด้วยใบหน้า (Face Attendance System)")
root.geometry("500x350")  # ขยายขนาดเล็กน้อยเพื่อพื้นที่ว่าง
root.resizable(False, False)
root.configure(bg='#f0f0f0')  # ตั้งค่าสีพื้นหลังหลัก

# --- การตั้งค่าสไตล์ (Styles) ---
WINDOW_BG = '#f0f0f0'
TEXT_COLOR = '#333333'
FONT_LARGE = ('Helvetica', 18, 'bold')
FONT_MEDIUM = ('Helvetica', 12)
FONT_BUTTON = ('Helvetica', 12, 'bold')

# สไตล์ปุ่ม Sign Up
BTN_REGISTER_BG = '#4CAF50'
BTN_REGISTER_FG = '#ffffff'
BTN_REGISTER_ACTIVE_BG = '#45a049'
BTN_REGISTER_ACTIVE_FG = '#ffffff'  # **สำคัญ: แก้ไขปัญหาสีจางบน Mac**

# สไตล์ปุ่ม Sign In
BTN_SIGNIN_BG = '#2196F3'
BTN_SIGNIN_FG = '#ffffff'
BTN_SIGNIN_ACTIVE_BG = '#1e88e5'
BTN_SIGNIN_ACTIVE_FG = '#ffffff'  # **สำคัญ: แก้ไขปัญหาสีจางบน Mac**

# --- การจัดวางองค์ประกอบ (Layout) ---

# ใช้ Frame หลักเพื่อให้มี padding รอบขอบ
main_frame = tk.Frame(root, bg=WINDOW_BG, padx=30, pady=30)
main_frame.pack(expand=True, fill='both')

# ป้ายข้อความต้อนรับ
welcome_label = tk.Label(
    main_frame,
    text="ยินดีต้อนรับ",
    font=FONT_LARGE,
    bg=WINDOW_BG,
    fg=TEXT_COLOR
)
welcome_label.pack(pady=(10, 5))

# ป้ายข้อความย่อย
subtitle_label = tk.Label(
    main_frame,
    text="กรุณาเลือกตัวเลือกด้านล่าง",
    font=FONT_MEDIUM,
    bg=WINDOW_BG,
    fg='#555555'
)
subtitle_label.pack(pady=(0, 30))

# Frame สำหรับปุ่ม
button_frame = tk.Frame(main_frame, bg=WINDOW_BG)
button_frame.pack(fill='x', expand=True)

# ปุ่ม Sign Up (ลงทะเบียน)
REGISTER_button = tk.Button(
    button_frame,
    text="ลงทะเบียนใบหน้า (Sign Up)",
    command=handle_sign_up,
    font=FONT_BUTTON,
    bg=BTN_REGISTER_BG,
    fg=BTN_REGISTER_FG,
    activebackground=BTN_REGISTER_ACTIVE_BG,
    activeforeground=BTN_REGISTER_ACTIVE_FG,  # **เพิ่มส่วนนี้**
    bd=0,
    highlightthickness=0,  # **เพิ่มส่วนนี้เพื่อลบขอบบน Mac**
    relief="flat",  # *** เพิ่มบรรทัดนี้เพื่อบังคับ macOS ***
    padx=20,
    pady=10,
    cursor="pointinghand"  # เปลี่ยน cursor เมื่อชี้
)
REGISTER_button.pack(pady=10, fill='x', expand=True)

# ปุ่ม Sign In (เข้าสู่ระบบ)
signin_button = tk.Button(
    button_frame,
    text="เข้าสู่ระบบ (Start Attendance)",
    command=handle_sign_in,
    font=FONT_BUTTON,
    bg=BTN_SIGNIN_BG,
    fg=BTN_SIGNIN_FG,
    activebackground=BTN_SIGNIN_ACTIVE_BG,
    activeforeground=BTN_SIGNIN_ACTIVE_FG,  # **เพิ่มส่วนนี้**
    bd=0,
    highlightthickness=0,  # **เพิ่มส่วนนี้เพื่อลบขอบบน Mac**
    relief="flat",  # *** เพิ่มบรรทัดนี้เพื่อบังคับ macOS ***
    padx=20,
    pady=10,
    cursor="pointinghand"
)
signin_button.pack(pady=10, fill='x', expand=True)

# เริ่ม Tkinter main loop
if __name__ == "__main__":
    root.mainloop()