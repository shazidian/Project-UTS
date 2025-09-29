import numpy as np
from PIL import Image, ImageOps, ImageTk
from . import file_ops


def update_output(img_pil):
    """Helper untuk update panel kanan"""
    file_ops.img_output_pil = img_pil
    img_resized_out = img_pil.resize((380, 340))
    file_ops.img_output = ImageTk.PhotoImage(img_resized_out)
    file_ops.panel_right.config(image=file_ops.img_output)
    file_ops.panel_right.image = file_ops.img_output


# === Histogram Equalization ===
def histogram_equalization():
    if file_ops.img_input_pil is None:
        return
    img_gray = ImageOps.grayscale(file_ops.img_input_pil)
    arr = np.array(img_gray)

    # Equalization
    hist, bins = np.histogram(arr.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    arr_equalized = np.interp(arr.flatten(), bins[:-1], cdf)
    arr_equalized = arr_equalized.reshape(arr.shape).astype("uint8")

    img_eq = Image.fromarray(arr_equalized, mode="L")
    update_output(img_eq)


# === Fuzzy HE RGB ===
def fuzzy_he_rgb():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil)

    # Per channel equalization (sederhana)
    out = np.zeros_like(arr)
    for i in range(3):
        hist, bins = np.histogram(arr[:, :, i].flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf = 255 * cdf / cdf[-1]
        eq = np.interp(arr[:, :, i].flatten(), bins[:-1], cdf)
        out[:, :, i] = eq.reshape(arr[:, :, i].shape)

    img_eq = Image.fromarray(out.astype("uint8"), "RGB")
    update_output(img_eq)


# === Fuzzy Grayscale ===
def fuzzy_grayscale():
    if file_ops.img_input_pil is None:
        return
    arr = np.array(file_ops.img_input_pil.convert("L"))

    # Membership function sederhana (fuzzy contrast stretch)
    arr_norm = arr / 255.0
    arr_fuzzy = np.where(arr_norm < 0.5, arr_norm**2, np.sqrt(arr_norm))
    arr_out = (arr_fuzzy * 255).astype("uint8")

    img_out = Image.fromarray(arr_out, mode="L")
    update_output(img_out)


# === Build Menu ===
def build_image_processing_menu(menubar):
    from tkinter import Menu
    ip_menu = Menu(menubar, tearoff=0)
    ip_menu.add_command(label="Histogram Equalization", command=histogram_equalization)
    ip_menu.add_command(label="Fuzzy HE RGB", command=fuzzy_he_rgb)
    ip_menu.add_command(label="Fuzzy Grayscale", command=fuzzy_grayscale)

    menubar.add_cascade(label="Image Processing", menu=ip_menu)
