import logging
from .utils.utility import Utility


class CustomerSlaStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        # room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        
        # percentage_completed = Utility.get_key(slots, 'cimEvent', {}).get('data').get('percentageCompleted')
        # dispatcher.text('Customer Sla Started - ' + str(percentage_completed) + '%')
        
        return []
    
