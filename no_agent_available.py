import logging

from .utils.utility import Utility
from .utils.events import schedule, slot


class NoAgentAvailable:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("NO_AGENT_AVAILABLE intent received", conversation_id)

        channel_session_list = Utility.get_channel_sessions(conversation)
        
        if not channel_session_list:
            self.log_info("Channel session list is empty, returning...", conversation_id)
            return [{'type': 'reset'}]

        dispatcher.text('No agents are available at this time. Please contact again in the future.')
        agent_state = slot.set('agent_state', 'not_requested')

        channel_session = Utility.get_latest_channel_session(conversation)
        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})

        if Utility.get_key(channel_session_sla_map, channel_session['id'], False):
            self.log_info("Customer activity timer already running, not starting it again", conversation_id)
            return [agent_state]

        self.log_info("Starting customer activity timer", conversation_id)

        channel_session_sla_map[channel_session['id']] = True
        inactivity_timer = Utility.get_inactivity_timeout(channel_session)
        schedule_timer = schedule.customer_sla(conversation_id, channel_session['id'], inactivity_timer)

        return [schedule_timer, agent_state, slot.set('channel_session_sla_map', channel_session_sla_map)]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[NO_AGENT_AVAILABLE] | conversation = [' + conversation_id + '] - ' + msg)
