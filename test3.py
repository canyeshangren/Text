import tkinter
import re
import pyodbc
# import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
# 第一行显示当前时间，年月日，星期几，随时间的变化而变化，添加功能计时器，设置一个倒计时，添加撤回功能


def create_connection():
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=国哥\\SQL111;DATABASE=text;UID=sa;PWD=123456')
    return connection


def change_area1(event):
    _ = event  # 去除“未使用形参 'event' 的值”的警告，表示我们知道有这么个参数，但不需要使用
    editor = TextEditor(root, 1)
    editor.open_file1(1)


def change_area2(event):
    _ = event
    editor = TextEditor(root, 2)
    editor.open_file1(2)


def change_area3(event):
    _ = event
    editor = TextEditor(root, 3)
    editor.open_file1(3)


def change_area4(event):
    _ = event
    editor = TextEditor(root, 4)
    editor.open_file1(4)


def create_button():
    but1 = tkinter.Button(root, text="紧急且重要", font=('Courier', 35))
    but1.place(x=0, y=0, width=300, height=200)
    but2 = tkinter.Button(root, text="紧急不重要", font=('Courier', 35))
    but2.place(x=300, y=0, width=300, height=200)
    but3 = tkinter.Button(root, text="重要不紧急", font=('Courier', 35))
    but3.place(x=0, y=200, width=300, height=200)
    but4 = tkinter.Button(root, text="不重要不紧急", font=('Courier', 35))
    but4.place(x=300, y=200, width=300, height=200)

    but1.bind('<Button-1>', change_area1)
    but2.bind('<Button-1>', change_area2)
    but3.bind('<Button-1>', change_area3)
    but4.bind('<Button-1>', change_area4)


class Clock:
    def __init__(self, master):
        self.windows = tk.Toplevel(master)
        self.windows.geometry("400x300")
        self.windows.title("计时器")
        self.h = tk.StringVar()
        self.m = tk.StringVar()
        self.s = tk.StringVar()
        self.Running = False  # 判断是否开始计时,True代表开始计时
        self.flag = False  # 判断是倒计时还是正计时,True代表正计时
        self.time_count = 0
        self.h.set("00")
        self.m.set("00")
        self.s.set("00")
        self.h_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_h)
        self.h_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_h)
        self.m_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_m)
        self.m_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_m)
        self.s_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_s)
        self.s_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_s)  # 加减计时器时间按钮的创建
        self.start = tk.Button(self.windows, text="开始", font=("Helvetica", 20), command=self.start1)
        self.pause = tk.Button(self.windows, text="暂停", font=("Helvetica", 20), command=self.pause1)
        self.stop = tk.Button(self.windows, text="重置", font=("Helvetica", 20), command=self.stop1)
        self.showtime()

    def showtime(self):
        h_label = tk.Label(self.windows, textvariable=self.h, font=("Helvetica", 48))
        m_label = tk.Label(self.windows, textvariable=self.m, font=("Helvetica", 48))
        s_label = tk.Label(self.windows, textvariable=self.s, font=("Helvetica", 48))  # 时分秒标签的创建
        colon1 = tk.Label(self.windows, text=':', font=("Helvetica", 48))
        colon2 = tk.Label(self.windows, text=':', font=("Helvetica", 48))  # 两个冒号的创建

        self.start.place(relx=0.5, rely=0.5, anchor='center', x=-100, y=-80, width=60, height=50)
        self.pause.place(relx=0.5, rely=0.5, anchor='center', y=-80, width=60, height=50)
        self.stop.place(relx=0.5, rely=0.5, anchor='center', x=100, y=-80, width=60, height=50)
        self.h_add.place(relx=0.5, rely=0.5, anchor='center', x=-80, y=60, width=20, height=20)
        self.h_minus.place(relx=0.5, rely=0.5, anchor='center', x=-120, y=60, width=20, height=20)
        self.m_add.place(relx=0.5, rely=0.5, anchor='center', x=20, y=60, width=20, height=20)
        self.m_minus.place(relx=0.5, rely=0.5, anchor='center', x=-20, y=60, width=20, height=20)
        self.s_add.place(relx=0.5, rely=0.5, anchor='center', x=120, y=60, width=20, height=20)
        self.s_minus.place(relx=0.5, rely=0.5, anchor='center', x=80, y=60, width=20, height=20)

        h_label.place(relx=0.5, rely=0.5, anchor='center', x=-100)
        m_label.place(relx=0.5, rely=0.5, anchor='center')
        s_label.place(relx=0.5, rely=0.5, anchor='center', x=100)
        colon1.place(relx=0.5, rely=0.5, anchor='center', x=-50)
        colon2.place(relx=0.5, rely=0.5, anchor='center', x=50)  # 所有组件的布局设置

    def add_h(self):
        self.time_count += 3600
        self.update()

    def minus_h(self):
        if self.time_count >= 3600:
            self.time_count -= 3600
        self.update()

    def add_m(self):
        self.time_count += 60
        self.update()

    def minus_m(self):
        if self.time_count >= 60:
            self.time_count -= 60
        self.update()

    def add_s(self):
        self.time_count += 1
        self.update()

    def minus_s(self):
        if self.time_count >= 1:
            self.time_count -= 1
        self.update()

    def start1(self):
        self.Running = True
        if not self.flag and self.time_count == 0:
            self.flag = True
        # if self.time_count != 0:
        #     self.flag = False
        # else:
        #     self.flag = True
        self.start.config(state='disabled')
        self.h_add.config(state='disabled')
        self.h_minus.config(state='disabled')
        self.m_add.config(state='disabled')
        self.m_minus.config(state='disabled')
        self.s_add.config(state='disabled')
        self.s_minus.config(state='disabled')

        self.update()

    def pause1(self):
        self.Running = False
        self.start.config(state='normal')
        self.update()

    def stop1(self):
        self.Running = False
        self.flag = False
        self.time_count = 0
        self.start.config(state='normal')
        self.h_add.config(state='normal')
        self.h_minus.config(state='normal')
        self.m_add.config(state='normal')
        self.m_minus.config(state='normal')
        self.s_add.config(state='normal')
        self.s_minus.config(state='normal')
        self.update()

    def update(self):
        if self.Running:
            if self.flag:
                self.time_count += 1
                self.windows.after(1000, self.update)
            elif self.time_count > 0:
                self.time_count -= 1
                self.windows.after(1000, self.update)
        self.h.set(str(int(self.time_count / 3600)).zfill(2))
        self.m.set(str(int((self.time_count % 3600) / 60)).zfill(2))
        self.s.set(str(int(self.time_count % 60)).zfill(2))
        print(self.time_count)


