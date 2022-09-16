import logging

from utils.jax import jax
from utils.events import slot

class AgentSubscribed:
    
    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - AGENT_SUBSCRIBED intent called')

        cc_user = jax.get_key(slots, 'ccUser')
        cc_user_list = jax.get_key(slots, 'ccUserList', [])
        channel_session_list = jax.get_key(slots, 'channelSessionList', [])

        if not channel_session_list:
            logging.info('['+conversation['id']+'] - Dispatching REVOKE_REQUEST bot-action, Customer has left')
            
            dispatcher.action('REVOKE_REQUEST', {"reasonCode": "CANCELLED"})
            agent_state = slot.set('agent_state', 'not_requested')
        
        else:
            cc_user_list.append(cc_user)
            agent_state = slot.set('agent_state', 'subscribed')
            logging.info('['+conversation['id']+'] - Agent added to this conversation successfully.')

        return [
            agent_state,
            slot.set('ccUserList', cc_user_list)
        ]