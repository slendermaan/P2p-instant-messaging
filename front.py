import json
from tkinter import Tk, StringVar, Radiobutton

root = Tk()
root.title('聊天窗口')
root.geometry('450x450')  # 这里的乘号不是 * ，而是小写英文字母 x
def get_friendlist():
    with open('ip_name.txt', "r") as f:
        msg = f.read()
        f.close()
    msg = json.loads(msg)
    return msg
friendlist = get_friendlist()
var = StringVar()
for key in friendlist:
    rd1 = Radiobutton(root, text=friendlist[key], variable=var, font=('微软雅黑', 8), value=key)
    rd1.pack()
root.mainloop()