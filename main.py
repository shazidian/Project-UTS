import tkinter as tk
from layout.menubar import create_menubar
from fungsi import file_ops


# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Form1")
root.geometry("800x400")

# ================= FRAME PANEL =================
frame_left = tk.Frame(root, bg="white", width=390, height=350, relief="solid", bd=1)
frame_left.place(x=5, y=5)

frame_right = tk.Frame(root, bg="white", width=390, height=350, relief="solid", bd=1)
frame_right.place(x=405, y=5)

# Panel kosong
# file_ops.panel_left = tk.Label(frame_left, bg="white")
# file_ops.panel_left.pack(expand=True, fill="both")

# file_ops.panel_right = tk.Label(frame_right, bg="white")
# file_ops.panel_right.pack(expand=True, fill="both")
# Panel kosong dengan ukuran tetap
file_ops.panel_left = tk.Label(frame_left, bg="white", width=380, height=340)
file_ops.panel_left.place(x=0, y=0, width=380, height=340)

file_ops.panel_right = tk.Label(frame_right, bg="white", width=380, height=340)
file_ops.panel_right.place(x=0, y=0, width=380, height=340)


# ================= STATUS BAR =================
status_frame = tk.Frame(root, relief="sunken", bd=1)
status_frame.pack(side="bottom", fill="x")

label1 = tk.Label(status_frame, text="toolStripStatusLabel1")
label1.pack(side="left")

label2 = tk.Label(status_frame, text="toolStripStatusLabel2")
label2.pack(side="left", padx=10)

# ================= MENUBAR =================
menubar = create_menubar(root)
root.config(menu=menubar)

# ================= RUN =================
root.mainloop()
