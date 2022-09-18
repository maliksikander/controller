import logging


class BotMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[BOT_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
