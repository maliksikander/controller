import logging

from utils.jax import jax

class EndChat:

    def run(self, conversation, slots, dispatcher, metadata):
    
        channel_session = jax.get_channel_session_from_conversation(conversation)

        if channel_session is None:
            logging.info('['+conversation['id']+'] - ChannelSession not found, will not post channel_session_expired')
        else:
            logging.info('['+conversation['id']+'] - Posting CHANNEL_SESSION_EXPIRED bot-action')
            dispatcher.action('CHANNEL_SESSION_EXPIRED', {
                "channelSession": channel_session
            })

        return []