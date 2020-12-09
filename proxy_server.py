import socket
import threading
import tkinter as tk
from tkinter import messagebox
    


def getFile(a):  
    #Lay file blacklist.conf
    f=open("blacklist.conf","rt")
    for x in f:
        a.append(x)


        

def handle_client(conn,a):

    #Lay request la 1 thong diep HTTP
    
    request2=conn.recv(10000)
    request=request2.decode('latin-1')
    print('request:')
    print(request)


    #Lay dong dau thong diep HTTP
    first_line=request.split('\n')[0]
    print('first_line:')
    print(first_line)


    #Lay URL
    url=first_line.split(' ')[1]
    print('url:')
    print(url)


    #find pos of "://"
    http_pos=url.find("://")
    if http_pos==-1:
        temp=url
    else:
        temp=url[(http_pos+3):]
    
    print('temp:')
    print(temp)
    #find end of web sever
    websever_pos=temp.find("/")
    if websever_pos==-1:
        websever_pos=len(temp)
    websever=""

    port=80

    #print(url)
    websever=temp[:websever_pos]
    port_pos=websever.find(":")
    if port_pos==-1:
        port=80
    else:
        port=int(websever[port_pos+1:])
        print(port)
        websever=websever[:port_pos]
    print('websever:')
    print(websever)
    blocked=False
    for str in a:
        if str[:len(str)-1] == websever:
            blocked=True

    if blocked==False:
        print('Unblocked')
        so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.settimeout(300)
        so.connect((websever,port))
        so.sendall(request2)
        while True:
            data=so.recv(10000)
            if(len(data)>0):
                conn.sendall(data)
            else:
                print('out!')
                break
        so.close()
    else:
        print('Blocked')
        

        
        conn.sendall(b'''HTTP/1.1 \n\n<html lang="en" dir="ltr">
                                        <head>
                                            <meta charset="utf-8">
                                            <link rel="stylesheet" href="style.css">
                                        </head>
                                        <body>
                                            <div class="wrapper">
                                            <div class="display">
                                                <div id="time">
                                        </div>
                                        </div>
                                        <span></span>
                                            <span></span>
                                            </div>
                                        <script>
                                            setInterval(()=>{
                                                const time = document.querySelector(".display #time");
                                            
                                                time.textContent = "403 Forbiden";
                                            });
                                            </script>

                                        </body>
                                        </html>''') 
        conn.sendall(b'''HTTP/1.1 \n\n*{
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
  }
  html,body{
    display: grid;
    height: 100%;
    place-items: center;
    background: #000;
  }
  .wrapper{
    height: 100px;
    width: 360px;
    position: relative;
    background: linear-gradient(135deg, #14ffe9, #ffeb3b, #ff00e0);
    border-radius: 10px;
    cursor: default;
    animation: animate 1.5s linear infinite;
  }
  .wrapper .display,
  .wrapper span{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .wrapper .display{
    z-index: 999;
    height: 85px;
    width: 345px;
    background: #1b1b1b;
    border-radius: 6px;
    text-align: center;
  }
  .display #time{
    line-height: 85px;
    color: #fff;
    font-size: 50px;
    font-weight: 600;
    letter-spacing: 1px;
    background: linear-gradient(135deg, #14ffe9, #ffeb3b, #ff00e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: animate 1.5s linear infinite;
  }
  @keyframes animate {
    100%{
      filter: hue-rotate(360deg);
    }
  }
  .wrapper span{
    height: 100%;
    width: 100%;
    border-radius: 10px;
    background: inherit;
  }
  .wrapper span:first-child{
    filter: blur(7px);
  }
  .wrapper span:last-child{
    filter: blur(20px);
  }
  ''')                                                
        
    conn.close()


HOST="10.0.156.119"
PORT=8888
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1000)

a=[]
getFile(a)  

while True:
    conn,addr=s.accept()
    t=threading.Thread(target=handle_client, args=(conn,a))
    t.setDaemon(True)
    t.start()
    
    