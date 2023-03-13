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

        if not cc_user_list:  # All agents left
            agent_state = Utility.get_key(slots, 'agent_state', Utility.create_agent_state('not_requested', None))
            direction = agent_state['direction']

            if agent_state['state'] == 'requested' and direction == 'DIRECT_CONFERENCE':
                self.dispatch_cancel_resource(dispatcher, conversation_id)

            if not channel_session_list:  # Customer has left
                self.dispatch_end_conversation(dispatcher, conversation_id)
                return [{'type': 'reset'}]
            else:  # Customer is still present
                self.if_bot_in_conversation_make_it_primary(dispatcher, conversation)
                events = self.schedule_inactivity_timer(slots, conversation)

                if agent_state['state'] == 'requested' and direction == 'DIRECT_TRANSFER':
                    return events

                routing_mode = Utility.get_routing_mode_from(conversation['channelSession'])
                reason_code = Utility.get_key(slots, 'agentSubUnSubReason')

                if routing_mode == 'PUSH' and reason_code == 'FORCED_LOGOUT':
                    self.log_info("Customer exists, No agent left, rMode=PUSH, reason=Forced-Logout, "
                                  "Dispatching find-agent", conversation_id)

                    dispatcher.action('FIND_AGENT')
                    events.append(slot.set('agent_state', Utility.create_agent_state('requested', 'INBOUND')))
                    return events

                events.append(slot.set('agent_state', Utility.create_agent_state('not_requested', None)))
                return events

        return []

    @staticmethod
    def schedule_inactivity_timer(slots, conversation):
        channel_session = Utility.get_latest_channel_session(conversation)

        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        channel_session_sla_map[channel_session['id']] = True

        inactivity_timeout = Utility.get_inactivity_timeout(channel_session)
        schedule_timer = schedule.customer_sla(conversation['id'], channel_session['id'], inactivity_timeout)

        return [schedule_timer, slot.set('channel_session_sla_map', channel_session_sla_map)]

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_UNSUBSCRIBED] | conversation = [' + conversation_id + '] - ' + msg)

    def dispatch_cancel_resource(self, dispatcher, conversation_id):
        self.log_info("Agent was requested for conference, current agent(s) left, "
                      "dispatching CANCEL_RESOURCE bot-action", conversation_id)
        dispatcher.action('CANCEL_RESOURCE', {"reasonCode": "CANCELLED"})

    def dispatch_end_conversation(self, dispatcher, conversation_id):
        self.log_info("Customer and Agent(s) left the conversation, ending conversation", conversation_id)
        dispatcher.action('END_CONVERSATION')

    @staticmethod
    def if_bot_in_conversation_make_it_primary(dispatcher, conversation):
        bot_participant = Utility.get_bot_participant(conversation)
        if bot_participant is not None:
            bot_id = bot_participant['participant']['id']
            role = 'PRIMARY'
            dispatcher.action('CHANGE_PARTICIPANT_ROLE', {"participantId": bot_id, "role": role})
