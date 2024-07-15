import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import subprocess

def open_easy_mode():
    subprocess.Popen(['python', 'easy_mode.py'])

def open_medium_mode():
    subprocess.Popen(['python', 'medium_mode.py'])

def open_hard_mode():
    subprocess.Popen(['python', 'hard_mode.py'])

def toggle_dark_mode():
    subprocess.Popen(['python', 'dark_mode.py'])
    pass

def toggle_no_light_mode():
    # Add your code to toggle no light mode here
    pass

def save_high_score(mode, score):
    with open(f"{mode}_high_score.txt", "w") as file:
        file.write(str(score))
    print(f"High score for {mode} mode saved: {score}")

def load_high_score(mode):
    try:
        with open(f"{mode}_high_score.txt", "r") as file:
            high_score = int(file.read())
        print(f"High score for {mode} mode loaded: {high_score}")
        return high_score
    except FileNotFoundError:
        print(f"No high score found for {mode} mode.")
        return 0

# Create the main window
root = tk.Tk()
root.title("Flappy Bird Game Modes")

# Set the window size
window_width = 900
window_height = 600
root.geometry(f"{window_width}x{window_height}")

# Set custom font
button_font = font.Font(family='Bauhaus', size=12, weight='bold')

# Set custom colors
button_bg_color = '#4CAF50'  # Green
button_fg_color = 'white'
button_hover_color = '#45a049'  # Darker green on hover

# Load and display the background image
try:
    background_image = Image.open("background_image.png")  # Replace with your background image file
    background_image = background_image.resize((window_width, window_height))
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Error loading background image:", e)

# Create frame for the buttons
button_frame = tk.Frame(root, bg='black')
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create buttons for each mode
button_width = 12
button_height = 2
button_padx = 20
button_pady = 25

easy_button = tk.Button(button_frame, text="Easy Mode", command=open_easy_mode, font=button_font, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_color, width=button_width, height=button_height)
easy_button.pack(side=tk.LEFT, pady=button_pady, padx=button_padx)

medium_button = tk.Button(button_frame, text="Medium Mode", command=open_medium_mode, font=button_font, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_color, width=button_width, height=button_height)
medium_button.pack(side=tk.LEFT, pady=button_pady, padx=button_padx)

hard_button = tk.Button(button_frame, text="Hard Mode", command=open_hard_mode, font=button_font, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_color, width=button_width, height=button_height)
hard_button.pack(side=tk.LEFT, pady=button_pady, padx=button_padx)

# Add buttons for additional modes
dark_mode_button = tk.Button(button_frame, text="Dark Mode", command=toggle_dark_mode, font=button_font, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_color, width=button_width, height=button_height)
dark_mode_button.pack(side=tk.LEFT, pady=button_pady, padx=button_padx)

no_light_mode_button = tk.Button(button_frame, text="No Light Mode", command=toggle_no_light_mode, font=button_font, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_color, width=button_width, height=button_height)
no_light_mode_button.pack(side=tk.LEFT, pady=button_pady, padx=button_padx)

# Display high scores for each mode
easy_high_score = load_high_score("easy")
easy_high_score_label = tk.Label(root, text=f"Easy High Score: {easy_high_score}", font=button_font, bg='#f0f0f0')
easy_high_score_label.pack(side=tk.TOP, pady=10)

medium_high_score = load_high_score("medium")
medium_high_score_label = tk.Label(root, text=f"Medium High Score: {medium_high_score}", font=button_font, bg='#f0f0f0')
medium_high_score_label.pack(side=tk.TOP, pady=10)

hard_high_score = load_high_score("hard")
hard_high_score_label = tk.Label(root, text=f"Hard High Score: {hard_high_score}", font=button_font, bg='#f0f0f0')
hard_high_score_label.pack(side=tk.TOP, pady=10)

# Run the main event loop
root.mainloop()
