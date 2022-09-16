import logging

from utils.jax import jax
from utils.events import schedule, unschedule, slot

class CustomerMessage:

    def run(self, conversation, slots, dispatcher, metadata):
        
        message = 'hello!'

        logging.info('['+conversation['id']+'] - Customer Message Received: ' + message)

        channel_session = jax.get_channel_session_from_conversation(conversation)
        channel_session_list = jax.get_key(slots, 'channelSessionList', [])
        cc_user_list = jax.get_key(slots, 'ccUserList', [])
        channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})

        agents_present_in_conversation = cc_user_list is not None and len(cc_user_list) > 0
        
        events = []
        for c_session in channel_session_list:
            # Skip the current channel session
            if c_session['id'] == channel_session['id']:
                continue

            if not jax.get_key(channel_session_sla_map, channel_session['id'], False):
                events.append(schedule.customer_sla(conversation['id'], channel_session['id'], jax.get_timeout_from_channel_session(channel_session)))
        
        if agents_present_in_conversation:
            events.append(unschedule.customer_sla(conversation['id'], channel_session['id']))
        
        else:
            routing_mode = jax.get_routing_mode_from_channel_session(channel_session)

            if routing_mode == 'PUSH':
                logging.info('['+conversation['id']+'] - PUSH mode, Handling Push mode on low confidence..')

                if jax.get_key(slots, 'agent_state') == 'requested':
                    dispatcher.text('An agent has been requested for this conversation, he/she will join you shortly. Please wait!')
                    events.append(unschedule.customer_sla(conversation['id'], channel_session['id']))
                else:
                    dispatcher.text('Bot could not understand your message, an Agent will join you shortly')
                    dispatcher.action('FIND_AGENT')
                    events.extend([
                        unschedule.customer_sla(conversation['id'], channel_session['id']),
                        slot.set('agent_state', 'requested')
                    ])
            
            elif routing_mode == 'PULL':
                logging.info('['+conversation['id']+'] - PULL mode, Handling Pull mode on low confidence..')
                dispatcher.text('Bot could not understand your message, all relevant agents have been notified, agent(s) will join you shortly. Please wait!')
                events.append(unschedule.customer_sla(conversation['id'], channel_session['id']))
        
        return events
