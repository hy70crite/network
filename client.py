import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 8000))

        # Ask for the username
        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.client_socket.send(self.username.encode())

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, message + "\n")
                self.chat_area.config(state='disabled')
                self.chat_area.yview(tk.END)
            except:
                print("An error occurred!")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.lower() == 'exit':
            self.client_socket.close()
            self.master.quit()
        else:
            self.client_socket.send(message.encode())
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()

