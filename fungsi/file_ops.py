from tkinter import filedialog
from PIL import Image, ImageTk

# variabel global
img_input_pil = None
img_output_pil = None
img_input = None
img_output = None

# panel (akan diisi dari main.py)
panel_left = None
panel_right = None


def open_file():
    global img_input_pil, img_output_pil, img_input, img_output

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        img_input_pil = Image.open(file_path).convert("RGB")
        img_output_pil = None

        img_resized_in = img_input_pil.resize((380, 340))
        img_input = ImageTk.PhotoImage(img_resized_in)

        panel_left.config(image=img_input)
        panel_left.image = img_input

        # kosongkan panel kanan
        panel_right.config(image="")
        panel_right.image = None


def save_file():
    if img_output_pil is None:
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if file_path:
        img_output_pil.save(file_path)
