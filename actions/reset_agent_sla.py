import logging
from .utils.utility import Utility


class ResetAgentSla:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

      # if customer is in the conversation
        if Utility.is_customer_present(conversation):
            self.log_info("Customer exist, dispatching START_AGENT_SLA", conversation['id'])
            dispatcher.action('START_AGENT_SLA', Utility.get_sla_thresholds())

        self.log_info("No customer exist in conversation. Agent SLA wont start.", conversation['id'])
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[RESET_AGENT_SLA] | conversation = [' + conversation_id + '] - ' + msg)