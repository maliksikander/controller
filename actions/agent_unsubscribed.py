import logging

from .utils.utility import Utility
from .utils.events import schedule, slot


class AgentUnSubscribed:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info('AGENT_UNSUBSCRIBED intent received', conversation_id)

        cc_user_list = Utility.get_agents(conversation)
        channel_session_list = Utility.get_channel_sessions(conversation)

        self.log_info('Number of ChannelSessions = [' + str(len(channel_session_list)) + ']', conversation_id)
        self.log_info('Number of Agents = ['+str(len(cc_user_list))+']', conversation_id)

        if not cc_user_list and not channel_session_list:
            self.log_info("No Participant left in conversation, sending end-conversation", conversation_id)
            dispatcher.action('END_CONVERSATION')
            return [{'type': 'reset'}]

        if channel_session_list and not cc_user_list:
            channel_session = Utility.get_latest_channel_session(conversation)

            channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
            channel_session_sla_map[channel_session['id']] = True

            inactivity_timeout = Utility.get_inactivity_timeout(channel_session)
            schedule_timer = schedule.customer_sla(conversation_id, channel_session['id'], inactivity_timeout)

            events = [schedule_timer, slot.set('channel_session_sla_map', channel_session_sla_map)]

            routing_mode = Utility.get_routing_mode_from(channel_session)
            reason_code = Utility.get_key(slots, 'agentSubUnSubReason')

            if routing_mode == 'PUSH' and reason_code == 'FORCED_LOGOUT':
                self.log_info("Customer exists, No agent left, rMode=PUSH, reason=Forced-Logout, "
                              "Dispatching find-agent", conversation_id)
                dispatcher.action('FIND_AGENT')
                events.append(slot.set('agent_state', 'requested'))
                return events
            
            events.append(slot.set('agent_state', 'not_requested'))
            return events

        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_UNSUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)
