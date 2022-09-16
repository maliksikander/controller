import logging

from utils.jax import jax
from utils.events import schedule, slot

class AgentUnSubscribed:
    
    def run(self, conversation, slots, dispatcher, metadata):
               
        cc_user = jax.get_key(slots, 'ccUser')
        cc_user_list = jax.get_key(slots, 'ccUserList', [])
        channel_session_list = jax.get_key(slots, 'channelSessionList', [])

        logging.info('['+conversation['id']+'] - AGENT_UNSUBSCRIBED intent received - Number of ChannelSessions = ['+str(len(channel_session_list))+'] - Number of Agents = ['+str(len(cc_user_list))+']')

        cc_user = jax.get_from_list(cc_user_list, cc_user['id'])
        
        if cc_user is None:
            logging.info('['+conversation['id']+'] - Agent not found')
        else:
            cc_user_list.remove(cc_user)
            logging.info('['+conversation['id']+'] - Agent removed successfully')


        if not cc_user_list and not channel_session_list:
            logging.info('['+conversation['id']+'] - No Participant left in conversation, sending end-conversation')
            dispatcher.action('END_CONVERSATION')
            return [{'type': 'reset'}]

        elif channel_session_list and not cc_user_list:
            channel_session = channel_session_list[len(channel_session_list) - 1]

            channel_session_sla_map = jax.get_key(slots, 'channel_session_sla_map', {})
            channel_session_sla_map[channel_session['id']] = True

            routing_mode = jax.get_routing_mode_from_channel_session(channel_session)
            reason_code = jax.get_key(slots, 'agentSubUnSubReason')

            events = [
                schedule.customer_sla(conversation['id'], channel_session['id'], jax.get_timeout_from_channel_session(channel_session)),
                slot.set('ccUserList', cc_user_list),
                slot.set('channel_session_sla_map', channel_session_sla_map)
            ]

            if routing_mode == 'PUSH' and reason_code == 'FORCED_LOGOUT':
                logging.info('['+conversation['id']+'] - Customer exists, No agent left, rMode=PUSH, reason=Forced-Logout, Dispatching find-agent')
                dispatcher.action('FIND_AGENT')
                events.append(slot.set('agent_state', 'requested'))
                return events
            
            events.append(slot.set('agent_state', 'not_requested'))
            return events

        else:
            return [
                slot.set('ccUserList', cc_user_list)
            ]
