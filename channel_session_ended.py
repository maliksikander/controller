import logging

from utils.jax import jax
from utils.events import unschedule, slot

class ChannelSessionEnded:
    
    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - CHANNEL_SESSION_ENDED intent received')

        channel_session = jax.get_key(slots, 'channelSession')
        channel_session_list = jax.get_key(slots, 'channelSessionList', [])
        cc_user_list = jax.get_key(slots, 'ccUserList', [])

        channel_session = jax.get_from_list(channel_session_list, channel_session['id'])
        
        if channel_session is None:
            logging.info('['+conversation['id']+'] - ChannelSession not found')
        else:
            channel_session_list.remove(channel_session)
            logging.info('['+conversation['id']+'] - Channel-Session removed from channel_session_list')


        if not channel_session_list and not cc_user_list:
            
            routing_mode = jax.get_routing_mode_from_channel_session(channel_session)
            agent_state = str(jax.get_key(slots, 'agent_state'))
            logging.info('['+conversation['id']+'] - Agent state: ' + agent_state)
            
            if routing_mode == 'PUSH' and agent_state == 'requested':
                logging.info('['+conversation['id']+'] - Agent was requested, dispatching CANCEL_RESOURCE bot-action')
                dispatcher.action('CANCEL_RESOURCE', {"reasonCode": "CANCELLED"})

            dispatcher.action('END_CONVERSATION')
            logging.info('['+conversation['id']+'] - No channel_sessions and agents remaining in conversation, restarting tracker')
            return [{'type': 'reset'}]

        channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})
        del channel_session_sla_map[channel_session['id']]
        
        return [
            unschedule.customer_sla(conversation['id'], channel_session['id']),
            slot.set('channelSessionList', channel_session_list),
            slot.set('channel_session_sla_map', channel_session_sla_map)
        ]