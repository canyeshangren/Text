import pygame
import re
import pyodbc
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
# from tkinter import font
# 第一行显示当前时间，年月日，星期几，随时间的变化而变化，添加功能计时器，设置一个倒计时，添加撤回功能
# 需求：tkinter库，pygame库，odbc库，sql server数据库，一个mp3格式文件
# 修改到本地的话只需要将create_connection内连接重新写一次，再把Clock类里的__init__文件里的self.music的地址改到自己的地址即可
# 数据库，只需要创建5个表，text1,text2,text3,text4,dict,text1~4对应的表需要两个列，
# time列和things列（这个列名随便改，但是time不能改，改了就要到open_file1里面修改sql语句）
# dict表需要创建word和value两个列，须将词典导入，我另外写了一个python程序往里面导入，
# 要注意的是通过游标往里面放单词的时候需要把末尾的换行符去掉，不然不能select到正确的value


def create_connection():
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=国哥\\SQL111;DATABASE=text;UID=sa;PWD=123456')
    return connection  # 连接数据库之后返回一个连接用于创建游标


def change_area1(event):
    _ = event  # 去除“未使用形参 'event' 的值”的警告，表示我们知道有这么个参数，但不需要使用
    editor = TextEditor(root, 1)
    editor.open_file1(1)  # 这里的四个函数用于打开对应的区域


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
    but1 = tk.Button(root, text="紧急且重要", font=('Courier', 35))
    but1.place(x=0, y=0, width=300, height=200)
    but2 = tk.Button(root, text="紧急不重要", font=('Courier', 35))
    but2.place(x=300, y=0, width=300, height=200)
    but3 = tk.Button(root, text="重要不紧急", font=('Courier', 35))
    but3.place(x=0, y=200, width=300, height=200)
    but4 = tk.Button(root, text="不重要不紧急", font=('Courier', 35))
    but4.place(x=300, y=200, width=300, height=200)

    but1.bind('<Button-1>', change_area1)
    but2.bind('<Button-1>', change_area2)
    but3.bind('<Button-1>', change_area3)
    but4.bind('<Button-1>', change_area4)
    # 这里是主页面按钮的创建


class Clock:
    def __init__(self, master):
        self.windows = tk.Toplevel(master)
        self.windows.geometry("400x300")
        self.windows.title("计时器")
        self.h = tk.StringVar()
        self.m = tk.StringVar()
        self.s = tk.StringVar()  # 时分秒的声明，设定为这样的可变的字符串类型就方便后续的更新了

        pygame.init()
        self.music = "D:\\逃跑音频库\\Angie Miller - This Is the Life.mp3"
        self.music_flag = False  # 判断音乐是否播放，默认是未播放
        pygame.mixer.music.load(self.music)  # 加载音频文件

        self.Running = False  # 判断是否开始计时,True代表开始计时
        self.flag = False  # 判断是倒计时还是正计时,True代表正计时
        self.time_count = 0
        self.h.set("00")
        self.m.set("00")
        self.s.set("00")  # 初始化各种数据，时分秒全部设定为0
        self.h_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_h)
        self.h_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_h)
        self.m_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_m)
        self.m_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_m)
        self.s_add = tk.Button(self.windows, text='>', font=("Helvetica", 16), command=self.add_s)
        self.s_minus = tk.Button(self.windows, text='<', font=("Helvetica", 16), command=self.minus_s)  # 加减计时器时间按钮的创建
        self.start = tk.Button(self.windows, text="开始", font=("Helvetica", 20), command=self.start1)
        self.pause = tk.Button(self.windows, text="暂停", font=("Helvetica", 20), command=self.pause1)
        self.stop = tk.Button(self.windows, text="重置", font=("Helvetica", 20), command=self.stop1)
        # 诸多按钮的声明，并绑定对应的函数
        self.showtime()
        # 显示时间以及各个按钮

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
        # 以中心为坐标原点，左右上下移动来放置这些组件
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
        self.time_count += 600
        self.update()

    def minus_m(self):
        if self.time_count >= 300:
            self.time_count -= 300
        self.update()

    def add_s(self):
        self.time_count += 1
        self.update()

    def minus_s(self):
        if self.time_count >= 1:
            self.time_count -= 1
        self.update()
    # 对应的6个按钮，分别对应时分秒的增加和减少

    def start1(self):
        self.Running = True
        if not self.flag and self.time_count == 0:
            self.flag = True
        self.start.config(state='disabled')
        self.h_add.config(state='disabled')
        self.h_minus.config(state='disabled')
        self.m_add.config(state='disabled')
        self.m_minus.config(state='disabled')
        self.s_add.config(state='disabled')
        self.s_minus.config(state='disabled')
        # 将这些按钮禁用,避免出现报告内提到的重复调用update函数
        self.update()

    def pause1(self):
        self.Running = False
        self.start.config(state='normal')  # 只需要恢复开始键的按钮状态即可
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
        if self.music_flag:
            pygame.mixer.music.stop()
            self.music_flag = False  # 按下停止按钮后,就会将音乐停止,以及各个按钮都会恢复成初始状态
        self.update()

    def update(self):
        if self.Running:
            if self.flag:  # 如果是正计时就每秒让time_count加1
                self.time_count += 1
                self.windows.after(1000, self.update)  # 每隔1s自动调用本函数
            elif self.time_count > 0:
                self.time_count -= 1
                self.windows.after(1000, self.update)
            elif self.time_count == 0:
                pygame.mixer.music.play()  # 倒计时为0时播放音乐
                self.music_flag = True
                self.Running = False
        self.h.set(str(int(self.time_count / 3600)).zfill(2))
        self.m.set(str(int((self.time_count % 3600) / 60)).zfill(2))
        self.s.set(str(int(self.time_count % 60)).zfill(2))
        # 显示时分秒


