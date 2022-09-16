import logging
from utils.jax import jax

class CustomerSLA:
    
    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - Customer activity timer expired')

        channel_session_list = jax.get_key(slots, 'channelSessionList', [])
        channel_session_id = jax.get_key(slots, 'customer_sla_metadata')
        channel_session = jax.get_from_list(channel_session_list, channel_session_id)

        if channel_session is None:
            logging.info('['+conversation['id']+'] - ChannelSession not found, will not post channel_session_expired')
        
        elif not jax.get_key(jax.get_key(slots, 'channel_session_sla_map', {}), channel_session['id'], False):
            logging.info('['+conversation['id']+'] - Invalid state: Customer-activity-timer flag false, will not post channel_session_expired')
        
        else:
            logging.info('['+conversation['id']+'] - Posting CHANNEL_SESSION_EXPIRED bot-action')
            dispatcher.action('CHANNEL_SESSION_EXPIRED', {
                "channelSession": channel_session
            })

        return []