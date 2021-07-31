import base64
import datetime
import os
import socketserver
import socket
import json
import struct
import sys
import threading
import time
import threading
import tkinter
from tkinter import simpledialog
from tkinter.simpledialog import askstring, Tk
import lsb_tq
from PIL import Image

import crp
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片
import numpy as np

file_now = ''
file_music_now = 'tem.key'


class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # 通信循环
        data = self.request[0]
        judge_message(data.decode(), self.client_address)


# --------------------------------------通信信息以及通信获取--------------------------------------------------#
def send_music(ip, filepath):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    filename = filepath
    filepath, shotname, extension = Get_FilePath_FileName_FileExt(filename)

    client_addr = (ip, 9001)
    f = open(filename, 'rb')
    count = 0
    flag = 1
    while True:
        if count == 0:
            data = bytes(shotname + extension, encoding="utf8")
            start = time.time()
            s.sendto(data, client_addr)
        data = f.read(1024)
        if str(data) != "b''":
            s.sendto(data, client_addr)
            print(str(count) + 'byte')

        else:
            s.sendto('end'.encode('utf-8'), client_addr)
            break
        data, server_addr = s.recvfrom(1024)
        count += 1
    print('recircled' + str(count))
    s.close
    end = time.time()
    print('cost' + str(round(end - start, 2)) + 's')


def receive_music():
    count = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (get_host_ip(), 9001)
    s.bind(server_addr)

    print('Bind UDP on 9999...')
    while True:
        if count == 0:
            data, client_addr = s.recvfrom(1024)
            print('connected from %s:%s' % client_addr)
            f = open(data, 'wb')
        data, client_addr = s.recvfrom(1024)
        if str(data) != "b'end'":
            f.write(data)
            print('recieved ' + str(count) + ' byte')
        else:
            break
        s.sendto('ok'.encode('utf-8'), client_addr)
        count += 1
    print('recercled' + str(count))
    f.close()
    s.close()


def send_file(ip, filepath, port=9001):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    filename = str(filepath)
    filepath, shotname, extension = Get_FilePath_FileName_FileExt(filename)
    client_addr = (ip, port)
    f = open(filename, 'rb')
    count = 0
    flag = 1
    while True:
        if count == 0:
            data = bytes(shotname + extension, encoding="utf8")
            start = time.time()
            s.sendto(data, client_addr)
        data = f.read(1024)
        if str(data) != "b''":
            s.sendto(data, client_addr)
            print(str(count) + 'byte')

        else:
            s.sendto('end'.encode('utf-8'), client_addr)
            break
        data, server_addr = s.recvfrom(1024)
        count += 1
    print('recircled' + str(count))
    s.close
    end = time.time()
    print('cost' + str(round(end - start, 2)) + 's')


def Get_FilePath_FileName_FileExt(filename):
    filepath, tempfilename = os.path.split(filename)
    shotname, extension = os.path.splitext(tempfilename)
    return filepath, shotname, extension

def new_file(path):
    lists = os.listdir(path)
    lists.sort(key=lambda fn:os.path.getmtime(path + "\\" + fn))
    file_new = os.path.join(path,lists[-1])
    return str(file_new)

def receive_file():
    count = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (get_host_ip(), 9001)
    s.bind(server_addr)
    print('Bind UDP on 9999...')
    while True:
        if count == 0:
            data, client_addr = s.recvfrom(1024)
            print('connected from %s:%s' % client_addr)
            f = open(data, 'wb')
        data, client_addr = s.recvfrom(1024)
        if str(data) != "b'end'":
            f.write(data)
            print('recieved ' + str(count) + ' byte')
        else:
            break
        s.sendto('ok'.encode('utf-8'), client_addr)
        count += 1
    print('recercled' + str(count))
    path = os.getcwd()
    ####弹窗####
    f.close()
    s.close()
    print(new_file(path))
    answer = tkinter.messagebox.askokcancel('提示', '请选择是否显示图片')
    if answer:
        im = Image.open(new_file(path))
        im.show()
    else:
        print("文件在："+new_file(path) + ".wav")
    print(new_file(path))
    newWin = Tk()
    newWin.withdraw()
    retVal = simpledialog.askstring('提示', "请输入所隐写字符长度", parent=newWin)
    # Destroy the temporary "parent"
    if retVal:
        print(lsb_tq.lsb_tq(2,new_file(path),"flag.txt"))
        tkinter.messagebox.askokcancel('提示', '所隐写字段为：'+lsb_tq.lsb_tq(int(retVal),new_file(path),"flag.txt"))
    else:
        print("文件在："+new_file(path) + ".wav")
    newWin.destroy()



