import tkinter as tk
from tkinter import Label, font
import cv2
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os  # For checking if the file exists
import threading
import time

def display_apod(image_path, explanation, title, credit_info, video_path=None):
    # Create a new window
    window = tk.Tk()
    window.title("Astronomy Picture of the Day")

    # Set the window to fullscreen
    window.attributes('-fullscreen', True)
    window.geometry("1920x1080")
    window.configure(bg='black')

    # Create a frame to hold all elements in a vertical stack
    container_frame = tk.Frame(window, bg='black')
    container_frame.pack(expand=True)

    if image_path:
        # Load and display the image using PIL
        image = Image.open(image_path)

        # Resize the image while maintaining aspect ratio
        max_width = 1400  # Set a maximum width for the image
        max_height = 700  # Set a maximum height for the image
        image.thumbnail((max_width, max_height), Image.LANCZOS)  # Resize the image

        photo = ImageTk.PhotoImage(image)

        # Display the image
        image_label = Label(container_frame, image=photo, bg='black')
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=(5, 5))  # Center image with padding
    elif video_path:
        def play_video():
            # Open the video file using OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("Error: Could not open video.")
                return

            # Get the video's frames per second (FPS) to control playback speed
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Create a canvas for video frames
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            canvas = tk.Canvas(container_frame, width=width, height=height)
            canvas.pack()

            # Function to display the video frames
            def update_video():
                while True:  # Infinite loop to keep the video playing
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the start
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break  # If video ended, restart it

                        # Convert the frame to RGB (from BGR)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        # Convert to Image format
                        img = Image.fromarray(frame)
                        img_tk = ImageTk.PhotoImage(image=img)

                        # Display the image on the canvas
                        canvas.create_image(0, 0, anchor="nw", image=img_tk)
                        canvas.image = img_tk  # Keep a reference to avoid garbage collection

                        window.update_idletasks()
                        window.update()

                        # Control playback speed by introducing a delay based on FPS
                        time.sleep(1 / fps)  # Delay to match the video FPS

                cap.release()  # Release the video capture object after the loop finishes

            # Start video playback in a new thread to avoid blocking the GUI
            video_thread = threading.Thread(target=update_video)
            video_thread.daemon = True
            video_thread.start()

            # Call the play_video function to start the video

        play_video()

    # Create a label for the title below the image/video
    title_font = tkFont.Font(family="Futura LT Pro Medium", size=20, weight="bold")
    title_label = Label(container_frame, text=title, wraplength=1800, justify="center", bg='black', fg='white', font=title_font)
    title_label.pack(pady=(5, 5))  # Center title below the image/video

    # Create a label for the copyright info at the bottom
    copyright_font = tkFont.Font(family="Futura LT Pro Medium", size=10)  # Smaller font for copyright info
    copyright_label = Label(container_frame, text=credit_info, wraplength=1800, justify="center", bg='black', fg='white', font=copyright_font)
    copyright_label.pack(pady=(5, 5))  # Center copyright

    # Create a custom font for explanation text
    custom_font = tkFont.Font(family="Futura LT Pro Medium", size=14, weight="normal")

    # Create a label for the explanation text
    explanation_label = Label(
        container_frame,
        text=explanation,
        wraplength=1800,  # Set a wraplength to keep text centered
        justify="center",
        bg='black',
        fg='white',
        font=custom_font,  # Set the custom font here
    )
    explanation_label.pack(pady=(20, 30))  # Center explanation with padding

    # Function to exit full-screen mode
    def end_fullscreen(event=None):
        window.attributes('-fullscreen', False)

    # Bind the Escape key to exit fullscreen mode
    window.bind("<Escape>", end_fullscreen)

    # Start the Tkinter event loop
    window.mainloop()


def play_video(video_path, video_label, window):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the video frame size
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a canvas for video frames
    canvas = tk.Canvas(video_label, width=width, height=height)
    canvas.pack()

    # Function to display the video frames
    def update_video():
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Video ended

            # Convert the frame to RGB (from BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to Image format
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)

            # Display the image on the canvas
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # Keep a reference to avoid garbage collection

            window.update_idletasks()
            window.update()

        cap.release()

    # Start video playback in a new thread
    video_thread = threading.Thread(target=update_video)
    video_thread.daemon = True
    video_thread.start()
