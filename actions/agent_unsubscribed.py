import logging

from .utils.utility import Utility


class AgentUnSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info('intent received', conversation['id'])

        # if all agents left and customer still in conversation
        if not Utility.get_agents(conversation) and Utility.is_customer_present(conversation):
            Utility.change_bot_participant_role('PRIMARY', dispatcher, conversation)

            routing_mode = Utility.get_routing_mode(conversation)
            reason_code = str((Utility.get_key(slots, 'cimEvent'))['data']['reason'])

            # If agent was unsubscribed by system, find another agent on this conversation
            if routing_mode == 'PUSH' and (reason_code == 'FORCED_LOGOUT' or reason_code == 'SLA_EXPIRED'):
                self.log_info('Dispatching FIND_AGENT', conversation['id'])
                dispatcher.action('FIND_AGENT')

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_UNSUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)
