from tkinter import Menu
from PIL import ImageTk, ImageOps, ImageEnhance
from . import file_ops
from PIL import Image, ImageTk, ImageOps
import numpy as np
from . import file_ops

def update_output(img_pil):
    """Helper untuk update panel kanan"""
    file_ops.img_output_pil = img_pil
    img_resized_out = img_pil.resize((380, 340))
    file_ops.img_output = ImageTk.PhotoImage(img_resized_out)

    file_ops.panel_right.config(image=file_ops.img_output)
    file_ops.panel_right.image = file_ops.img_output


# ===== RGB Warna Sederhana =====
def apply_color_tone(color):
    if file_ops.img_input_pil is None:
        return
    r, g, b = file_ops.img_input_pil.split()
    if color == "Kuning":
        img = Image.merge("RGB", (r, g, b.point(lambda x: 0)))
    elif color == "Orange":
        img = Image.merge("RGB", (r, g.point(lambda x: int(x*0.5)), b.point(lambda x: 0)))
    elif color == "Cyan":
        img = Image.merge("RGB", (r.point(lambda x: 0), g, b))
    elif color == "Purple":
        img = Image.merge("RGB", (r, g.point(lambda x: 0), b))
    elif color == "Grey":
        img = ImageOps.grayscale(file_ops.img_input_pil).convert("RGB")
    elif color == "Coklat":
        img = Image.merge("RGB", (r, g.point(lambda x: int(x*0.7)), b.point(lambda x: int(x*0.4))))
    elif color == "Merah":
        img = Image.merge("RGB", (r, g.point(lambda x: 0), b.point(lambda x: 0)))
    else:
        img = file_ops.img_input_pil
    update_output(img)


# ===== Grayscale Variasi =====
def grayscale_average():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil)
    gray = np.mean(arr, axis=2).astype("uint8")
    img = Image.fromarray(gray, mode="L")   # simpan mode L (grayscale)
    update_output(img)


def grayscale_lightness():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil)
    gray = ((arr.max(axis=2) + arr.min(axis=2)) / 2).astype("uint8")
    img = Image.fromarray(gray, mode="L")
    update_output(img)


def grayscale_luminance():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil)
    gray = (0.299*arr[:, :, 0] + 0.587*arr[:, :, 1] + 0.114*arr[:, :, 2]).astype("uint8")
    img = Image.fromarray(gray, mode="L")
    update_output(img)


# ===== Brightness / Contrast =====
def adjust_contrast():
    if file_ops.img_input_pil is None:
        return
    enhancer = ImageEnhance.Contrast(file_ops.img_input_pil)
    img = enhancer.enhance(1.5)  # contoh tingkat contrast
    update_output(img)


# ===== Invers =====
def invert_colors():
    if file_ops.img_input_pil is None:
        return
    img = ImageOps.invert(file_ops.img_input_pil)
    update_output(img)


# ===== Log Brightness =====
import numpy as np
def log_brightness():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil, dtype=np.float32)
    c = 255 / np.log(1 + np.max(arr))
    arr = c * np.log(1 + arr)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    from PIL import Image
    img = Image.fromarray(arr)
    update_output(img)


# ===== Bit Depth =====
def reduce_bit_depth(bits):
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil)
    shift = 8 - bits
    arr = (arr >> shift) << shift
    from PIL import Image
    img = Image.fromarray(arr)
    update_output(img)


# ===== Gamma Correction =====
def gamma_correction():
    if file_ops.img_input_pil is None:
        return
    gamma = 2.2
    inv_gamma = 1.0 / gamma
    table = [int((i / 255.0) ** inv_gamma * 255) for i in range(256)]
    img = file_ops.img_input_pil.point(table * 3)
    update_output(img)


# ===== Build Menu =====
def build_colors_menu(menubar):
    colors_menu = Menu(menubar, tearoff=0)

    # RGB submenu
    rgb_menu = Menu(colors_menu, tearoff=0)
    for color in ["Kuning", "Orange", "Cyan", "Purple", "Grey", "Coklat", "Merah"]:
        rgb_menu.add_command(label=color, command=lambda c=color: apply_color_tone(c))
    colors_menu.add_cascade(label="RGB", menu=rgb_menu)

    # Grayscale submenu
    grayscale_menu = Menu(colors_menu, tearoff=0)
    grayscale_menu.add_command(label="Average", command=grayscale_average)
    grayscale_menu.add_command(label="Lightness", command=grayscale_lightness)
    grayscale_menu.add_command(label="Luminance", command=grayscale_luminance)
    colors_menu.add_cascade(label="RGB to Grayscale", menu=grayscale_menu)

    # Brightness submenu
    brightness_menu = Menu(colors_menu, tearoff=0)
    brightness_menu.add_command(label="Contrast", command=adjust_contrast)
    colors_menu.add_cascade(label="Brightness", menu=brightness_menu)

    # lainnya
    colors_menu.add_command(label="Invers", command=invert_colors)
    colors_menu.add_command(label="Log Brightness", command=log_brightness)

    # Bit Depth submenu
    bitdepth_menu = Menu(colors_menu, tearoff=0)
    for i in range(1, 8):
        bitdepth_menu.add_command(label=f"{i} bit", command=lambda b=i: reduce_bit_depth(b))
    colors_menu.add_cascade(label="Bit Depth", menu=bitdepth_menu)

    colors_menu.add_command(label="Gamma Correction", command=gamma_correction)

    menubar.add_cascade(label="Colors", menu=colors_menu)
