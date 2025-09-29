import tkinter as tk
from tkinter import Toplevel, Frame, Label, Button, StringVar, OptionMenu, filedialog
from PIL import Image, ImageTk
import numpy as np

def show_arithmetical_operations():
    """Membuat form baru untuk operasi aritmetika"""
    # Buat window baru
    arith_win = Toplevel()
    arith_win.title("Aritmetical Operations")
    arith_win.geometry("600x500")
    arith_win.resizable(False, False)
    
    # Variabel untuk menyimpan gambar
    img1_pil = None
    img2_pil = None
    img_result_pil = None
    
    # Frame untuk gambar
    frame_top = Frame(arith_win)
    frame_top.pack(pady=10)
    
    frame_bottom = Frame(arith_win)
    frame_bottom.pack(pady=10)
    
    # Panel untuk gambar
    panel_img1 = Label(frame_top, bg="white", width=180, height=150, relief="solid", bd=1)
    panel_img1.grid(row=0, column=0, padx=5, pady=5)
    label_img1 = Label(frame_top, text="Input 1")
    label_img1.grid(row=1, column=0)
    
    panel_img2 = Label(frame_top, bg="white", width=180, height=150, relief="solid", bd=1)
    panel_img2.grid(row=0, column=1, padx=5, pady=5)
    label_img2 = Label(frame_top, text="Input 2")
    label_img2.grid(row=1, column=1)
    
    panel_result = Label(frame_bottom, bg="white", width=180, height=150, relief="solid", bd=1)
    panel_result.grid(row=0, column=0, padx=5, pady=5)
    label_result = Label(frame_bottom, text="Output")
    label_result.grid(row=1, column=0)
    
    # Fungsi untuk load gambar
    def load_image1():
        nonlocal img1_pil
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            img1_pil = Image.open(file_path).convert("RGB")
            img_resized = img1_pil.resize((180, 150))
            img_tk = ImageTk.PhotoImage(img_resized)
            panel_img1.config(image=img_tk)
            panel_img1.image = img_tk
    
    def load_image2():
        nonlocal img2_pil
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            img2_pil = Image.open(file_path).convert("RGB")
            img_resized = img2_pil.resize((180, 150))
            img_tk = ImageTk.PhotoImage(img_resized)
            panel_img2.config(image=img_tk)
            panel_img2.image = img_tk
    
    # Fungsi operasi aritmetika
    def perform_operation(operation):
        nonlocal img1_pil, img2_pil, img_result_pil
        
        if img1_pil is None or img2_pil is None:
            return
        
        # Pastikan kedua gambar memiliki ukuran yang sama
        img2_resized = img2_pil.resize(img1_pil.size)
        
        # Konversi ke array numpy
        arr1 = np.array(img1_pil, dtype=np.float32)
        arr2 = np.array(img2_resized, dtype=np.float32)
        
        if operation == "Addition":
            result = arr1 + arr2
            result = np.clip(result, 0, 255).astype(np.uint8)
        elif operation == "Subtraction":
            result = arr1 - arr2
            result = np.clip(result, 0, 255).astype(np.uint8)
        elif operation == "Multiplication":
            result = arr1 * arr2 / 255.0
            result = np.clip(result, 0, 255).astype(np.uint8)
        elif operation == "Division":
            # Hindari division by zero
            arr2[arr2 == 0] = 1
            result = arr1 / arr2 * 255.0
            result = np.clip(result, 0, 255).astype(np.uint8)
        elif operation == "Blend":
            result = (arr1 * 0.5 + arr2 * 0.5).astype(np.uint8)
        elif operation == "AND":
            result = np.bitwise_and(arr1.astype(np.uint8), arr2.astype(np.uint8))
        elif operation == "OR":
            result = np.bitwise_or(arr1.astype(np.uint8), arr2.astype(np.uint8))
        elif operation == "XOR":
            result = np.bitwise_xor(arr1.astype(np.uint8), arr2.astype(np.uint8))
        else:
            return
        
        img_result_pil = Image.fromarray(result)
        
        # Tampilkan hasil
        img_resized = img_result_pil.resize((180, 150))
        img_tk = ImageTk.PhotoImage(img_resized)
        panel_result.config(image=img_tk)
        panel_result.image = img_tk
    
    # Frame untuk tombol
    frame_buttons = Frame(arith_win)
    frame_buttons.pack(pady=10)
    
    # Tombol load gambar
    btn_load1 = Button(frame_buttons, text="Load Image 1", command=load_image1)
    btn_load1.grid(row=0, column=0, padx=5)
    
    btn_load2 = Button(frame_buttons, text="Load Image 2", command=load_image2)
    btn_load2.grid(row=0, column=1, padx=5)
    
    # Frame untuk operasi
    frame_operations = Frame(arith_win)
    frame_operations.pack(pady=10)
    
    # Dropdown untuk memilih operasi
    operations = ["Addition", "Subtraction", "Multiplication", "Division", "Blend", "AND", "OR", "XOR"]
    selected_operation = StringVar(arith_win)
    selected_operation.set(operations[0])
    
    Label(frame_operations, text="Operation:").grid(row=0, column=0, padx=5)
    op_menu = OptionMenu(frame_operations, selected_operation, *operations)
    op_menu.grid(row=0, column=1, padx=5)
    
    btn_apply = Button(frame_operations, text="Apply Operation", 
                      command=lambda: perform_operation(selected_operation.get()))
    btn_apply.grid(row=0, column=2, padx=5)
    
    # Tombol save hasil
    def save_result():
        if img_result_pil is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                img_result_pil.save(file_path)
    
    btn_save = Button(frame_operations, text="Save Result", command=save_result)
    btn_save.grid(row=0, column=3, padx=5)

def build_arithmetic_menu(menubar):
    """Membuat menu Aritmetical Operation"""
    from tkinter import Menu
    arithmetic_menu = Menu(menubar, tearoff=0)
    arithmetic_menu.add_command(label="Open Arithmetic Operations", command=show_arithmetical_operations)
    menubar.add_cascade(label="Aritmetical Operation", menu=arithmetic_menu)