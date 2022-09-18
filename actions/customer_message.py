import logging

from .utils.utility import Utility
from .utils.events import schedule, unschedule


class CustomerMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        cim_message = Utility.get_key(slots, 'cimMessage')
        message = cim_message['body']['markdownText']

        self.log_info('Customer Message Received: ' + message, conversation_id)

        channel_session = cim_message['header']['channelSession']
        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})

        cc_user_list = Utility.get_agents(conversation)
        agents_present_in_conversation = cc_user_list is not None and len(cc_user_list) > 0
        
        events = self.schedule_timers_for_other_sessions(conversation, channel_session, channel_session_sla_map)
        events.append(unschedule.customer_sla(conversation_id, channel_session['id']))

        if not agents_present_in_conversation:
            routing_mode = Utility.get_routing_mode_from(channel_session)

            if routing_mode == 'PUSH' and Utility.get_key(slots, 'agent_state') == 'requested':
                dispatcher.text('An agent has been requested for this conversation, '
                                'he/she will join you shortly. Please wait!')
            elif routing_mode == 'PULL':
                dispatcher.text('Bot could not understand your message, all relevant agents have been notified, '
                                'agent(s) will join you shortly. Please wait!')
        
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

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CUSTOMER_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
