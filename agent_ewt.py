import logging


class AgentEwt:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("Going to send a message [agent will join soon]", conversation['id'])
        dispatcher.text("You're in queue, please wait an agent will come to you soon")
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_EWT] | conversation = [' + conversation_id + '] - ' + msg)
