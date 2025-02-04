import logging

from .utils.utility import Utility


class ChannelSessionStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

        if str(room_info['mode']) == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
            return []

        channel_session = (Utility.get_key(slots, 'cimEvent'))['data']

        # ChannelSession.latestIntent field is set in case of 'Agent-Outbound' and 'Voice',
        # We do not want to dispatch the welcome message for these cases.
        if not Utility.get_key(channel_session, 'latestIntent'):
            self.log_info("Latest intent is Empty, Dispatching welcome message", str(room_info['id']), conversation)
            dispatcher.text('Hey! this is sparrow from ExpertFlow. How may i help you today?')

        return []

    @staticmethod
    def log_info(msg, room_id, conversation):
        conversation_id = str(None if not conversation else conversation['id'])
        logging.info(
            '[CHANNEL_SESSION_STARTED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
