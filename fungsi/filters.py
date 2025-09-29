import numpy as np
from PIL import Image, ImageTk, ImageFilter
from scipy import ndimage
from . import file_ops

def update_output(img_pil):
    """Helper untuk update panel kanan"""
    file_ops.img_output_pil = img_pil
    img_resized_out = img_pil.resize((380, 340))
    file_ops.img_output = ImageTk.PhotoImage(img_resized_out)
    file_ops.panel_right.config(image=file_ops.img_output)
    file_ops.panel_right.image = file_ops.img_output

# === FILTER IDENTITY ===
def filter_identity():
    if file_ops.img_input_pil is None:
        return
    # Identity filter (tidak mengubah gambar)
    update_output(file_ops.img_input_pil)

# === EDGE DETECTION ===
def sobel_edge_detection():
    if file_ops.img_input_pil is None:
        return
    img_gray = file_ops.img_input_pil.convert('L')
    array = np.array(img_gray)
    
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    grad_x = ndimage.convolve(array, sobel_x)
    grad_y = ndimage.convolve(array, sobel_y)
    
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    gradient = (gradient / gradient.max()) * 255
    gradient = gradient.astype(np.uint8)
    
    img_out = Image.fromarray(gradient, mode='L')
    update_output(img_out)

def prewitt_edge_detection():
    if file_ops.img_input_pil is None:
        return
    img_gray = file_ops.img_input_pil.convert('L')
    array = np.array(img_gray)
    
    # Prewitt kernels
    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    
    grad_x = ndimage.convolve(array, prewitt_x)
    grad_y = ndimage.convolve(array, prewitt_y)
    
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    gradient = (gradient / gradient.max()) * 255
    gradient = gradient.astype(np.uint8)
    
    img_out = Image.fromarray(gradient, mode='L')
    update_output(img_out)

def roberts_edge_detection():
    if file_ops.img_input_pil is None:
        return
    img_gray = file_ops.img_input_pil.convert('L')
    array = np.array(img_gray)
    
    # Roberts cross operator
    roberts_x = np.array([[1, 0], [0, -1]])
    roberts_y = np.array([[0, 1], [-1, 0]])
    
    grad_x = ndimage.convolve(array, roberts_x)
    grad_y = ndimage.convolve(array, roberts_y)
    
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    gradient = (gradient / gradient.max()) * 255
    gradient = gradient.astype(np.uint8)
    
    img_out = Image.fromarray(gradient, mode='L')
    update_output(img_out)

# === SHARPEN ===
def sharpen_filter():
    if file_ops.img_input_pil is None:
        return
    # Sharpen kernel
    kernel = ImageFilter.Kernel((3, 3), 
                               [0, -1, 0, 
                                -1, 5, -1, 
                                0, -1, 0], 
                               scale=1)
    img_out = file_ops.img_input_pil.filter(kernel)
    update_output(img_out)

# === GAUSSIAN BLUR ===
def gaussian_blur():
    if file_ops.img_input_pil is None:
        return
    img_out = file_ops.img_input_pil.filter(ImageFilter.GaussianBlur(radius=2))
    update_output(img_out)

# === UNSHARP MASKING ===
def unsharp_masking():
    if file_ops.img_input_pil is None:
        return
    img_out = file_ops.img_input_pil.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    update_output(img_out)

# === AVERAGE FILTER ===
def average_filter():
    if file_ops.img_input_pil is None:
        return
    # Average filter 3x3
    kernel = np.ones((3, 3)) / 9.0
    array = np.array(file_ops.img_input_pil)
    
    if len(array.shape) == 3:  # RGB
        filtered = np.zeros_like(array)
        for i in range(3):
            filtered[:, :, i] = ndimage.convolve(array[:, :, i], kernel)
    else:  # Grayscale
        filtered = ndimage.convolve(array, kernel)
    
    img_out = Image.fromarray(filtered.astype(np.uint8))
    update_output(img_out)

