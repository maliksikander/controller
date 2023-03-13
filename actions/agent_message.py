import logging

from .utils.utility import Utility
from .utils.events import schedule, slot


class AgentMessage:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Agent message is received", conversation_id)

        cim_message = Utility.get_key(slots, 'cimMessage')

        channel_session_id = str(cim_message['header']['channelSessionId'])
        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        
        if channel_session is None:
            self.log_info("Channel-Session not found, returning...", conversation_id)
            return []
        elif Utility.get_key(channel_session_sla_map, channel_session['id'], False):
            self.log_info("Customer activity timer is already running, not starting again", conversation_id)
            return []

        timeout = Utility.get_inactivity_timeout(channel_session)
        channel_session_sla_map[channel_session['id']] = True
        
        self.log_info("Scheduling customer activity timer for " + str(timeout) + " seconds", conversation_id)
        
        return [
            schedule.customer_sla(conversation_id, channel_session['id'], timeout),
            slot.set('channel_session_sla_map', channel_session_sla_map)
        ]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_MESSAGE] | conversation = [' + conversation_id + '] - ' + msg)
        