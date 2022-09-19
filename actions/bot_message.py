import logging

from actions.utils.events import schedule, slot
from actions.utils.utility import Utility


class BotMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("intent received", conversation_id)

        cim_message = Utility.get_key(slots, 'cimMessage')
        channel_session = cim_message['header']['channelSession']

        if channel_session is None:
            self.log_info("Channel Session not found, returning...", conversation_id)
            return []

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        return self.schedule_inactivity_timer(conversation_id, channel_session, channel_session_sla_map)

    @staticmethod
    def schedule_inactivity_timer(conversation_id, channel_session, channel_session_sla_map):
        channel_session_id = channel_session['id']

        if not Utility.get_key(channel_session_sla_map, channel_session_id, False):
            channel_session_sla_map[channel_session_id] = True
            inactivity_timeout = Utility.get_inactivity_timeout(channel_session)

            schedule_timer = schedule.customer_sla(conversation_id, channel_session_id, inactivity_timeout)
            return [schedule_timer, slot.set('channel_session_sla_map', channel_session_sla_map)]

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[BOT_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
