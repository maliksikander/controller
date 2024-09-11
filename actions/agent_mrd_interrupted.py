import logging
from .utils.utility import Utility


class AgentMrdInterrupted:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']
        self.log_info("intent received", str(room_info['id']), conversation)

        # To check for private room

        mrd_interrupted = (Utility.get_key(slots, 'cimEvent'))['data']

        if str(mrd_interrupted['mrdId']) == '62f9e360ea5311eda05b0242' or str(mrd_interrupted['mrdId'])
        == '20316843be924c8ab4f57a7a' :
            self.log_info("MRD is of voice type, REMOVE_ALL_AGENTS will not be invoked.", str(room_info['id']),
            conversation)
            return []

        dispatcher.action('REMOVE_ALL_AGENTS', {"mrdInterrupted": mrd_interrupted, "reason": "MRD_INTERRUPTED"})

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[AGENT_MRD_INTERRUPTED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
