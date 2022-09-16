import logging

from utils.jax import jax
from utils.events import schedule, slot

class NoAgentAvailable:
    
    def run(self, conversation, slots, dispatcher, metadata):

        logging.info('['+conversation['id']+'] - NO_AGENT_AVAILABLE intent received')

        channel_session_list = jax.get_key(slots, 'channelSessionList', [])
        
        if not channel_session_list:
            logging.info('['+conversation['id']+'] - Channel session list is empty, returning...')
            return [
                slot.set('agent_state', 'not_requested')
            ]

        dispatcher.text('No agents are available at this time. Please contact again in the future.')

        channel_session = channel_session_list[len(channel_session_list) - 1]
        channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})

        if jax.get_key(channel_session_sla_map, channel_session['id'], False):
            logging.info('['+conversation['id']+'] - Customer activity timer already running, not starting it again')
            return [
                slot.set('agent_state', 'not_requested')
            ]

        logging.info('['+conversation['id']+'] - Starting customer activity timer')
        channel_session_sla_map[channel_session['id']] = True
        
        return [
            schedule.customer_sla(conversation['id'], channel_session['id'], jax.get_timeout_from_channel_session(channel_session)),
            slot.set('agent_state', 'not_requested'),
            slot.set('channel_session_sla_map', channel_session_sla_map)
        ]