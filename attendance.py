# -*- coding: utf-8 -*-
"""
Attendance viewer & CSV reader (Tkinter + ttk.Treeview)

- อ่านไฟล์ CSV ชื่อใดชื่อหนึ่งที่พบก่อนในลิสต์:
  ["attendences.csv", "attendances.csv", "attendence.csv"]
- ให้เลือก "วันที่" ก่อน แล้วค่อยแสดงชื่อ/เวลาในวันนั้น
- มีป้าย "วันที่ที่เลือก" และปุ่ม "รีโหลด"
"""
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ชื่อไฟล์ที่ลองหาเป็นลำดับ
_CANDIDATE_CSVS = ["attendances.csv"]

def _auto_csv():
    """คืน path ของไฟล์ CSV ตัวแรกที่พบในโฟลเดอร์เดียวกับสคริปต์"""
    here = os.path.abspath(os.path.dirname(__file__))
    for name in _CANDIDATE_CSVS:
        p = os.path.join(here, name)
        if os.path.exists(p):
            return p
    # ถ้าไม่เจอเลย ก็คืนอันแรกไว้ก่อน (ไว้ให้ผู้ใช้เห็นพาธในกล่องแจ้งเตือน)
    return os.path.join(here, _CANDIDATE_CSVS[0])

def _read_rows(csv_path):
    """
    อ่าน CSV และคืนค่า list ของ dicts: [{name, time, date}, ...]
    - strip header เพื่อกันเคส ' Time'
    - คาดหวัง time format: dd/mm/YYYY HH:MM:SS
    """
    rows = []
    if not os.path.exists(csv_path):
        return rows

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # เคลียร์ช่องว่างในชื่อคอลัมน์
        reader.fieldnames = [ (h or "").strip() for h in (reader.fieldnames or []) ]

        for r in reader:
            # อ่านค่าแบบมี fallback เล็กน้อย
            name = (r.get("Name") or r.get("name") or "").strip()
            tstr = (r.get("Time") or r.get("time") or r.get("Timestamp") or "").strip()
            if not name or not tstr:
                continue

            # พาร์สเวลา
            try:
                dt = datetime.strptime(tstr, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                # ถ้าพาร์สไม่ได้ ข้ามแถวนั้น
                continue

            rows.append({
                "name": name,
                "time": dt.strftime("%H:%M:%S"),
                "date": dt.strftime("%d/%m/%Y"),
            })
    return rows

def open_attendance_window(parent=None, csv_path=None):
    """
    เปิดหน้าต่างย่อยเพื่อแสดงข้อมูลการเช็คชื่อแยกตามวัน
    - เริ่มต้น: ให้ "ยังไม่เลือกวัน" ตารางว่าง
    - เมื่อเลือกวัน: แสดงชื่อ/เวลา
    - ปุ่มรีโหลด: อ่าน CSV ใหม่และพยายามคงวันเดิมไว้
    """
    # หาไฟล์ CSV อัตโนมัติถ้าไม่ได้ระบุมา
    target_csv = csv_path or _auto_csv()
    rows = _read_rows(target_csv)

    def _all_dates(data):
        return sorted({r["date"] for r in data}, key=lambda s: datetime.strptime(s, "%d/%m/%Y"))

    dates = _all_dates(rows)

    win = tk.Toplevel(parent) if parent is not None else tk.Toplevel()
    win.title("บันทึกการเช็คชื่อ")
    win.geometry("620x520")
    win.minsize(600, 500)

    # ===== แถบเลือกวันที่ + ปุ่มรีโหลด =====
    top = tk.Frame(win)
    top.pack(side="top", fill="x", padx=12, pady=12)

    tk.Label(top, text="เลือกวันที่:").pack(side="left")

    selected_date = tk.StringVar(value="")  # เริ่มยังไม่เลือก
    date_combo = ttk.Combobox(top, textvariable=selected_date, state="readonly", width=16)
    date_combo.pack(side="left", padx=8)

    def refresh_table(date_str):
        for iid in tree.get_children():
            tree.delete(iid)
        if not date_str:
            count_var.set("รวม 0 รายการ")
            return
        cnt = 0
        for r in rows:
            if r["date"] == date_str:
                tree.insert("", "end", values=(r["name"], r["time"]))
                cnt += 1
        count_var.set(f"รวม {cnt} รายการ")

    def on_date_change(event=None):
        d = selected_date.get()
        refresh_table(d)

    # ตั้งค่า combobox values (ยังไม่เลือก)
    date_combo["values"] = dates
    date_combo.bind("<<ComboboxSelected>>", on_date_change)

    # ===== ตาราง =====
    columns = ("name", "time")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=18)
    tree.pack(side="top", fill="both", expand=True, padx=12, pady=(0, 8))
    tree.heading("name", text="ชื่อ")
    tree.heading("time", text="เวลา")
    tree.column("name", width=380, anchor="w")
    tree.column("time", width=160, anchor="center")

    yscroll = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.place(relx=1.0, rely=0.24, relheight=0.66, anchor="ne")

    # ===== แถบสรุป =====
    bottom = tk.Frame(win)
    bottom.pack(side="bottom", fill="x", padx=12, pady=10)
    count_var = tk.StringVar(value="รวม 0 รายการ")
    tk.Label(bottom, textvariable=count_var, anchor="w").pack(side="left")

    # เริ่มต้นยังไม่เลือก
    selected_date.set("")
    on_date_change()

    # แจ้งเตือนถ้าไม่พบไฟล์/ไม่มีข้อมูล
    if not os.path.exists(target_csv):
        messagebox.showwarning(
            "ไม่พบไฟล์ CSV",
            f"ไม่พบไฟล์ CSV ในโฟลเดอร์นี้\nที่ลองหา: {', '.join(_CANDIDATE_CSVS)}"
        )
    elif not rows:
        messagebox.showinfo(
            "ไม่มีข้อมูล",
            f"อ่านไฟล์ได้: {os.path.basename(target_csv)}\nแต่ไม่พบข้อมูลที่พาร์สได้\n\n"
            "ตรวจสอบ:\n"
            "- หัวคอลัมน์ต้องเป็น Name, Time\n"
            "- รูปแบบเวลา dd/mm/YYYY HH:MM:SS\n"
            "- ไม่มีบรรทัดว่าง/รูปแบบผิด"
        )

    return win

# ทดสอบรันเดี่ยว
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_attendance_window(root)
    root.mainloop()