from concurrent import futures
import time

import grpc

import messenger_pb2
import messenger_pb2_grpc
import asyncio

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
class Messenger(messenger_pb2_grpc.MessengerServicer):
    
    def __init__(self):
            #self.friendname = 'alice' 
            #self.chats = {'alice':[], 'charlie': [], 'eve':[], 'foo':[], 'bar':[], 'baz':[], 'qux':[]}
            #self.chats={"group1": [], "group2":[]}
            # chats are created
            self.chats=[]
            #self.f = 
            
            
    def MsgStream(self, request_iterator , context):
        #LRU
        #while self.friendname != " ":
        if len(self.chats) > 15:
            a = len(self.chats) - 15
            self.chats= self.chats[a:]
        '''
        if len(self.chats[self.friendname]) > 15:
            a = len(self.chats[self.friendname]) - 15
            self.chats[self.friendname]= self.chats[self.friendname][a:]
        
        
        aliceindex =0, 
        charlieindex =0
        eveindex =0
        fooindex =0
        barindex =0
        bazindex =0 
        quxindex =0

        lastindex = { 'alice' : aliceindex , 'charlie': charlieindex, 'eve':eveindex, 'foo':fooindex, 'bar':barindex, 'baz':bazindex, 'qux':quxindex}
        '''# For every client a infinite loop starts (in gRPC's own managed thread)
        lastindex =0
        while True:
            # Check if there are any new messages
            #index = lastindex[self.friendname]
            #print("in msgstream")
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
                
        
    def SendMsg(self, request: messenger_pb2.Msg, context):
        #print(request.name + ": "+request.friendname)
        #self.friendname = request.friendname
        self.chats.append(request)
        return messenger_pb2.EmptyStream()
    

if __name__ == '__main__':
    port = 3001
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MessengerServicer_to_server(Messenger(), server)
    try:
        print("Spartan server started at port " +str(port)+"")
        server.add_insecure_port('[::]:' + str(port))
        server.start()
    except:
        KeyboardInterrupt
        
    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100) 

