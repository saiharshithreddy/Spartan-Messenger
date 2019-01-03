import threading
from tkinter import *
from tkinter import simpledialog
import grpc
import messenger_pb2
import messenger_pb2_grpc
import asyncio
import sys
import yaml
import time

import base64
import os
address = 'localhost'
port = 3001


class Client:

    def __init__(self, u: str):
        with open("config.yaml", "r") as configFile:
            config = yaml.load(configFile)
        configFile.close()
        userlist =config["users"]
        if u in userlist:    
            print("[Spartan] Connected to the Spartan Server")
    
            friendslist = [x for x in userlist if x != u]
            print ("[Spartan] User List:",end=" ")
            print(', '.join(friendslist))
            print("[Spartan] Enter a user whom you want to chat with :", end=" ") 
            self.user = input()
            if self.user in friendslist:
                print("[Spartan] You are now ready to chat with "+self.user)
            else:
                exit()
        else: 
            exit()
        
    
        self.username = u
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = messenger_pb2_grpc.MessengerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__read_messages, daemon=True).start()
        
        self.type_message()

    def __read_messages(self):
            #note.friend == username
            #print('l')
            for note in self.conn.MsgStream(messenger_pb2.Msg()):
                if(self.username == note.friendname and note.name == self.user):
                
                    print("[{}] {}".format(note.name, note.message))
                    #print("[{}]".format(self.username), end=" ")

    def type_message(self):
        try:
            while True:
                #print("[{}]".format(self.username), end=" ")
                self.text = input()
                
                self.send_message('<Return>')
                time.sleep(0.5)
        except:
            KeyboardInterrupt
            
    def send_message(self, event):
        """
        This method is called when user enters something into the textbox
        """
        #print('2')
        n = messenger_pb2.Msg()
        n.name = self.username
        n.message = self.text
        n.friendname= self.user
        
        print("[{}] {}".format(self.username, self.text))
        self.conn.SendMsg(n)

        

if __name__ == '__main__':
    while True:
        c = Client(sys.argv[1]) # client object c is created
    
    