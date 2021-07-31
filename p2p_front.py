import json
import threading
import tkinter
import p2p
from tkinter import *
friend_name = ""

def start_rec():
    s = threading.Thread(target=p2p.crea_ser)
    s.start()


def get_friendlist():
    with open('ip_name.txt', "r") as f:
        msg = f.read()
        f.close()
    msg = json.loads(msg)
    return msg


def init_message():
    msg = ''
    with open('ip_message.txt', "w") as f:
        f.write(msg)
        f.close()


def main():
    start_rec()
    root = Tk()
    root.title('聊天窗口')
    root.geometry('450x450')  # 这里的乘号不是 * ，而是小写英文字母 x
    init_message()
    friendlist = get_friendlist()


    def select_member():
        p2p.change_now_ip(var.get())
        p2p.key_consult_transmit(p2p.get_now_ip())
        # p2p.change_now_ip(friendlist[var.get()])
        # p2p.key_consult_transmit(friendlist[var.get()])
        s = "您正在和" + friendlist[var.get()] + "通信"
        change_now_member()
        getmessage()
        lb.config(text=s)

    lb = Label(root)
    lb.pack()
    lb2 = Label(root)
    lb2.pack()
    var = StringVar()
    for key in friendlist:
        rd1 = Radiobutton(root, text=friendlist[key], variable=var, font=('微软雅黑', 8), value=key, command=select_member)
        rd1.pack()

    def change_now_member():
        global friend_name
        friend_name = var.get()

    def getmessage():
        global friend_name
        with open('ip_message.txt', "r") as f:
            msg = f.read()
            f.close()
        if msg=='':
            s="您还没有和对方有交流，快找对方说说话吧！"
            txt.insert(END, s)
            friendmessage = {friend_name:{"2021/7/10":"这是一条加密信道哦！"}}
        else:
            friendmessage = json.loads(msg)
        txt.delete('1.0', END)
        for key in friendmessage[friend_name]:
            s = str(key) + '\n'
            txt.insert(END, s)
            s = str(friendmessage[friend_name][key]) + '\n'
            txt.insert(END, s)
        root.after(1000, getmessage)  # 每隔1s调用函数 gettime 自身获取时间

    def choose_file():
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            lb2.config(text='您选择的文件是' + filename)
            p2p.picture_tranfer(filename)
        else:
            lb2.config(text='您没有选择任何文件')

    def send_message():
        msg = inp1.get()
        p2p.message_transfer(str(msg), p2p.get_now_ip())
        select_member()

    txt = Text(root)
    txt.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.5)

    btn1 = Button(root, text='发送信息', command=send_message)
    btn1.place(relx=0.01, rely=0.85, relwidth=0.3, relheight=0.05)
    btn2 = Button(root, text='发送图片', command=choose_file)
    btn2.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.05)
    btn2 = Button(root, text='发送音频', command=p2p.voice_tranfer)
    btn2.place(relx=0.67, rely=0.85, relwidth=0.3, relheight=0.05)
    inp1 = Entry(root)
    inp1.place(relx=0.35, rely=0.9, relwidth=0.3, relheight=0.05)
    root.mainloop()


if __name__ == '__main__':
    main()
