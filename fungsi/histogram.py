import matplotlib.pyplot as plt
import numpy as np
from . import file_ops
from PIL import ImageOps, ImageTk

def show_histogram_rgb(image, title="Histogram"):
    if image is None:
        return

    arr = np.array(image)

    plt.figure(title, figsize=(6, 6))

    # Kalau grayscale (1 channel)
    if len(arr.shape) == 2 or image.mode == "L":
        plt.hist(arr.ravel(), bins=256, range=(0, 256), color="gray", alpha=0.9)
        plt.title("Grayscale")
        plt.xlim([0, 256])

    # Kalau RGB (3 channel)
    else:
        colors = ("red", "green", "blue")
        channel_names = ("Red", "Green", "Blue")

        for i, color in enumerate(colors):
            plt.subplot(3, 1, i+1)
            plt.hist(arr[:, :, i].ravel(), bins=256, range=(0, 256),
                     color=color, alpha=0.9)
            plt.title(channel_names[i])
            plt.xlim([0, 256])

        plt.tight_layout()

    plt.show()

def apply_grayscale_average():
    if file_ops.img_input_pil is None:
        return
    # simpan sebagai grayscale (mode "L")
    file_ops.img_output_pil = ImageOps.grayscale(file_ops.img_input_pil)

    # untuk ditampilkan di panel kanan, resize
    img_resized_out = file_ops.img_output_pil.resize((380, 340))
    file_ops.img_output = ImageTk.PhotoImage(img_resized_out)
    file_ops.panel_right.config(image=file_ops.img_output)
    file_ops.panel_right.image = file_ops.img_output

def histogram_input():
    show_histogram_rgb(file_ops.img_input_pil, "Histogram Input")


def histogram_output():
    if file_ops.img_output_pil is None:
        return

    arr_out = np.array(file_ops.img_output_pil)

    plt.figure("Histogram Output", figsize=(6, 6))

    # Kalau grayscale
    if len(arr_out.shape) == 2 or file_ops.img_output_pil.mode == "L":
        plt.hist(arr_out.ravel(), bins=256, range=(0, 256),
                 color="gray", alpha=0.9)
        plt.title("Output - Grayscale")
        plt.xlim([0, 256])

    # Kalau RGB
    else:
        colors = ("red", "green", "blue")
        channel_names = ("Red", "Green", "Blue")

        for i, color in enumerate(colors):
            plt.subplot(3, 1, i+1)
            plt.hist(arr_out[:, :, i].ravel(), bins=256, range=(0, 256),
                     color=color, alpha=0.9)
            plt.title(f"Output - {channel_names[i]}")
            plt.xlim([0, 256])

        plt.tight_layout()

    plt.show()



def histogram_both():
    if file_ops.img_input_pil is None or file_ops.img_output_pil is None:
        return

    arr_in = np.array(file_ops.img_input_pil)
    arr_out = np.array(file_ops.img_output_pil)

    plt.figure("Histogram Input & Output", figsize=(10, 6))

    # Input
    if len(arr_in.shape) == 2 or file_ops.img_input_pil.mode == "L":
        plt.subplot(1, 2, 1)
        plt.hist(arr_in.ravel(), bins=256, range=(0, 256), color="gray")
        plt.title("Input - Grayscale")
        plt.xlim([0, 256])
    else:
        colors = ("red", "green", "blue")
        for i, c in enumerate(colors):
            plt.subplot(3, 2, i*2+1)
            plt.hist(arr_in[:, :, i].ravel(), bins=256, range=(0, 256), color=c)
            plt.title(f"Input - {c.capitalize()}")
            plt.xlim([0, 256])

    # Output
    if len(arr_out.shape) == 2 or file_ops.img_output_pil.mode == "L":
        plt.subplot(1, 2, 2)
        plt.hist(arr_out.ravel(), bins=256, range=(0, 256), color="gray")
        plt.title("Output - Grayscale")
        plt.xlim([0, 256])
    else:
        colors = ("red", "green", "blue")
        for i, c in enumerate(colors):
            plt.subplot(3, 2, i*2+2)
            plt.hist(arr_out[:, :, i].ravel(), bins=256, range=(0, 256), color=c)
            plt.title(f"Output - {c.capitalize()}")
            plt.xlim([0, 256])

    plt.tight_layout()
    plt.show()

