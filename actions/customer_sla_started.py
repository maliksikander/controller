import logging
from .utils.utility import Utility


class CustomerSlaStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        # room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        # self.log_info("intent received", str(room_info['id']), conversation)
        
        # percentage_completed = Utility.get_key(slots, 'cimEvent', {}).get('data').get('percentageCompleted')
        # dispatcher.text('Customer Sla Started - ' + str(percentage_completed) + '%')
        
        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[CUSTOMER_SLA_STARTED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