class TextEditor:
    def __init__(self, master, area):
        self.master = master
        self.master.resizable(True, True)
        self.master.title("Text Editor")
        self.text = tk.Text(self.master, font=('Helvetica', 18))
        self.text.pack(fill='both', expand=False)
        self.menu = tk.Menu(self.master)
        self.create_menu()
        self.file_name = None
        self.font1 = font.Font(family='Helvetica', size=14, weight='bold')
        self.area = area
        self.flag = False  # 代表，是否置顶
        # self.time = datetime.datetime.now()
        self.undo_stack = []
        self.undo_stack_limit = 5  # 代表着撤回的最高次数
        self.text.bind("<BackSpace>", self.undo_limit)
        tk.messagebox.showinfo("提示", "请按照一行时间+多行记录的形式输入要记录的事件")

    def create_menu(self):
        file_menu = tk.Menu(self.menu, tearoff=False)
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
        self.menu.add_cascade(label="文件", menu=file_menu)

        edit_menu = tk.Menu(self.menu)
        edit_menu.add_command(label="裁剪", command=self.cut, accelerator='Ctrl+x')
        edit_menu.add_command(label="复制", command=self.copy, accelerator='Ctrl+c')
        edit_menu.add_command(label="粘贴", command=self.paste, accelerator='Ctrl+v')
        edit_menu.add_command(label="置顶", command=self.topmost, accelerator='按2次取消')
        edit_menu.add_command(label="撤回", command=self.undo, accelerator='Ctrl+z')
        self.master.bind('<Control-z>', lambda event: self.undo())
        self.menu.add_cascade(label="编辑", menu=edit_menu)

        self.menu.add_command(label="返回", command=self.hidden)
        self.menu.add_command(label="计时器", command=self.create_time)
        self.master.config(menu=self.menu)

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
        # else:
        #     tk.messagebox.showinfo('错误提醒',
        #                            '请按照yyyy-mm-dd hh:mm:ss的格式来添加时间，冒号需使用英文\n'
        #                            '只填写日期，或者几点几分也是可以的,如mm-dd,或者是hh:mm')
        # 修改后的代码将不会触发这个错误提醒

    def new_file(self):
        self.undo_limit()
        self.text.delete(1.0, tk.END)

    def open_file(self):
        file_name = filedialog.askopenfilename()
        if file_name:
            with open(file_name, "r") as f:
                file_contents = f.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, file_contents)
            self.file_name = file_name
            self.undo_limit()

    def open_file1(self, s):
        self.area = s
        self.master.title(f"{s}号区域")
        connect = create_connection()
        cursor = connect.cursor()
        cursor.execute('select * from text'+f'{s}'+' order by time asc')
        self.text.delete(1.0, tk.END)
        for row in cursor:
            self.text.insert(tk.END, f"{row[0]}:\n{row[1]}")
        connect.close()
        self.undo_limit()

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
        self.undo_limit()
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.undo_limit()
        self.text.event_generate("<<Paste>>")

    def hidden(self):
        self.text.pack_forget()  # 隐藏text组件
        # self.menu.delete(0, 'end')
        self.master.title("备忘录")
        self.master.geometry("600x400")  # 将改变后的恢复到原来的大小，防止按不到按钮
        create_button()
        self.master.resizable(False, False)  # 控制主窗口大小不可变

    def topmost(self):
        self.flag = not self.flag
        self.master.attributes("-topmost", self.flag)

    def undo(self):
        if self.undo_stack:
            self.undo_stack_limit += 1
            self.text.delete(1.0, tk.END)
            text = self.undo_stack.pop()
            self.text.insert(tk.END, text)
        else:
            tk.messagebox.showinfo("提示", "已经无法撤回更前操作")

    def undo_limit(self, event=None):
        _ = event
        if self.undo_stack_limit == 0:
            self.undo_stack.pop(0)
            self.undo_stack_limit += 1
        self.undo_stack_limit -= 1
        self.undo_stack.append(self.text.get("1.0", tk.END).rstrip())

    def create_time(self):
        clock = Clock(self.master)
        _ = clock


if __name__ == '__main__':
    root = tk.Tk()
    root.title("备忘录")
    width, height = 600, 400  # 设置根窗口宽和高
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()  # 获取电脑屏幕的宽和高，便于将窗口放在正中间
    AlignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(AlignStr)
    root.resizable(False, False)  # 因为按钮大小固定了，为了不被发现，禁止改变宽和高
    create_button()
    root.mainloop()