class Dictionary:
    def __init__(self, master):
        self.windows = tk.Toplevel(master)
        self.windows.geometry("300x200")
        self.windows.title("英汉字典")
        self.search = tk.Button(self.windows, text="搜索", width=8, height=2, command=self.search1)
        self.entry = tk.Entry(self.windows)
        self.label = tk.Label(self.windows)
        self.place_widget()

    def place_widget(self):
        self.entry.grid(row=1, column=1)
        self.search.grid(row=1, column=2)
        self.windows.rowconfigure(0, weight=1)
        self.windows.rowconfigure(2, weight=1)
        self.windows.rowconfigure(3, weight=2)  # 使得第三行的权重为2，即第0行的高比上第2，3行的高为1:3,使布局更美观
        self.windows.columnconfigure(0, weight=1)
        self.windows.columnconfigure(2, weight=1)  # 使得第0列和第2列的权重相同，分配的空间相同，所以第1列就会在中间

    def search1(self):
        connect = create_connection()  # 连接上数据库
        cursor = connect.cursor()  # 创建游标
        text = self.entry.get()  # 获得单行文本框里的内容
        cursor.execute('select value from dict ' +
                       f'where word=\'{text}\';')
        result = cursor.fetchall()  # 返回对应单词的意思
        result_str = tk.StringVar()
        if len(result) != 0:  # 判断是否找到了对应的意思,如果没有显示未找到该单词
            result_str.set(result[0][0])
        else:
            result_str.set('未找到对应单词的意思')
        self.label.config(textvariable=result_str)
        self.label.grid(row=2, column=1)


