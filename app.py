import tkinter as tk
import os
import sys
import subprocess

# --- ฟังก์ชันกลางสำหรับเปิดหน้าต่างย่อย (Reusable) ---
def open_sub_window(script_name):
    """
    ปิดหน้าต่างหลัก → เปิดสคริปต์ย่อย (เช่น main.py / register.py / attendance.py)
    และเมื่อปิดสคริปต์ย่อยแล้ว จะกลับมาที่หน้าต่างหลักอีกครั้ง
    """
    global root
    print(f"--- เปิดสคริปต์: {script_name} ---")

    # 1. ปิดหน้าต่างหลัก
    try:
        root.destroy()
    except tk.TclError:
        pass

    # 2. รันสคริปต์ย่อยและรอจนกว่าจะปิด
    try:
        command = [sys.executable, script_name]
        print(f"กำลังรันคำสั่ง: {' '.join(command)}")
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการรัน {script_name}: {e}")

    # 3. เมื่อปิดหน้าต่างย่อยแล้ว กลับมาเปิด GUI หลักอีกครั้ง
    print("--- กลับมาที่หน้าหลัก ---")
    show_main_window()


# --- ฟังก์ชันควบคุม (Handlers) ---

def handle_check_data():
    open_sub_window("attendance.py")

def handle_sign_up():
    open_sub_window("register.py")

def handle_sign_in():
    open_sub_window("main.py")


# --- ฟังก์ชันสร้างหน้าต่างหลักใหม่ ---
def show_main_window():
    global root
    root = tk.Tk()
    root.title("ระบบเช็คชื่อด้วยใบหน้า (Face Attendance System)")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg='#f0f0f0')

    # --- การตั้งค่าสไตล์ (Styles) ---
    WINDOW_BG = '#f0f0f0'
    TEXT_COLOR = '#333333'
    FONT_LARGE = ('Helvetica', 18, 'bold')
    FONT_MEDIUM = ('Helvetica', 12)
    FONT_BUTTON = ('Helvetica', 12, 'bold')

    BTN_REGISTER_BG = '#4CAF50'
    BTN_REGISTER_FG = '#ffffff'
    BTN_REGISTER_ACTIVE_BG = '#45a049'
    BTN_REGISTER_ACTIVE_FG = '#ffffff'

    BTN_SIGNIN_BG = '#2196F3'
    BTN_SIGNIN_FG = '#ffffff'
    BTN_SIGNIN_ACTIVE_BG = '#1e88e5'
    BTN_SIGNIN_ACTIVE_FG = '#ffffff'

    # --- การจัดวางองค์ประกอบ (Layout) ---
    main_frame = tk.Frame(root, bg=WINDOW_BG, padx=30, pady=30)
    main_frame.pack(expand=True, fill='both')

    welcome_label = tk.Label(
        main_frame, text="ยินดีต้อนรับ",
        font=FONT_LARGE, bg=WINDOW_BG, fg=TEXT_COLOR
    )
    welcome_label.pack(pady=(10, 5))

    subtitle_label = tk.Label(
        main_frame, text="กรุณาเลือกตัวเลือกด้านล่าง",
        font=FONT_MEDIUM, bg=WINDOW_BG, fg='#555555'
    )
    subtitle_label.pack(pady=(0, 30))

    button_frame = tk.Frame(main_frame, bg=WINDOW_BG)
    button_frame.pack(fill='x', expand=True)

    # ปุ่มลงทะเบียนใบหน้า
    tk.Button(
        button_frame,
        text="ลงทะเบียนใบหน้า (Register)",
        command=handle_sign_up,
        font=FONT_BUTTON,
        bg=BTN_REGISTER_BG, fg=BTN_REGISTER_FG,
        activebackground=BTN_REGISTER_ACTIVE_BG,
        activeforeground=BTN_REGISTER_ACTIVE_FG,
        bd=0, highlightthickness=0, relief="flat",
        padx=20, pady=10, cursor="pointinghand"
    ).pack(pady=10, fill='x', expand=True)

    # ปุ่มเริ่มระบบเช็คชื่อ
    tk.Button(
        button_frame,
        text="เข้าสู่ระบบ (Start Attendance)",
        command=handle_sign_in,
        font=FONT_BUTTON,
        bg=BTN_SIGNIN_BG, fg=BTN_SIGNIN_FG,
        activebackground=BTN_SIGNIN_ACTIVE_BG,
        activeforeground=BTN_SIGNIN_ACTIVE_FG,
        bd=0, highlightthickness=0, relief="flat",
        padx=20, pady=10, cursor="pointinghand"
    ).pack(pady=10, fill='x', expand=True)

    # ปุ่มดูข้อมูลการเช็คชื่อ
    tk.Button(
        button_frame,
        text="ดูการเช็คชื่อ (เลือกวัน)",
        command=handle_check_data,
        font=FONT_BUTTON,
        bg=BTN_SIGNIN_BG, fg=BTN_SIGNIN_FG,
        activebackground=BTN_SIGNIN_ACTIVE_BG,
        activeforeground=BTN_SIGNIN_ACTIVE_FG,
        bd=0, highlightthickness=0, relief="flat",
        padx=20, pady=10, cursor="pointinghand"
    ).pack(pady=10, fill='x', expand=True)

    root.mainloop()


# --- เริ่มต้นโปรแกรม ---
if __name__ == "__main__":
    show_main_window()
