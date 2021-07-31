import time
import random
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import sm2_keycreate
from gmssl import sm2, func
import json
import pyaudio
import wave
from playsound import playsound
import hashlib                                   #导入hashlib模块

def hash(file_path,Bytes=1024):
    md5_1 = hashlib.md5()                        #创建一个md5算法对象
    with open(file_path,'rb') as f:              #打开一个文件，必须是'rb'模式打开
        while 1:
            data =f.read(Bytes)                  #由于是一个文件，每次只读取固定字节
            if data:                             #当读取内容不为空时对读取内容进行update
                md5_1.update(data)
            else:                                #当整个文件读完之后停止update
                break
    ret = md5_1.hexdigest()                      #获取这个文件的MD5值
    return ret

#######
# 加密 #
#######
def sm2_encry(pubk, data):
    # func:实现SM2非对称加密
    # @param:_pubk:SM2加密公钥
    # @param:_data：加密数据
    # return:加密后的密文
    sm2_crypt = sm2.CryptSM2(public_key=pubk, private_key='0')
    return sm2_crypt.encrypt(data)


def sm2_decry(prik, data):
    # func:实现SM2非对称解密
    # @param:_prik:SM2解密私钥
    # @param:_data：待解密数据
    # return:解密后的明文
    sm2_crypt = sm2.CryptSM2(public_key='0', private_key=prik)
    return sm2_crypt.decrypt(data)


def sm4_encry(key, data):
    # func:实现SM4对称解密
    # @param:pubk:16字节加密密钥
    # @param:data：待加密数据
    # return:加密后的密文
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    return crypt_sm4.crypt_ecb(data)


def sm4_decry(key, data):
    # func:实现SM4对称加密
    # @param:pubk:16字节解密密钥
    # @param:data：待解密数据
    # return:解密后的明文
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_DECRYPT)
    return crypt_sm4.crypt_ecb(data)


def create_sm2_key():
    # func:生成sm2的公私钥并持久化存储
    # return:返回sm2的公私钥
    # 说明：将公私钥存入sm2_prikey.pem 以及sm2_pubkey.pem中
    priKey = sm2_keycreate.PrivateKey()
    pubKey = priKey.publicKey()
    with open("sm2_prikey.pem", "wb") as f:
        f.write(str(priKey.toString()).encode())
        f.close()
    with open("sm2_pubkey.pem", "wb") as f:
        f.write(str(pubKey.toString(compressed=False)).encode())
        f.close()
    return pubKey.toString(), priKey.toString()


def create_sm4_key(length, sm4_keyfile):
    # func:生成16字节sm4的密钥
    # return:返回sm4密钥
    # 说明：将所生成密钥存入sm4.pem
    secret_key = "n&^-9#k*-6pwzsjt-qsc@s3$l46k(7e%f80e7gx^f#vouf3yvz"
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (
                random.getstate(),
                time.time(),
                secret_key)).encode('utf-8')
        ).digest())
    ret = ''.join(random.choice(allowed_chars) for i in range(length))
    with open(sm4_keyfile, "wb") as f:
        f.write(str(ret).encode())
        f.close()
    return ret


def get_sm4_key(file):
    # func:读取file文件下的sm4密钥
    # return:返回sm4密钥
    with open(file, "rb") as f:
        pub = f.read()
        f.close()
    return pub


def get_sm2_pubkey(pubfile1):
    # func:读取file文件下的sm2公钥
    # return:返回sm4公钥
    with open(pubfile1, "rb") as f:
        pub = f.read()
        f.close()
    return pub.decode()


def get_sm2_prikey(prifile2):
    # func:读取file文件下的sm2私钥
    # return:返回sm2私钥
    with open(prifile2, "rb") as f:
        pri = f.read()
        f.close()
    return pri.decode()


def sm2_sign(data):
    # func:实现sm2的签名
    # @param:data：待签名数据
    # @param:data：待解密数据
    # return:签名
    public_key = get_sm2_pubkey('sm2_pubkey.pem')
    private_key = get_sm2_pubkey('sm2_prikey.pem')
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    return sm2_crypt.sign(data, random_hex_str)  # 16进制


def sm2_verify(sign, data,pubkey):
    # func:验证sm2的签名
    # @param:data：待签名数据
    # @param:sign：签名
    # return:返回签名结果
    public_key = pubkey
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=0)
    return sm2_crypt.verify(sign, data)


#####
# 证书#
#####
def create_cer(username, pubkey, ip, port):
    # func:生成证书
    # @param:username:用户名
    # @param:pubkey：用户公钥
    # @param:ip：用户ip地址
    # @param:port：用户端口号
    # return:输出证书的js编码
    cer = {'user': username, 'pubkey': pubkey, 'ip': ip, 'port': port, }
    js = json.dumps(cer)
    sign = sm2_sign(js.encode())
    print(js.encode())
    cer.setdefault('sign', sign)
    return json.dumps(cer)


def verify_cer(cerjs):
    # func:验证证书
    # @param:cerjs:证书js格式
    # return:返回验证结果
    cer = json.loads(cerjs)
    sign = cer['sign']
    cer.pop('sign')
    return sm2_verify(sign, json.dumps(cer).encode())


##########
# 文件加密#
##########
def file_sm4_en(filename,key):
    # func:文件加密
    # @param:filename：文件路径
    # return:加密后数据
    with open(filename, "rb") as f:
        pub = f.read()
        f.close()
    return sm4_encry(key, pub)

def file_sm4_de(filename,key):
    # func:文件解密
    # @param:filename:解密文件路径
    # return:返回解密后数据
    with open(filename, "rb") as f:
        minwen = f.read()
        f.close()
    return sm4_decry(key, minwen)


#########
# 音频制作#
#########
def playmusic(filename):
    # func:播放音频
    # @param:filename:待播放音频
    playsound(filename)
    print("播放完成")


def create_music(filepath):
    # func:录制音频
    # @param:filename:待录制音频文件
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("*" * 10, "开始录音：请在5秒内输入语音")
    frames = []
    flag = 0
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if (flag == 1):
            print("结束了")
            break
        if (i == 10 * 62.5):
            flag = 1
    print("*" * 10, "录音结束\n")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#playmusic('hel.wav')
#create_music('hel.wav')
# data = b'1222'
# data2 = b'12213'

#d = {'name': 'tom', 'age': 20, 'interestlist': {'len':3,'vim1':'asdf','vim2':'123','vim3':'1234' }}
#j = json.dumps(d)
#
#print(j)
#d1 = json.loads(j)
#print(d1['interestlist']['vim2'])
#dict={}
#j = json.dumps(d)
#with open('a.js', "wb") as f:
#   f.write(j.encode())
#   f.close()

#create_sm2_key()
# print(j.encode())
# d1 = json.loads(j)
# print(d1)
# print(type(d1))
# print(d1['name'])
# d = "{'name':'tom','age':20,'interest':['music','movie']}"
# print(sm2_encry(get_sm2_pubkey('sm2_pubkey.pem'), d.encode()))
# print(sm2_verify(sm2_sign(data), data))
# print(verify_cer(create_cer('123', '1233', '123', '12312')))
# with open('22.png', "rb") as f:
#    pub = f.read()
#    f.close()
# with open('22key.key', "wb") as f:
#    f.write(sm4_encry(get_sm4_key('sm4.pem'),pub))
#    f.close()
# with open('22key.key', "rb") as f:
#    aaa = f.read()
#    f.close()
# aa=sm4_decry(get_sm4_key('sm4.pem'),aaa)
# with open('2222.png', "wb") as f:
#    f.write(aa)
#    f.close()