# === LOW PASS FILTER ===
def low_pass_filter():
    if file_ops.img_input_pil is None:
        return
    # Low pass filter 5x5
    kernel = np.ones((5, 5)) / 25.0
    array = np.array(file_ops.img_input_pil)
    
    if len(array.shape) == 3:  # RGB
        filtered = np.zeros_like(array)
        for i in range(3):
            filtered[:, :, i] = ndimage.convolve(array[:, :, i], kernel)
    else:  # Grayscale
        filtered = ndimage.convolve(array, kernel)
    
    img_out = Image.fromarray(filtered.astype(np.uint8))
    update_output(img_out)

# === HIGH PASS FILTER ===
def high_pass_filter():
    if file_ops.img_input_pil is None:
        return
    # High pass filter = original - low pass
    img_gray = file_ops.img_input_pil.convert('L')
    array = np.array(img_gray, dtype=np.float32)
    
    # Low pass filter
    low_pass_kernel = np.ones((5, 5)) / 25.0
    low_pass = ndimage.convolve(array, low_pass_kernel)
    
    # High pass
    high_pass = array - low_pass
    high_pass = np.clip(high_pass + 128, 0, 255)  # Add offset for better visualization
    
    img_out = Image.fromarray(high_pass.astype(np.uint8), mode='L')
    update_output(img_out)

# === BANDSTOP FILTER ===
def bandstop_filter():
    if file_ops.img_input_pil is None:
        return
    # Bandstop filter menggunakan FFT
    img_gray = file_ops.img_input_pil.convert('L')
    array = np.array(img_gray, dtype=np.float32)
    
    # FFT
    fft = np.fft.fft2(array)
    fft_shift = np.fft.fftshift(fft)
    
    # Create bandstop mask (stop frekuensi tengah)
    rows, cols = array.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols))
    
    # Stop frequencies dalam radius tertentu
    r_inner = 10
    r_outer = 30
    y, x = np.ogrid[:rows, :cols]
    mask_area = np.logical_and(
        (x - ccol)**2 + (y - crow)**2 >= r_inner**2,
        (x - ccol)**2 + (y - crow)**2 <= r_outer**2
    )
    mask[mask_area] = 0
    
    # Apply mask
    fft_shift_filtered = fft_shift * mask
    
    # Inverse FFT
    fft_filtered = np.fft.ifftshift(fft_shift_filtered)
    img_filtered = np.fft.ifft2(fft_filtered)
    img_filtered = np.abs(img_filtered)
    
    img_out = Image.fromarray(img_filtered.astype(np.uint8), mode='L')
    update_output(img_out)

def build_filters_menu(menubar):
    
    from tkinter import Menu
    
    filters_menu = Menu(menubar, tearoff=0)
    
    # Semua filter langsung di menu utama Filter (bukan submenu)
    filters_menu.add_command(label="Filter Identity", command=filter_identity)
    
    # Edge Detection
    filters_menu.add_command(label="Edge Detection - Sobel", command=sobel_edge_detection)
    filters_menu.add_command(label="Edge Detection - Prewitt", command=prewitt_edge_detection)
    filters_menu.add_command(label="Edge Detection - Roberts", command=roberts_edge_detection)
    
    filters_menu.add_command(label="Sharpen", command=sharpen_filter)
    filters_menu.add_command(label="Gaussian Blur", command=gaussian_blur)
    filters_menu.add_command(label="Unsharp Masking", command=unsharp_masking)
    filters_menu.add_command(label="Average Filter", command=average_filter)
    filters_menu.add_command(label="Low Pass Filter", command=low_pass_filter)
    filters_menu.add_command(label="High Pass Filter", command=high_pass_filter)
    filters_menu.add_command(label="Bandstop Filter", command=bandstop_filter)
    
    menubar.add_cascade(label="Filter", menu=filters_menu)