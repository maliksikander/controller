import logging


class Default:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("Default action called", conversation['id'])
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[DEFAULT] | conversation = [' + conversation_id + '] - ' + msg)
