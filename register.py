import tkinter as tk
import cv2
import face_recognition
from tkinter import simpledialog
import numpy as np

from PIL import Image, ImageTk
import datetime  # Added for unique filenames

# --- Globals ---
latest_frame = None  # To store the most recent frame

# --- Setup ---
root = tk.Tk()
root.title("Register")
root.resizable(False, False)

# Let the video label expand to fill space
video_label = tk.Label(root)
video_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- New Widgets (Bottom Frame) ---

# Create a frame at the bottom for controls
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

# Create a StringVar for the status bar
status_var = tk.StringVar()
status_var.set("")

# Create the status bar label
status_label = tk.Label(
    bottom_frame,
    textvariable=status_var,
    relief=tk.FLAT,  # Gives it a "sunken" look
    anchor=tk.CENTER  # 'W' stands for West (left-align)
)
status_label.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5)

# Create the snapshot button
snapshot_button = tk.Button(
    bottom_frame,
    text="Take Snapshot",
    command=lambda: take_snapshot()  # Call the new function
)
snapshot_button.pack(side=tk.BOTTOM, pady=20)

# --- Webcam and Main Loop ---
cap = cv2.VideoCapture(0)


# --- Functions ---

def show_frame():
    """Reads a frame, updates the video label, and stores the frame."""
    global latest_frame  # Access the global variable

    ret, frame = cap.read()

    # ============================================================

    resized_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    converted_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(converted_frame)

    for location in locations:
        y1, x2, y2, x1 = location
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # rescale พิกัดกลับมาไซส์เดิม
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0),
                      3)  # cv2.rectangle(image, pt1บนซ้าย, pt2ล่างขวา, color, thickness)

    # ============================================================

    if ret:
        latest_frame = frame  # Store the raw frame

        # Convert for Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Repeat
        video_label.after(15, show_frame)
    else:
        # Handle error if webcam disconnects
        status_var.set("Error: Cannot read from webcam")


def take_snapshot():
    """Saves the latest frame as a PNG file."""
    global latest_frame

    if latest_frame is not None:


        resized_frame = cv2.resize(latest_frame, (0, 0), fx=0.25, fy=0.25)
        converted_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(converted_image)

        if len(locations) != 1:
            status_var.set("Error: Must have 1 person in frame.")
        else:
            encoded = face_recognition.face_encodings(converted_image)[0]

            filename = simpledialog.askstring(
                title="Register",
                prompt="Enter register name..."
            )

            if not filename:  # This checks for None (Cancel) or an empty string ""
                status_var.set("Register canceled")
                return  # Stop the function

            np.save(f"face_input_vectors/{filename}.npy", encoded)
            status_var.set("Registered!")

    else:
        status_var.set("Error: No frame captured yet")


def on_closing():
    """Releases the webcam and closes the application."""
    print("Releasing webcam and closing...")
    cap.release()
    root.destroy()


# --- Main ---
root.protocol("WM_DELETE_WINDOW", on_closing)
show_frame()  # Start the video loop
root.mainloop()