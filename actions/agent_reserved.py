import logging


class AgentReserved:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("An agent has been reserved for this conversation", conversation['id'])
        dispatcher.text('An agent has been reserved for you, please wait agent will join you soon')
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_RESERVED] | conversation = [' + conversation_id + '] - ' + msg)
