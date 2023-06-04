import tkinter
import re
import pyodbc
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
# 第一行显示当前时间，年月日，星期几，随时间的变化而变化，添加功能计时器，设置一个倒计时，添加撤回功能


def create_connection():
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=国哥\\SQL111;DATABASE=text;UID=sa;PWD=123456')
    return connection


def change_area1(event):
    editor = TextEditor(root, 1)
    editor.open_file1(1)


def change_area2(event):
    editor = TextEditor(root, 2)
    editor.open_file1(2)


def change_area3(event):
    editor = TextEditor(root, 3)
    editor.open_file1(3)


def change_area4(event):
    editor = TextEditor(root, 4)
    editor.open_file1(4)


def create_button():
    but1 = tkinter.Button(root)
    but1['text'] = "紧急且重要"
    but1.place(x=0, y=0, width=300, height=200)
    but2 = tkinter.Button(root)
    but2['text'] = "紧急不重要"
    but2.place(x=300, y=0, width=300, height=200)
    but3 = tkinter.Button(root)
    but3['text'] = "重要不紧急"
    but3.place(x=0, y=200, width=300, height=200)
    but4 = tkinter.Button(root)
    but4['text'] = "不重要不紧急"
    but4.place(x=300, y=200, width=300, height=200)

    but1.bind('<Button-1>', change_area1)
    but2.bind('<Button-1>', change_area2)
    but3.bind('<Button-1>', change_area3)
    but4.bind('<Button-1>', change_area4)


