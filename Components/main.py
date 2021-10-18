from tkinter import PhotoImage,StringVar,ttk
import pickle
import socket
import struct
import cv2
from utile import centre_fenetre
from ttkbootstrap import Style
from Crypto.Hash import HMAC
from Crypto import Hash

def chat_client():
    """ Client Side stream call"""
    #-----------creation socket ----------
    # create socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = SERVEURIP.get() # paste your server ip address here
    port = 9999
    client_socket.connect((host_ip,port)) # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024) # 4K
            if not packet:
                break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    client_socket.close()

def chat():
    """ Server Side Stream """
    # Socket Create
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:',host_ip)
    port = 9999
    socket_address = (host_ip,port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:",socket_address)

    # Socket Accept
    while True:
        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                img,frame = vid.read()
                frame = imutils.resize(frame,width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
                cv2.imshow('TRANSMITTING VIDEO',frame)
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()


def main_soft(main):
    """" fonction qui lance l'interface graphique"""
    global SERVEURIP
    main.destroy()
    style=Style(theme='solar')
    maitre=style.master
    centre_fenetre(maitre,800,500)
    maitre.resizable(False,False)
    maitre.bg=PhotoImage(file="Components/images/0001.png")
    #--------- backgroun image ---------#
    # Create a label
    ttk.Label(maitre,image=maitre.bg).place(x=0,y=0,relwidth=1,relheight=1)
    #-----------  Main application -------------#

        #-------  Input words ---------#
    hostname  = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    txt_serveurip=ttk.Label(maitre, text="Votre Adresse hôte est :")
    txt_serveurip.place(relx=0.197,rely=0.38)
    clientip=ttk.Label(maitre, text=hostip)
    clientip.place(relx=0.235,rely=0.44)
    txt_cip=ttk.Label(maitre, text="Entrer l'adresse de l'hôte ici :")
    txt_cip.place(relx=0.64,rely=0.38)
    SERVEURIP=ttk.Entry(maitre,font=("Helvetica",12),width=20,textvariable=StringVar())
    SERVEURIP.place(relx=0.63,rely=0.44)
    style.configure('TLabel',background="#068056")
        #-------  Button room ---------#
    call = ttk.Button(maitre, text="Créer hôte",command=lambda:chat(),width=18)
    call.place(relx=0.19,rely=0.54)
    receive = ttk.Button(maitre, text="Rejoindre un hôte",command=lambda:chat_client(),width=18)
    receive.place(relx=0.65,rely=0.54)
