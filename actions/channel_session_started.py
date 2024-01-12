import logging

from .utils.utility import Utility


class ChannelSessionStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        self.log_info("intent received", conversation['id'])

        room_mode = str((Utility.get_key(slots, 'cimEvent'))['roomInfo']['mode'])

        if room_mode == "PRIVATE":
            self.log_info("Room-mode: Private, Ignoring this intent", conversation['id'])
            return []

        channel_session = (Utility.get_key(slots, 'cimEvent'))['data']

        # ChannelSession.latestIntent field is set in case of 'Agent-Outbound' and 'Voice',
        # We do not want to dispatch the welcome message for these cases.
        if not Utility.get_key(channel_session, 'latestIntent'):
            self.log_info("Latest intent is Empty, Dispatching welcome message", conversation['id'])
            dispatcher.text('Hey! this is sparrow from ExpertFlow. How may i help you today?')

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CHANNEL_SESSION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