def change_file_now(filenow):
    global file_now
    file_now = filenow


msg = {}


def get_pubkey_byip(ip):
    return get_from_file_pubkey(ip)


def save_pubkey(ip, pubkey):
    with open('ip_pubkey.txt', "r") as f:
        msg = f.read()
        f.close()
    msg = json.loads(msg)
    msg[ip] = pubkey
    msg = json.dumps(msg)
    print(msg)
    with open('ip_pubkey.txt', "w") as f:
        f.write(msg)
        f.close()


def init_pubkey():
    msg = {
        "192.168.1.1": 'fbe22ce7ea541afea3b42348dc4efcd138dc28bd69558296c5554aeff08c96e4b936a12bdac3090744677d39f5d7219f4230749de94c9efd2fd8376b826dde93'}
    msg = json.dumps(msg)
    with open('ip_pubkey.txt', "w") as f:
        f.write(msg)
        f.close()


def get_from_file_pubkey(ip):
    with open('ip_pubkey.txt', "r") as f:
        msg = f.read()
        f.close()
    msg = json.loads(msg)
    return msg[ip]


def get_sm4key_byip(ip):
    return getfromfile_sm4key(ip)
    # return getfromfile_sm4key(ip)


now_ip = ""


def get_now_ip():
    return str(now_ip)


def change_now_ip(ip):
    global now_ip
    now_ip = ip


