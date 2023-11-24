import logging
from .utils.utility import Utility


class CustomerMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        if len(Utility.get_agents(conversation)) > 0:
            self.log_info("Agent exist in conversation, dispatch start", conversation['id'])
            dispatcher.action('START_AGENT_SLA', Utility.get_sla_thresholds())


            return[]

        self.log_info("No agent exist in conversation.", conversation['id'])
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CUSTOMER_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)