class TextEditor:
    def __init__(self, master, area):
        self.master = master
        self.master.title("Text Editor")
        self.text = tk.Text(self.master)
        self.text.pack(fill='both', expand=True)
        self.create_menu()
        self.file_name = None
        self.font1 = font.Font(family='Helvetica', size=14, weight='bold')
        self.area = area
        self.time = datetime.datetime.now()

    def create_menu(self):
        menu = tk.Menu(self.master)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="新建", command=self.new_file, accelerator='Ctrl+n')
        self.master.bind('<Control-n>', lambda event: self.new_file())
        openfile = tk.Menu(file_menu, tearoff=False)
        openfile.add_command(label="打开1号区域", command=lambda: self.open_file1(1))
        openfile.add_command(label="打开2号区域", command=lambda: self.open_file1(2))
        openfile.add_command(label="打开3号区域", command=lambda: self.open_file1(3))
        openfile.add_command(label="打开4号区域", command=lambda: self.open_file1(4))
        openfile.add_command(label="打开文本文件", command=self.open_file, accelerator='Ctrl+o')
        self.master.bind('<Control-o>', lambda event: self.open_file())
        file_menu.add_cascade(label="打开", menu=openfile, accelerator='Ctrl+o')
        savefile = tk.Menu(file_menu, tearoff=False)
        savefile.add_command(label="保存在对应区域", command=self.save_file1, accelerator='Ctrl+s')
        self.master.bind('<Control-s>', lambda event: self.save_file1())
        savefile.add_command(label="保存为文本文件", command=self.save_file)
        file_menu.add_cascade(label="保存", menu=savefile, accelerator='Ctrl+s')
        file_menu.add_command(label="另存为", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)
        menu.add_cascade(label="文件", menu=file_menu)

        edit_menu = tk.Menu(menu)
        edit_menu.add_command(label="裁剪", command=self.cut, accelerator='Ctrl+x')
        edit_menu.add_command(label="复制", command=self.copy, accelerator='Ctrl+c')
        edit_menu.add_command(label="粘贴", command=self.paste, accelerator='Ctrl+v')
        edit_menu.add_command(label="返回", command=self.hidden)
        menu.add_cascade(label="编辑", menu=edit_menu)
        self.master.config(menu=menu)

    @staticmethod
    def time_normalization(self, content):

        data = content.split()
        # print(data)  # 开启此输出可展示提取时间等信息
        if not data:
            return
        if len(data) == 2:
            time = data[1]
            time = time.split(sep=':')
            if len(time) == 2:
                b = f'{time[0]}:{time[1]}:00'
            else:
                b = f'{time[0]}:{time[1]}:{time[2]}'
            data2 = data[0]
            data2 = data2.split(sep='-')
            if len(data2) == 2:
                a = f'2023-{data2[0]}-{data2[1]}'
            else:
                a = f'{data2[0]}-{data2[1]}-{data2[2]}'
            return a + " " + b
        elif ':' in data[0]:
            time = data[0]
            time = time.split(sep=':')
            if len(time) == 2:
                b = f'{time[0]}:{time[1]}:00'
            else:
                b = f'{time[0]}:{time[1]}:{time[2]}'
            return f'{self.time.year}-{self.time.month}-{self.time.day} '+b
        elif '-' in data[0]:
            data2 = data[0]
            data2 = data2.split(sep='-')
            if len(data2) == 2:
                a = f'2023-{data2[0]}-{data2[1]}'
            else:
                a = f'{data2[0]}-{data2[1]}-{data2[2]}'
            return a
        else:
            tk.messagebox.showinfo('错误提醒',
                                   '请按照yyyy-mm-dd hh:mm:ss的格式来添加时间，冒号需使用英文\n'
                                   '只填写日期，或者几点几分也是可以的,如mm-dd,或者是hh:mm')

    def new_file(self):
        self.text.delete(1.0, tk.END)

    def open_file(self):
        file_name = filedialog.askopenfilename()
        if file_name:
            with open(file_name, "r") as f:
                file_contents = f.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, file_contents)
            self.file_name = file_name

    def open_file1(self, s):
        self.area = s
        self.master.title(f"{s}号区域")
        # time_now = self.time.strftime('%Y-%m-%d %H:%M:%S')
        connect = create_connection()
        cursor = connect.cursor()
        cursor.execute('select * from text'+f'{s}'+' order by time asc')
        self.text.delete(1.0, tk.END)
        # self.text.insert(tk.END, f"当前时间为:{time_now}\n", self.font1)
        for row in cursor:
            self.text.insert(tk.END, f"{row[0]}:\n{row[1]}")
        connect.close()

    def save_file(self):
        if not self.file_name:
            self.save_file_as()
        else:
            with open(self.file_name, "w") as f:
                f.write(self.text.get(1.0, tk.END))

    def save_file1(self):
        connect = create_connection()
        cursor = connect.cursor()
        cursor.execute("delete from text"+f'{self.area}')
        content1 = self.text.get("1.0", tk.END)
        # content = re.findall(r'(((?:\d{2,4}-)?\d{1,2}-\d{1,2}\s?)|(?:\d{1,2}:\d{1,2}(?::\d{1,2}:?)?\s?))', content1)
        # print(content)
        content = re.split(r'((?:(?:\d{2,4}-)?\d{1,2}-\d{1,2}\s?)|(?:\d{1,2}:\d{1,2}(?::\d{1,2}:?)?\s?))', content1)
        # print(content)
        i = 0
        while i < len(content):
            match = re.search(r'((?:(?:\d{2,4}-)?\d{1,2}-\d{1,2}\s?)|(?:\d{1,2}:\d{1,2}(?::\d{1,2}:?)?\s?))',
                              content[i])
            if match and content[i+1] == '':
                str1 = self.time_normalization(self, content[i]+content[i+2])
                cursor.execute("insert into text" + f"{self.area} values ('{str1}','{content[i + 3]}')")
                i += 3
            elif match:
                str1 = self.time_normalization(self, content[i])
                cursor.execute("insert into text" + f"{self.area} values ('{str1}','{content[i + 1]}')")
                i += 1
            i += 1
        connect.commit()
        connect.close()

    def save_file_as(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_name:
            self.file_name = file_name
            self.save_file()

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def hidden(self):
        self.text.pack_forget()


    # def update_time(self):
    #     time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     self.text.delete(1.0, '2.0')  # 删除第一行之后的所有文本
    #     self.text.insert('2.0', time_now)  # 插入新的时间
    #     self.master.after(1000, self.update_time)  # 每秒钟更新一次时间


if __name__ == '__main__':
    root = tk.Tk()
    width, height = 600, 400
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    AlignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(AlignStr)

    root.attributes("-topmost", True)
    create_button()
    # editor = TextEditor(root)
    root.mainloop()