def get_ip_from_username(name):
    with open('name_ip.txt', "r") as f:
        msg = f.read()
        f.close()
    print(json.loads(msg)[name])


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def send_message(ip, msg, port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 数据报协议-》udp
    client.sendto(msg.encode(), (ip, port))
    client.close()


def getfromfile_sm4key(ip):
    with open('ip_sm4.txt', "r") as f:
        msg = f.read()
        f.close()
    msg = json.loads(msg)
    return msg[ip]


def save_sm4pass(ip, sm4key):
    with open('ip_sm4.txt', "r") as f:
        msg = f.read()
        f.close()
    if msg=='':
        msg={"123.123.123.123":"asdqdegadetgfad"}
    else:
        msg = json.loads(msg)
    msg[ip] = sm4key
    msg = json.dumps(msg)
    with open('ip_sm4.txt', "w") as f:
        f.write(msg)
        f.close()



def init_sm4key():
    msg = {'127.0.0.1': 'hellasdfasdfo'}
    msg = json.dumps(msg)
    with open('ip_sm4.txt', "w") as f:
        f.write(msg)
        f.close()

def save_message(data,ip):
    with open('ip_message.txt', "r") as f:
        msg = f.read()
        f.close()
    if msg=='':
        msg={ip:{str(datetime.datetime.now()):"已经建立SM4加密通信"}}
    else:
        msg = json.loads(msg)
    now_time = datetime.datetime.now()
    msg[ip][str(now_time)]=data
    print(msg[ip])
    msg=json.dumps(msg)
    with open('ip_message.txt', "w") as f:
        f.write(msg)
        f.close()
# --------------------------------------接受消息--------------------------------------------------#
def judge_message(data, ip):
    msg = json.loads(data)
    if msg['type'] == 100:  # 密钥协商
        key_consult_receive(data, ip)
    if msg['type'] == 101:  # 消息通信
        message_receive(data, ip)
    if msg['type'] == 102:  # 图片传输
        picture_receive(data, ip)
    if msg['type'] == 112:  # 图片接受确认
        picture_channel(data, ip)
    if msg['type'] == 103:  # 音频传输
        voice_receive(data, ip)
    if msg['type'] == 113:  # 音频接受确认
        voice_channel(data, ip)


def key_consult_receive(data, ip):
    print("B收到密钥协商了 ！")
    data = json.loads(data)
    # data={'type':100,'msg':''}
    key_mi = base64.b64decode(data["msg"])
    sm4_key = crp.sm2_decry(crp.get_sm2_prikey('sm2_prikey.pem'), key_mi)
    print(sm4_key.decode())
    print(type(sm4_key.decode()))
    save_sm4pass(str(ip[0]), sm4_key.decode())
    print(sm4_key.decode())


def message_receive(data, ip):
    print("B收到消息了！！")
    save_message("other:"+crp.sm4_decry(get_sm4key_byip(ip[0]).encode(), base64.b64decode(json.loads(data)['msg'])).decode(),
                 ip[0])
    print(get_sm4key_byip(ip[0]))
    print(crp.sm4_decry(get_sm4key_byip(ip[0]).encode(), base64.b64decode(json.loads(data)['msg'])).decode())
    return crp.sm4_decry(get_sm4key_byip(ip[0]).encode(), base64.b64decode(json.loads(data)['msg'])).decode()


voice_id = 1


def voice_receive(data, ip, g_num=0):
    global voice_id
    mutex = threading.Lock()
    print("B接收到音频头了！！！")
    music_rev_accpect(ip)
    mutex.acquire()  # 上锁 注意了此时锁的代码越少越好
    g_num += 1
    time.sleep(2)
    miwen = crp.file_sm4_de('tem.key', get_sm4key_byip(get_now_ip()).encode())
    with open(str(voice_id) + ".wav", "wb") as f:
        f.write(miwen)
        f.close()
    time.sleep(1)
    ###弹出窗口
    answer = tkinter.messagebox.askokcancel('请选择是否收听音频', '请选择是否收听音频')
    if answer:
        crp.playmusic(str(voice_id) + ".wav")
    else:
        print("文件在："+str(voice_id) + ".wav")
    voice_id += 1
    mutex.release()  # 解锁


def voice_channel(data, ip):
    data = json.loads(data)
    if data['msg'] == 'ok':
        print("A建立了语音发送通道")
        #######这里要建立发送通道########
        music = threading.Thread(target=send_music, args=[ip[0], file_music_now])
        music.start()


def picture_receive(data, ip):
    print("B接收到图片头了！！！")
    # if (crp.sm2_verify(json.loads(data)['msg']['sign'], crp.hash(json.loads(data)['msg']['filename']).encode())):
    # 开启传输的函数file_transfer（）
    print("验证成功")
    picture_rev_accpect(ip)


def picture_channel(data, ip):
    global file_now
    data = json.loads(data)
    if data['msg'] == 'ok':
        print("A建立了图片发送通道")
        #######这里要建立发送通道########
        print(file_now)
        picture = threading.Thread(target=send_file, args=[ip[0], file_now])
        picture.start()


# --------------------------------------发送消息--------------------------------------------------#
def key_consult_transmit(ip):
    print("生成密钥协商data...")
    pubkey = get_pubkey_byip(ip)
    sm4_key = crp.create_sm4_key(16, 'sm4_key.pem').encode()
    msg = base64.b64encode(crp.sm2_encry(pubkey, sm4_key)).decode()
    save_sm4pass(ip, sm4_key.decode())
    data2 = {"type": 100, "msg": msg}
    send_message(get_now_ip(),json.dumps(data2))
    return json.dumps(data2)


def message_transfer(msg, ip):
    print("生成加密消息ing....")
    save_message('me:'+msg,str(ip))
    msg = crp.sm4_encry(get_sm4key_byip(ip).encode(), msg.encode())
    data = {"type": 101, "msg": base64.b64encode(msg).decode()}
    send_message(get_now_ip(), json.dumps(data))
    return json.dumps(data)


# print(message_receive(message_transfer('nihao', 123)))
# print(crp.sm4_decry(crp.get_sm4_key('sm4.pem'),base64.b64decode(json.loads(message_transfer('hello',123))['msg'])))


def picture_tranfer(filepath):
    print("生成图像传输data...")
    filename = os.path.basename(filepath)
    s = askstring('请输入', '请输入一串文字')
    lsb_tq.lsb_write(filepath, s, "hided_" + filename)
    change_file_now("hided_" + filename)
    sign = crp.hash(filepath)
    sign = crp.sm2_sign(sign.encode())
    msg = {'filename': filename, 'sign': sign}
    data = {"type": 102, "msg": msg}
    # 发送
    send_message(get_now_ip(), json.dumps(data))
    return json.dumps(data)


def picture_rev_accpect(ip):
    print("B构造同意接受图片data...")
    msg = "ok"
    #######这里要建立接受通道########
    data = {'type': 112, 'msg': msg}
    data = json.dumps(data)
    send_message(str(ip[0]), data)
    receive_file()
    #picture_get = threading.Thread(target=receive_file)
    #picture_get.start()
    # 开启接受线程
    return data


# print(picture_tranfer("2222.png"))


# print(crp.sm2_verify(json.loads(picture_tranfer("2222.png"))['msg']['sign'],crp.hash('2222.png').encode()))

def voice_tranfer():
    print("生成音频录制以及相应消息头...")
    crp.create_music('music.wav')
    j = crp.file_sm4_en('music.wav', get_sm4key_byip(get_now_ip()).encode())
    with open('tem.key', "wb") as f:
        f.write(j)
        f.close()
    filename = os.path.basename('tem.key')
    sign = crp.hash('tem.key')
    sign = crp.sm2_sign(sign.encode())
    msg = {'filename': filename, 'sign': sign}
    data = {"type": 103, "msg": msg}
    # 发送
    time.sleep(1)
    send_message(get_now_ip(), json.dumps(data))
    return json.dumps(data)


# print(voice_tranfer())

def music_rev_accpect(ip):
    print("B构造同意接受音频头ing...")
    msg = "ok"
    #######这里要建立接受通道########
    data = {'type': 113, 'msg': msg}
    data = json.dumps(data)
    send_message(ip[0], data)
    music_get = threading.Thread(target=receive_music)
    music_get.start()
    # 开启接受线程
    return data


# --------------------------------------接受端生成---------------------------------------------------------#
def crea_ser():
    print("----------------开始接收各方信息-------------------")
    s = socketserver.ThreadingUDPServer((get_host_ip(), 9999), MyHandler)
    s.serve_forever()

#change_now_ip(get_host_ip())
# --------------------------------------测试---------------------------------------------------------#
def test_sendmessage():
    init_sm4key()
    init_pubkey()
    change_now_ip("10.22.133.101")
    save_pubkey(get_now_ip(), crp.get_sm2_pubkey("sm2_pubkey.pem"))
    send_message(get_now_ip(), key_consult_transmit(get_now_ip()))
    print(message_transfer(("hello"), get_now_ip()))
    while True:
        change_now_ip("10.22.133.101")
        # change_now_ip(get_host_ip())
        print("是否发送语音")
        if (input() == 'ok'):
            print(voice_tranfer())
            input()
        else:
            print(message_transfer(("hello"), get_now_ip()))
            print(picture_tranfer('img.png'))
            send_message(get_now_ip(), input())  # li

#if __name__ == '__main__':
#    s = threading.Thread(target=crea_ser)
#    s.start()
#
#    s2 = threading.Thread(target=test_sendmessage)
#    s2.start()
