import logging
from .utils.utility import Utility


class AgentMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])
        dispatcher.action('STOP_AGENT_SLA')

        return[]


    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)