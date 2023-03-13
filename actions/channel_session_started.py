import logging

from .utils.utility import Utility
from .utils.events import schedule, slot


class ChannelSessionStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Channel-session-started intent received", conversation_id)

        channel_session = Utility.get_key(slots, 'channelSession')
        channel_session_list = Utility.get_channel_sessions(conversation)

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        channel_session_sla_map[channel_session['id']] = False

        events = self.schedule_timer_for_all_sessions(conversation_id, channel_session_list, channel_session_sla_map)
        events.append(slot.set('channel_session_sla_map', channel_session_sla_map))

        latest_intent = Utility.get_key(channel_session, 'latestIntent')
        self.log_info('Latest intent in channel Session: ' + str(latest_intent), conversation_id)

        if not latest_intent:
            self.log_info("Latest intent is Empty, Dispatching welcome message", conversation_id)
            dispatcher.text('Hey! this is sparrow from ExpertFlow. How may i help you today?')

        return events

    @staticmethod
    def schedule_timer_for_all_sessions(conversation_id, channel_sessions, channel_session_sla_map):
        events = []

        for c_session in channel_sessions:
            if not Utility.get_key(channel_session_sla_map, c_session['id'], False):
                channel_session_sla_map[c_session['id']] = True

                inactivity_timeout = Utility.get_inactivity_timeout(c_session)
                schedule_timer = schedule.customer_sla(conversation_id, c_session['id'], inactivity_timeout)

                events.append(schedule_timer)

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CHANNEL_SESSION_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
