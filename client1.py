from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def recebe():
    """Lida com o recebimento de mensagens"""
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_split = msg.split("@")
            print(msg_split)
            if len(msg_split) > 1:
                destino = msg_split[1]
                print(destino)
                if destino == remetente.get():
                    print(msg_split)
                    msg_list.insert(tkinter.END, "Remetente: " + msg_split[0])
                    msg_list.insert(tkinter.END, "Assunto: " + msg_split[2])
                    msg_list.insert(tkinter.END, "Mensagem: " + msg_split[3])
                    msg_list.insert(tkinter.END, " ")

            if len(msg_split) == 1:
                msg_list.insert(tkinter.END, msg)
                print(msg)

        except OSError:  # Possivelmente o cliente saiu do chat.
            break


def set_name():  # event is passed by binders.
    """Lida com o recebimento do nome do remetente."""
    msg = remetente.get()
    print(msg)
    client_socket.send(bytes(msg, "utf8"))


def send():
    """Lida com o envio de mensagens."""
    if destinatario.get() != "" and mensagem.get() != "":
        msg = "@" + destinatario.get() + "@" + assunto.get() + "@" + mensagem.get()
        destinatario.set("")  # limpa o campo do destinatário
        assunto.set("")
        mensagem.set("")  # limpa o campo de mensagem
        client_socket.send(bytes(msg, "utf8"))

def exit():
    """Encerrar a conexão"""
    msg = "quit"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    window.quit()


def fecha():
    """Essa funcão é chamada quando a janela é fechada"""
    mensagem.set("quit")
    send()


window = tkinter.Tk()
window.title("ChatBox1")
window.configure(bg="#ffffff")
window.geometry("+450+10")  # tamanho e psocionamento

campo_conversa = tkinter.Frame(window)
remetente = tkinter.StringVar()  # declarando o tipo do campo remetente
destinatario = tkinter.StringVar()   # declarando o tipo do campo destinatário
assunto = tkinter.StringVar()   # declarando o tipo do campo assunto
mensagem = tkinter.StringVar()  # declarando o tipo do campo mensagem

scrollbar = tkinter.Scrollbar(campo_conversa)
scrollbar2 = tkinter.Scrollbar(campo_conversa)

l_remetente = tkinter.Label(window, text="   Remetente:", font="Ubuntu 14", width=11, height=2, bg="#ffffff")
l_destinatario = tkinter.Label(window, text=" Destinatário:", font="Ubuntu 14", width=11, height=2, bg="#ffffff")
l_assunto = tkinter.Label(window, text="       Assunto:", font="Ubuntu 14", width=11, height=2, bg="#ffffff")
l_mensagem = tkinter.Label(window, text="   Mensagem:", font="Ubuntu 14", width=11, height=2, bg="#ffffff")

l_conversa = tkinter.Label(window, text=" Conversa: ", font="Ubuntu 14", height=2, bg="#ffffff")

msg_list = tkinter.Listbox(window, height=11, width=38, font="Ubuntu 12 bold", fg="#483659", border=2,
                           yscrollcommand=scrollbar.set)

e_remetente = tkinter.Entry(window, font="Ubuntu 12 bold", fg="#483659", textvariable=remetente)
e_remetente.bind("<Return>", )
e_destinatario = tkinter.Entry(window, font="Ubuntu 12 bold", fg="#483659", textvariable=destinatario)
e_destinatario.bind("<Return>", )
e_assunto = tkinter.Entry(window, font="verdana 12 bold", fg="#483659", textvariable=assunto)
e_assunto.bind("<Return>", )
e_mensagem = tkinter.Entry(window, font="Ubuntu 12 bold", fg="#483659", width=65, textvariable=mensagem)
e_mensagem.bind("<Return>", )

window.protocol("WM_DELETE_WINDOW", fecha)

b_enviar_remetente = tkinter.Button(window, text="    Enviar    ", font="Ubuntu 14 bold", height=1, border=3,
                                    relief="groove", fg="#483659", command=set_name)
b_enviar = tkinter.Button(window, text="Enviar Mensagem", font="Ubuntu 14 bold", height=1, border=3,
                          relief="groove", fg="#483659", command=send)
b_sair = tkinter.Button(window, text="Exit", font="Ubuntu 14 bold", fg="red", border=3, relief='groove',
                        command=exit)

scrollbar.grid()
msg_list.grid(row=2, column=3)
campo_conversa.grid(column=3)

l_remetente.grid(row=1, column=1, sticky="n")
l_destinatario.grid(row=2, column=1)
l_assunto.grid(row=3, column=1)
l_mensagem.grid(row=4, column=1)
l_conversa.grid(row=1, column=3)

e_remetente.grid(row=1, column=2)
e_destinatario.grid(row=2, column=2)
e_assunto.grid(row=3, column=2)
e_mensagem.grid(row=4, column=2, columnspan=6)

b_enviar.grid(row=5, column=2, sticky="n")
b_enviar_remetente.grid(row=2, column=2, sticky="n")
b_sair.grid(row=5, column=3)

HOST = "localhost"
PORT = 50000
if not PORT:
    PORT = 50000
else:
    PORT = int(PORT)

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=recebe)
receive_thread.start()
"""início da execucão da interface"""
window.mainloop()