class TextEditor:
    def __init__(self, master, area):
        self.master = master
        self.master.resizable(True, True)  # 使得整个界面是可调节的
        self.master.title("Text Editor")
        self.text = tk.Text(self.master, font=('Helvetica', 18))
        self.text.pack(fill='both', expand=False)  # 使得文本框填充满整个窗口
        self.menu = tk.Menu(self.master)  # 创建主菜单
        self.create_menu()
        self.file_name = None  # 初始化声明一个文件名
        # self.font1 = font.Font(family='Helvetica', size=14, weight='bold')
        self.area = area
        self.flag = False  # 代表是否置顶
        self.time = datetime.datetime.now()
        self.undo_stack = []
        self.undo_stack_limit = 10  # 代表着撤回的最高次数
        self.text.bind("<BackSpace>", self.undo_limit)  # 绑定撤回操作,当按下回车进行删除的时候,先保存
        tk.messagebox.showinfo("提示", "请按照一行时间+多行记录的形式输入要记录的事件")
        # 显示使用提示,凸显人性化

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
        # 上面是文件菜单,及其子菜单的设定
        edit_menu = tk.Menu(self.menu)
        edit_menu.add_command(label="裁剪", command=self.cut, accelerator='Ctrl+x')
        edit_menu.add_command(label="复制", command=self.copy, accelerator='Ctrl+c')
        edit_menu.add_command(label="粘贴", command=self.paste, accelerator='Ctrl+v')
        # 这三个不需要绑定快捷键,因为这三个的快捷键是windows系统自带的,如果绑了会导致翻倍效果,比如你只复制了"哈哈"两个字,粘贴会显示四个"哈"字
        edit_menu.add_command(label="置顶", command=self.topmost, accelerator='按2次取消')
        edit_menu.add_command(label="撤回", command=self.undo, accelerator='Ctrl+z')
        self.master.bind('<Control-z>', lambda event: self.undo())
        self.menu.add_cascade(label="编辑", menu=edit_menu)
        # 上面是编辑菜单,及其菜单内容的设置
        self.menu.add_command(label="返回", command=self.hidden)
        self.menu.add_command(label="计时器", command=self.create_time)
        self.menu.add_command(label="英汉字典", command=self.create_dictionary)
        self.master.config(menu=self.menu)  # 绑定主菜单的位置

    # @staticmethod  一开始并未使用到self.time设置了一个静态,然后后面用self.time来获取当前时间就去掉了
    def time_normalization(self, content):
        data = content.split()  # 将所以时间分隔开,日期和时分秒分开
        # print(data)  # 开启此输出可展示提取时间等信息
        if not data:
            return  # 如果进来的是空值,返回
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
            return a+f' {self.time.hour}:{self.time.minute}:{self.time.second}'
        # else:
        #     tk.messagebox.showinfo('错误提醒',
        #                            '请按照yyyy-mm-dd hh:mm:ss的格式来添加时间，冒号需使用英文\n'
        #                            '只填写日期，或者几点几分也是可以的,如mm-dd,或者是hh:mm')
        # 修改后的代码将不会触发这个错误提醒

    def new_file(self):
        self.undo_limit()
        self.text.delete(1.0, tk.END)
        self.file_name = None
        # 清空文本框里的内容就相当于打开了新页面,注意还要把文件名也变为None不然会保存到原来那个文件里

    def open_file(self):
        file_name = filedialog.askopenfilename()  # 使用这个函数获取文件名
        if file_name:
            self.undo_limit()
            with open(file_name, "r") as f:
                file_contents = f.read()
            self.text.delete(1.0, tk.END)  # 清空文本然后插入打开文件的内容
            self.text.insert(tk.END, file_contents)
            self.file_name = file_name

    def open_file1(self, s):
        self.undo_limit()
        self.area = s
        self.master.title(f"{s}号区域")
        connect = create_connection()
        cursor = connect.cursor()
        cursor.execute('select * from text'+f'{s}'+' order by time asc')  # 查找数据库中的数据
        self.text.delete(1.0, tk.END)
        for row in cursor:
            self.text.insert(tk.END, f"{row[0]}:\n{row[1]}")  # 将数据库里的内容插入到文本框内
        connect.close()  # 关闭连接

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
        content = re.split(r'((?:\d{2,4}-)?\d{1,2}-\d{1,2}\s?|\d{1,2}:\d{1,2}(?::\d{1,2}:?)?\s?)', content1)
        # 将文本切割成不同部分,以时间为分隔,方便后续的处理
        i = 0
        while i < len(content):  # 遍历整个备忘录
            match = re.search(r'((?:\d{2,4}-)?\d{1,2}-\d{1,2}\s?|\d{1,2}:\d{1,2}(?::\d{1,2}:?)?\s?)',
                              content[i])  # 匹配日期时间
            if match and content[i+1] == '':  # 这里是我看了content输出的写法,时间后面有一个空格代表既有日期又有时分
                str1 = self.time_normalization(content[i]+content[i+2])  # 对时间进行归一化处理
                cursor.execute("insert into text" + f"{self.area} values ('{str1}','{content[i + 3]}')")
                # 将时间和事件插入数据库
                i += 3
            elif match:
                str1 = self.time_normalization(content[i])  # 同上
                cursor.execute("insert into text" + f"{self.area} values ('{str1}','{content[i + 1]}')")
                i += 1
            i += 1
        connect.commit()  # 这里是保存数据库的修改
        connect.close()  # 关闭数据库

    def save_file_as(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_name:
            self.file_name = file_name
            self.save_file()

    def cut(self):
        self.undo_limit()
        self.text.event_generate("<<Cut>>")
        # 剪切文本框内的文本

    def copy(self):
        self.text.event_generate("<<Copy>>")
        # 复制文本框内的文本

    def paste(self):
        self.undo_limit()
        self.text.event_generate("<<Paste>>")
        # 粘贴之前要把内容压入撤回的栈里

    def hidden(self):
        self.text.pack_forget()  # 隐藏text组件
        # self.menu.delete(0, 'end')
        self.master.title("备忘录")
        self.master.geometry("600x400")  # 将改变后的恢复到原来的大小，防止按不到按钮
        create_button()
        # 重新创建按钮,如果不这样的话,那些按钮会变得不对齐,我也不知道为什么,但是加了这句就可以避免了
        self.master.resizable(False, False)  # 控制主窗口大小不可变

    def topmost(self):
        self.flag = not self.flag
        self.master.attributes("-topmost", self.flag)  # 使得该窗口置顶状态发生改变

    def undo(self):
        if self.undo_stack:
            self.undo_stack_limit += 1
            self.text.delete(1.0, tk.END)
            text = self.undo_stack.pop()
            self.text.insert(tk.END, text)
        else:
            tk.messagebox.showinfo("提示", "已经无法撤回更前操作")
    # 将撤回栈里栈顶的数据弹出来

    def undo_limit(self, event=None):
        _ = event
        if self.undo_stack_limit == 0:
            self.undo_stack.pop(0)
            self.undo_stack_limit += 1
        self.undo_stack_limit -= 1
        self.undo_stack.append(self.text.get("1.0", tk.END).rstrip())
    # 将文本框里面的内容压入撤回栈中,同时限制撤回栈的元素数量,如果超出,就弹出栈底的那个元素

    def create_time(self):
        clock = Clock(self.master)
        _ = clock
    # 打开计时器组件

    def create_dictionary(self):
        dict1 = Dictionary(self.master)
        _ = dict1
    # 打开英汉字典组件


if __name__ == '__main__':
    root = tk.Tk()
    root.title("备忘录")
    width, height = 600, 400  # 设置根窗口宽和高
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()  # 获取电脑屏幕的宽和高，便于将窗口放在正中间
    AlignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(AlignStr)
    root.resizable(False, False)  # 因为按钮大小固定了，为了不被发现，禁止改变宽和高
    create_button()  # 创建按钮
    root.mainloop()  # 监视整个主页面的变动并更新
