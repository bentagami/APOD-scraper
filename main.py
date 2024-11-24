from fetch import fetch_explanation, fetch_img, fetch_title_credit
from display import display_apod
import schedule
import time
import tkinter as tk

def main():
    try:
        explanation = fetch_explanation()
        image_path = fetch_img()
        title, credit_info = fetch_title_credit()
        display_apod(image_path, explanation, title, credit_info)
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
    schedule_updates()  # This will run the scheduling in a blocking manner
