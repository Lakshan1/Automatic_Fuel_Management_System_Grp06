import tkinter as tk
import cv2
import threading
from PIL import Image, ImageTk
import queue

root = tk.Tk()
canvas = tk.Canvas(root, width=1280, height=480)
canvas.pack()

# Create two image labels
label1 = tk.Label(canvas)
label1.pack(side=tk.LEFT)
label2 = tk.Label(canvas)
label2.pack(side=tk.RIGHT)

# Create two queues for each camera
queue1 = queue.Queue()
queue2 = queue.Queue()

def capture_frames(cam_id, queue):
    cap = cv2.VideoCapture(cam_id)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        queue.put(frame)
    cap.release()

# Create two threads to capture frames from each camera
thread1 = threading.Thread(target=capture_frames, args=(0, queue1))
thread2 = threading.Thread(target=capture_frames, args=(1, queue2))
thread1.start()
thread2.start()

def update_frames():
    global thread1, thread2, queue1, queue2
    if not queue1.empty() and not queue2.empty():
        frame1 = queue1.get()
        frame2 = queue2.get()

        # Convert frames to PIL Image and resize
        img1 = Image.fromarray(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)).resize((640, 480))
        img2 = Image.fromarray(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)).resize((640, 480))

        # Convert PIL Image to Tkinter PhotoImage and update labels
        tk_img1 = ImageTk.PhotoImage(img1)
        tk_img2 = ImageTk.PhotoImage(img2)
        label1.config(image=tk_img1)
        label1.image = tk_img1
        label2.config(image=tk_img2)
        label2.image = tk_img2

    root.after(10, update_frames)

# Start the update_frames loop
update_frames()

root.mainloop()
