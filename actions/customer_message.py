import logging

from .utils.utility import Utility
from .utils.events import schedule, unschedule, slot


class CustomerMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        cim_message = Utility.get_key(slots, 'cimMessage')
        message = cim_message['body']['markdownText']

        self.log_info('Customer Message Received: ' + message, conversation_id)

        channel_session_id = str(cim_message['header']['channelSessionId'])
        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        
        events = self.schedule_timers_for_other_sessions(conversation, channel_session, channel_session_sla_map)
        events.append(unschedule.customer_sla(conversation_id, channel_session['id']))
        channel_session_sla_map[channel_session['id']] = False
        events.append(slot.set('channel_session_sla_map', channel_session_sla_map))
        
        return events

    @staticmethod
    def schedule_timers_for_other_sessions(conversation, current_session, channel_session_sla_map):
        events = []
        channel_sessions = Utility.get_channel_sessions(conversation)

        for c_session in channel_sessions:
            # Skip the current channel session
            if c_session['id'] == current_session['id']:
                continue

            if not Utility.get_key(channel_session_sla_map, c_session['id'], False):
                inactivity_timeout = Utility.get_inactivity_timeout(c_session)
                events.append(schedule.customer_sla(conversation['id'], c_session['id'], inactivity_timeout))
                channel_session_sla_map[c_session['id']] = True

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CUSTOMER_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
