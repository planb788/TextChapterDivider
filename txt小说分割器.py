import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class NumberPad:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.geometry('180x240')  # 修改窗口大小
        
        self.entry = tk.Entry(self.top, width=8, justify='center')
        self.entry.pack(pady=20)

        btns_frame = tk.Frame(self.top)
        btns_frame.pack(side=tk.BOTTOM)

        # 创建按钮
        for i in range(9):
            btn = tk.Button(btns_frame, width=5, height=1, text=str(i+1), command=lambda i=i: self.entry.insert(tk.END, str(i+1)))
            btn.grid(row=i//3, column=i%3)

        zero_btn = tk.Button(btns_frame, width=5, height=1, text='0', command=lambda: self.entry.insert(tk.END, '0'))
        zero_btn.grid(row=3, column=0)

        clear_btn = tk.Button(btns_frame, width=5, height=1, text='清除', command=lambda: self.entry.delete(0, tk.END))
        clear_btn.grid(row=3, column=1)

        ok_btn = tk.Button(btns_frame, width=5, height=1, text='确定', command=self.set_chapters)
        ok_btn.grid(row=3, column=2)
            
    def set_chapters(self):
        chapters = self.entry.get()
        if chapters.isdigit() and 0 < int(chapters) <= 1000:
            chapters_per_file_label.config(text=f'每个文件章节数: {chapters}')
            self.top.destroy()
        else:
            messagebox.showerror("错误", "数字必须在1到1000之间")
            
def set_chapters_per_file():
    NumberPad(root)
    
def split_novel(input_file, output_dir, chapters_per_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 检测章节标题及其内容
    chapter_contents = re.findall(r'(第[\d一二三四五六七八九十百千]+章[\s\S]*?)(?=第[\d一二三四五六七八九十百千]+章|$)', content)
    
    # 使用os.path.basename()函数获取文件名，用于给分割后的文件命名
    file_name = os.path.basename(input_file)
    file_name_without_ext = os.path.splitext(file_name)[0]

    # 按照每8章一个txt文件进行分割
    for i in range(0, len(chapter_contents), chapters_per_file):
        end = i + chapters_per_file
        filename = f"{output_dir}/{file_name_without_ext}{i // chapters_per_file + 1}.txt"
        with open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(chapter_contents[i:end]))
            
    # 执行成功后，弹出提示
    messagebox.showinfo("提示", "执行成功！")

def browse_input_file():
    filename = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(tk.END, filename)

def browse_output_dir():
    dirname = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(tk.END, dirname)

def start_split():
    input_file = input_file_entry.get()
    output_dir = output_dir_entry.get()
    chapters_per_file = int(chapters_per_file_label.cget('text').split(': ')[1])  # 从 label 文本获取章节数
    if not input_file.lower().endswith('.txt'):
        messagebox.showerror("错误", "输入文件必须是.txt格式")
    else:
        split_novel(input_file, output_dir, chapters_per_file) 

root = tk.Tk()
root.title("txt小说分割器")
root.geometry("300x260")

input_file_label = tk.Label(root, text="输入文件:")
input_file_label.pack()
input_file_entry = tk.Entry(root)
input_file_entry.pack()
input_file_button = tk.Button(root, text="浏览...", command=browse_input_file)
input_file_button.pack()

output_dir_label = tk.Label(root, text="输出目录:")
output_dir_label.pack()
output_dir_entry = tk.Entry(root)
output_dir_entry.pack()
output_dir_button = tk.Button(root, text="浏览...", command=browse_output_dir)
output_dir_button.pack()

chapters_per_file_label = tk.Label(root, text="每个文件章节数: 8")  # 初始化为8
chapters_per_file_label.pack()
chapters_per_file_button = tk.Button(root, text="设置...", command=set_chapters_per_file)
chapters_per_file_button.pack()

start_button = tk.Button(root, text="开始", command=start_split)
start_button.pack()

root.mainloop()