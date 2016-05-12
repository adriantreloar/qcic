'''
Created on 5 May 2016

@author: treloarja
'''

import pytest
from qcic import qcic
from qcic.qcic import Qcic_Monitor
import time

from Queue import Queue

class Test_Qcic_Monitor(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass


    def test_can_initialise_a_qcic_monitor(self):

        queue=Queue()

        monitor=Qcic_Monitor(queue=queue)
        
        #Default for production
        assert(monitor.sleep_ms==60000)
        assert(monitor.state=='INITIALISED')
        assert(monitor.started==False)


    def test_can_initialise_with_sleep_ms(self):
        '''We'll need to be able to set sleep ms directly, or we'll not be able to test sensibly'''

        queue=Queue()
        monitor=Qcic_Monitor(sleep_ms=50,queue=queue)

        assert(monitor.sleep_ms==50)


    def test_can_set_sleep_ms(self):
        '''We'll need to be able to set sleep ms directly, or we'll not be able to test sensibly'''
        queue=Queue()
        monitor=Qcic_Monitor(queue=queue)

        monitor.sleep_ms=5
        assert(monitor.sleep_ms==5)


class Test_Qcic_Monitor_Loop(object):

    def setup_method(self,function=None):
        queue=Queue()
        self.monitor=Qcic_Monitor(sleep_ms=2,queue=queue)

    def teardown_method(self,function=None):
        '''Stop the monitor, otherwise it will loop forever'''
        self.monitor.stop()
              
    def test_can_start(self):

        self.monitor.start()
        assert(self.monitor.state=='STARTED')
        assert(self.monitor.started==True)
        
    def test_can_stop(self):

        self.monitor.start()
        self.monitor.stop()
        assert(self.monitor.state=='STOPPED')
        assert(self.monitor.started==False)

