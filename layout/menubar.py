import tkinter as tk
from tkinter import Menu, Toplevel, Label
from fungsi import arithmetic_ops, file_ops, histogram, colors, image_processing, filters


def show_about(root):
    about_win = Toplevel(root)
    about_win.title("Tentang Aplikasi")
    about_win.geometry("300x150")
    about_win.resizable(False, False)

    Label(about_win, text="Nama Aplikasi: Image Processing Tool", font=("Arial", 11)).pack(pady=10)
    Label(about_win, text="Versi: 1.0.0", font=("Arial", 11)).pack(pady=5)
    Label(about_win, text="Dibuat oleh: Diana", font=("Arial", 11)).pack(pady=5)


def create_menubar(root):
    menubar = Menu(root)

    # === FILE ===
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Buka", command=file_ops.open_file)
    file_menu.add_command(label="Simpan", command=file_ops.save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Keluar", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # === VIEW ===
    view_menu = Menu(menubar, tearoff=0)
    histogram_menu = Menu(view_menu, tearoff=0)
    histogram_menu.add_command(label="Input", command=histogram.histogram_input)
    histogram_menu.add_command(label="Output", command=histogram.histogram_output)
    histogram_menu.add_command(label="Input & Output", command=histogram.histogram_both)
    view_menu.add_cascade(label="Histogram", menu=histogram_menu)
    menubar.add_cascade(label="View", menu=view_menu)

    # === COLORS ===
    colors.build_colors_menu(menubar)

    # === ABOUT ===
    menubar.add_command(label="Tentang", command=lambda: show_about(root))
    
    # === IMAGE PROCESSING ===
    image_processing.build_image_processing_menu(menubar)
    
   # === ARITHMETICAL OPERATION ===
    arithmetic_ops.build_arithmetic_menu(menubar)
    
    # === FILTER ===
    filters.build_filters_menu(menubar)

    return menubar
