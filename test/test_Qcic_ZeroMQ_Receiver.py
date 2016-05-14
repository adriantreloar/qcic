'''
Created on 5 May 2016

@author: treloarja
'''

import pytest
from qcic import qcic
from qcic.qcic import Qcic_ZeroMQ_Receiver
import time
import zmq
from queue import Queue

class Test_Qcic_ZeroMQ_Receiver(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass


    def test_can_initialise_a_qcic_Qcic_ZeroMQ_Receiver(self):

        queue=Queue()

        receiver=Qcic_ZeroMQ_Receiver(channels=[],queue=queue)

        #Default for production
        assert(receiver.state=='INITIALISED')
        assert(receiver.started==False)




class Test_Qcic_ZeroMQ_Receiver_Loop(object):

    def setup_method(self,function=None):

        self._sender1_url="tcp://127.0.0.1:5659"

        '''Setup some senders'''
        self._sender_context = zmq.Context()
        
        self._sender1 =self._sender_context.socket(zmq.PUB)
        self._sender1.setsockopt(zmq.LINGER, 20)
        self._sender1.bind(self._sender1_url)

        self.channels=[self._sender1_url]

        queue=Queue()
        self.receiver=Qcic_ZeroMQ_Receiver(channels=self.channels,queue=queue)

        self._sender1.send_multipart([b'STARTED'])
            

    def teardown_method(self,function=None):
        '''Stop the receiver, otherwise it will loop forever'''
        #print('Stopping')
        self.receiver.stop()
        #print('Stopped')
              
        '''Clear up the senders'''      
        self._sender1.setsockopt(zmq.LINGER,1)
        self._sender1.close()
        self._sender_context.term() 
                  
    def test_can_start(self):

        self.receiver.start()
        time.sleep(0.01)
        
        assert(self.receiver.state=='STARTED')
        assert(self.receiver.started==True)
        
    def test_can_stop(self):

        self.receiver.start()
        time.sleep(0.01)
        self.receiver.stop()
        time.sleep(0.01)
        
        assert(self.receiver.state=='STOPPED')
        assert(self.receiver.started==False)

    def test_can_stop_immediately(self):

        self.receiver.start()
        #No sleep here
        self.receiver.stop()
        time.sleep(0.02)
        
        assert(self.receiver.state=='STOPPED')
        assert(self.receiver.looping==False)

    def test_channels_initialise_correctly(self):
        
        self.receiver.start()

        assert(self.receiver._channels==self.channels)


        
    def test_cleans_up_after_error(self):

        self.receiver.start()

        #Stub out handle_message to raise an error
        def handle_message_stub(receiver,message):
            
            print('In MonkeyPatched Stub')
            
            msgtype=message[0]
        
            if msgtype==b'STOPLOOP':
                self.state='STOPPING'
                self.started=False
                self.looping=False
                
            print('RaisingError')
            raise ValueError

        #print(self.receiver.handle_message)
        
        #Monkey patch handle_message into the test code
        self.receiver.handle_message=handle_message_stub

        print('sending PROGRESS message from test suite')

        #wait for startup to be complete
        time.sleep(0.01)
                
        #raise an erro by sending a message to the monkey patched stub
        self._sender1.send_multipart([b'PROGRESS'])

        print('sent PROGRESS message from test suite')


        time.sleep(0.01)

        assert(self.receiver.state=='FAILED')
        assert(self.receiver.started==False)
        assert(self.receiver.looping==False)
            
