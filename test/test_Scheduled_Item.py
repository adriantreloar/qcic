'''
Created on 5 May 2016

@author: treloarja
'''

import pytest
from qcic import qcic
from qcic.qcic import Scheduled_Item
import time

class Test_Load_Scheduled_Item(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_can_initialise_a_scheduled_item(self):

        mybestmate='my best mate'
        wedding='wedding'
        started='STARTED'
                
        weekday='WEEKDAY'
        monday =2
        tenthirty =time.strptime("10:30","%H:%M")

        e=Scheduled_Item(sender=mybestmate,event=wedding,message_type='STARTED', periodicity=weekday, periods=[monday],times=[tenthirty])

        assert(e.sender==mybestmate)
        assert(e.event==wedding)
        assert(e.message_type==started)
        
        assert(e.periodicity==weekday)
        assert(e.periods==[monday])
        assert(e.times==[tenthirty])

        #recurring should be the default
        assert(e.recurring==True)

#    def test_can_load_sender_name_and_code_from_json(self):
#
#        assert(False)

#    def test_can_load_simple_repetition_period_from_json(self):

#        assert(False)

#    def test_can_load_two_simple_repetition_period_from_json(self):

#        assert(False)


    @classmethod
    def teardown_class(cls):
        pass
