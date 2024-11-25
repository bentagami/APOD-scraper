from fetch import fetch_explanation, fetch_img, fetch_title_credit, fetch_video, get_video_url
from display import display_apod
import tkinter as tk
import os

def main():
    try:
        # Fetch the explanation, title, and credit info
        explanation = fetch_explanation()
        title, credit_info = fetch_title_credit()

        # Fetch the image path and check if it exists
        image_path = fetch_img()

        # Check if the image path is valid (not None and exists)
        if image_path and os.path.exists(image_path):  # If the image exists, display it
            print(f"Displaying image: {image_path}")  # Debugging line
            display_apod(image_path, explanation, title, credit_info)
        else:
            # If no image exists, fetch and display the video
            video_url = get_video_url()  # Get the video URL
            video_path = fetch_video(video_url)  # Fetch and save the video locally
            print(f"Video path returned: {video_path}")  # Debugging line

            # Check if the video path is valid (not None and exists)
            if video_path and os.path.exists(video_path):
                print(f"Displaying video: {video_path}")
                display_apod(image_path=None, explanation=explanation, title=title, credit_info=credit_info,
                             video_path=video_path)
            else:
                raise FileNotFoundError("Neither image nor video could be found or downloaded.")
    except Exception as e:
        show_error_window(e)

def show_error_window(error):
    root = tk.Tk()
    root.title("Error")
    root.geometry("400x200")
    error_message = tk.Label(root, text=f"An error occurred:\n{error}", wraplength=380, justify="left")
    error_message.pack(pady=20, padx=10)
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
