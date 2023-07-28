import tkinter as tk

root = tk.Tk()
root.geometry('800x800')

root.title("Frames Example")

# 创建上方Frame
frame_top = tk.Frame(root, bg="red", width=800, height=200)
frame_top.pack(side=tk.TOP)

# 创建下方Frame
frame_bottom = tk.Frame(root, bg="blue", width=800, height=200)
frame_bottom.pack(side=tk.BOTTOM)

# 创建左侧Frame
frame_left = tk.Frame(root, bg="green", width=200, height=400)
frame_left.pack(side=tk.LEFT)

# 创建右侧Frame
frame_right = tk.Frame(root, bg="yellow", width=200, height=400)
frame_right.pack(side=tk.RIGHT)

# 创建中间Frame
frame_center = tk.Frame(root, bg="orange", width=400, height=400)
frame_center.pack(side=tk.TOP)

root.mainloop()
