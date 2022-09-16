import logging

from utils.jax import jax
from utils.events import schedule, slot

class ChannelSessionStarted:
    
    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - Channel-session-started intent received')
        
        channel_session = jax.get_key(slots, 'channelSession')
        channel_session['participantType'] = 'ChannelSession'
        
        channel_session_list = jax.get_key(slots, 'channelSessionList', [])
        events = []

        
        channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})
        channel_session_sla_map[channel_session['id']] = False
        
        channel_session_list.append(channel_session)
        logging.info('['+conversation['id']+'] - channel-session added to conversation successfully')

        for c_session in channel_session_list:
            if not jax.get_key(channel_session_sla_map, c_session['id'], False):
                channel_session_sla_map[c_session['id']] = True
                events.append(schedule.customer_sla(conversation['id'], channel_session['id'], jax.get_timeout_from_channel_session(c_session)))
        

        latest_intent = jax.get_key(channel_session, 'latestIntent')
        logging.info('['+conversation['id']+'] - Latest intent in channel Session: ' + str(latest_intent))

        if not latest_intent:
            logging.info('['+conversation['id']+'] - Latest intent is Empty, Dispatching welcome message')
            dispatcher.text('Hey! this is sparrow from Expertflow. How may i help you today?')

        events.extend([
            slot.set('channelSessionList', channel_session_list),
            slot.set('channel_session_sla_map', channel_session_sla_map)
        ])

        return events
