from time import time, sleep
from threading import Thread

import zmq

class Scheduled_Item:
    """

    """    
    def __init__(self,periodicity, periods,times,sender,event,message_type='SUCCEEDED',recurring=True):
        
        self.sender=sender
        self.periodicity=periodicity
        self.periods=periods
        self.times=times
        self.event=event
        self.message_type=message_type
        
        self.recurring=recurring
        
        
class Qcic_Monitor:
    """

    """    
    def __init__(self,sleep_ms=60000):
        
        self.sleep_ms=sleep_ms

        self.state='INITIALISED'
        self.started=False

    def start(self):
        self.state='STARTED'
        self.started=True

        #Create a thread with a while loop that sleeps
        t=Thread(target = self._start_looping)
        t.start()
        
        
    def _start_looping(self):
        
        while(self.started):
            sleep(self.sleep_ms/1000.0)

    def stop(self):
        self.state='STOPPED'
        self.started=False

class Qcic_ZeroMQ_Receiver:
    """

    """    
    def __init__(self,channels):

        self._main_thread_sender_url='tcp://127.0.0.1:5013'
        self._main_thread_sender_context=None
        self._channels=channels
        
        self.started=False
        self.looping=False
       
        self.state='INITIALISED'
        

    def __del__(self):
        pass
        

    def start(self):

        '''Had problems freeing up this context - so context is created and dropped in the same function - let ZMQ handle the magic of SUB being created befor ePUB'''

        '''Create a PUB socket to send messages to the looping thread, e.g. STOP'''
        
        self._main_thread_sender_context = zmq.Context()
        
        self._main_thread_sender =self._main_thread_sender_context.socket(zmq.PUB)
        self._main_thread_sender.setsockopt(zmq.LINGER, 20)
        self._main_thread_sender.bind(self._main_thread_sender_url)        


                
        #Create a thread with a while loop that sleeps
        t=Thread(target = self._start_looping)
        t.start()
        

            
        
    def _start_looping(self):

        self.looping=True

        #print('Started Thread')
        
        '''Create a zmq context '''        
        self._context = zmq.Context()
        self._receiver =self._context.socket(zmq.SUB)
        

        
        for _channel in self._channels: 
            self._receiver.connect(_channel)
        
        self._receiver.connect(self._main_thread_sender_url)
        #print('Connected Thread')
        
        
        self._receiver.setsockopt(zmq.SUBSCRIBE, b"STARTED")
        self._receiver.setsockopt(zmq.SUBSCRIBE, b"PROGRESS")
        self._receiver.setsockopt(zmq.SUBSCRIBE, b"FAILED")
        self._receiver.setsockopt(zmq.SUBSCRIBE, b"SUCCEEDED")
                
        #Special message for testing erorr conditions
        self._receiver.setsockopt(zmq.SUBSCRIBE, b"STOPLOOP")
        
        self.started=True
        self.state='STARTED'
        
        #Let everything start properly
        sleep(0.01)
        
        try:
            while(self.looping):
                print('Awaiting message')
                signal=self._receiver.recv_multipart()
                print('Got message',signal[0])
                
                self.handle_message(signal)

            self.state='STOPPED'

        except Exception:
            self.state='FAILED'
            self.started=False
            self.looping=False
            print('Failed Thread')

        finally:
            self._receiver.setsockopt(zmq.LINGER,1)
            self._receiver.close()
            self._context.term()   
            self.started=False
            
        
            
        #print('Stopped Thread')
                    
    def stop(self):
        
        if self._main_thread_sender_context:

            #print('Sending message to loop')
            '''Send a message to the looping thread to stop'''
            self._main_thread_sender.send_multipart([b'STOPLOOP'])

            #print('Sent message to loop')

                
            '''Close our context properly'''
            self._main_thread_sender.setsockopt(zmq.LINGER,100)
            self._main_thread_sender.close()
            self._main_thread_sender_context.term()     
            self._main_thread_sender_context=None
            
        
        #Set self.started here too - so that if we haven't started properly when we stop, we don't loop forever
        self.looping=False  
        self.started=False
        
    def handle_message(self,message):
        msgtype=message[0]
    
        if msgtype==b'STOPLOOP':
            self.state='STOPPING'
            self.started=False
            self.looping=False
        