import tkinter as tk
from tkinter import Label, font
from PIL import Image, ImageTk
import tkinter.font as tkFont  # Import tkinter font module

#Print Available Fonts
#root = tk.Tk()
#print(font.families())  # Prints all available fonts
#root.destroy()

def display_apod(image_path, explanation, title, credit_info):
    # Create a new window
    window = tk.Tk()
    window.title("Astronomy Picture of the Day")

    # Set the window to fullscreen
    window.attributes('-fullscreen', True)
    window.geometry("1920x1080")
    # Set the background color to black
    window.configure(bg='black')

    # Create a center-justified title at the top of the window
    #header_font = tkFont.Font(family="Futura", size=24, weight="bold")
    #header_label = Label(window, text="Astronomy Picture of the Day", bg='black', fg='white', font=header_font)
    #header_label.pack(pady=(20, 10))  # Add some padding at the top

    # Load and display the image using PIL
    image = Image.open(image_path)

    # Resize the image while maintaining aspect ratio
    max_width = 1400  # Set a maximum width for the image
    max_height = 700  # Set a maximum height for the image
    image.thumbnail((max_width, max_height), Image.LANCZOS)  # Resize the image

    photo = ImageTk.PhotoImage(image)

    # Create a frame to hold all elements in a vertical stack
    container_frame = tk.Frame(window, bg='black')
    container_frame.pack(expand=True)

    # Display the image
    image_label = Label(container_frame, image=photo, bg='black')
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack(pady=(5, 5))  # Center image with padding

    # Create a label for the title below the image
    title_font = tkFont.Font(family="Futura LT Pro Medium", size=20, weight="bold")
    title_label = Label(container_frame, text=title, wraplength=1800, justify="center", bg='black', fg='white', font=title_font)
    title_label.pack(pady=(5, 5))  # Center title below the image

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

# Example usage
# display_apod("path/to/apod/image.jpg", "Your explanation text here.", "Spiral Galaxy NGC 6744", "John Hayes - Copyright: Specific rights apply.")
