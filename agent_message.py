import imp
import logging

from utils.jax import jax
from utils.events import schedule, slot

class AgentMessage:

    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - Agent message is received')

        channel_session = jax.get_channel_session_from_conversation(conversation)
        channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})
        
        if channel_session is None:
            logging.info('['+conversation['id']+'] - Channel-Session not found, returning without starting customer activity timer')
            return []
        elif jax.get_key(channel_session_sla_map, channel_session['id'], False):
            logging.info('['+conversation['id']+'] - Customer activity timer is already running, not starting again')
            return []

        timeout = jax.get_timeout_from_channel_session(channel_session)
        channel_session_sla_map[channel_session['id']] = True
        
        logging.info('['+conversation['id']+'] - Scheduling customer activity timer for ' + str(timeout) + ' seconds')
        
        return [
            schedule.customer_sla(conversation['id'], channel_session['id'], timeout),
            slot.set('channel_session_sla_map', channel_session_sla_map)
        ]
        