'''
Created on 5 May 2016

@author: treloarja
'''

import pytest
from qcic import qcic
from qcic.qcic import Qcic_Monitor, Qcic_ZeroMQ_Receiver
import time

from queue import Queue




class Test_Qcic_Monitor(object):

    def setup_method(self,function=None):

        #PAss the same queue to both instances, so one can put stuff on the queue, and the other can pull stuff off it
        queue=Queue()

        self.monitor=Qcic_Monitor(sleep_ms=1,queue=queue)
        self.monitor.start()
        
        self._sender1_url="tcp://127.0.0.1:5659"
        self.channels=[self._sender1_url]
        self.receiver=Qcic_ZeroMQ_Receiver(channels=self.channels,queue=queue)
            

    def teardown_method(self,function=None):
        '''Stop the receiver, otherwise it will loop forever'''
        self.receiver.stop()
        self.monitor.stop()
              
    def test__received_queue_is_the_monitor_queue(self):
        assert(self.receiver.queue==self.monitor.queue)

    def test_PROGRESS_message_received_ends_up_on_monitor_queue(self):
        
        message=[b'PROGRESS']
        #Send message directly
        self.receiver.handle_message(message)
        assert(self.receiver._latest_message_sent_to_queue==message)
        time.sleep(0.001)
        assert(self.monitor._latest_message_grabbed_from_queue==message)

    def test_SUCCEEDED_message_received_ends_up_on_monitor_queue(self):
        
        message=[b'SUCCEEDED']
        #Send message directly
        self.receiver.handle_message(message)
        assert(self.receiver._latest_message_sent_to_queue==message)
        time.sleep(0.001)
        assert(self.monitor._latest_message_grabbed_from_queue==message)

