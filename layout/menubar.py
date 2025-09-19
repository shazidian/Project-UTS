import tkinter as tk
from tkinter import Menu
from fungsi import file_ops, histogram, colors

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

    return menubar
