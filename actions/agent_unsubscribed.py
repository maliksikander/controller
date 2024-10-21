    import logging

    from .utils.utility import Utility
    from .utils.api import API


    class AgentUnSubscribed:
        def run(self, conversation, slots, dispatcher, metadata):
            room_info = (Utility.get_key(slots, 'cimEvent'))['roomInfo']

            reason_code = str((Utility.get_key(slots, 'cimEvent'))['data']['reason'])
            self.log_info("intent received", str(room_info['id']), conversation)

            if str(room_info['mode']) == "PRIVATE":
                self.log_info("Room-mode: Private, Ignoring this intent", str(room_info['id']), conversation)
                return []

            participants = conversation.get('participants', [])

            # Get channel sessions of 'CUSTOMER' type
            customer_channel_sessions = [
                participant.get('participant') for participant in participants
                if participant.get('type') == 'CUSTOMER'
            ]

            for customer_channel_session in customer_channel_sessions:
                mrd_id = customer_channel_session['channel']['channelType']['mediaRoutingDomain']

                # If mrd_id matches and the reason is 'FORCED_LOGOUT', dispatch action
                if mrd_id == '62f9e360ea5311eda05b0242' and reason_code == 'FORCED_LOGOUT':
                    self.log_info("Agent forcefully logged out on voice channel, dispatching REMOVE_CHANNEL_SESSION", str(room_info['id']), conversation)
                    dispatcher.action('REMOVE_CHANNEL_SESSION', {"channelSession": customer_channel_session, "reasonCode": "FORCE_CLOSED"})
                    return []


            if not Utility.get_agents(conversation) and Utility.is_customer_present(conversation):
                Utility.change_bot_participant_role('PRIMARY', dispatcher, conversation)

                routing_mode = Utility.get_routing_mode(conversation)

                # If agent was unsubscribed by system, due to SLA_EXPIRED, or due to MRD_INTERRUPTED then find another agent on this conversation
                if routing_mode == 'PUSH' and (reason_code == 'FORCED_LOGOUT' or reason_code == 'SLA_EXPIRED' or reason_code == 'MRD_INTERRUPTED'):
                    self.log_info('Dispatching FIND_AGENT', str(room_info['id']), conversation)
                    dispatcher.action('FIND_AGENT', {'lastAgentId': API.get_last_agent(conversation['customer']['_id'])})

            return []

        @staticmethod
        def log_info(msg, room_id, conversation):
            conversation_id = str(None if not conversation else conversation['id'])
            logging.info(
                '[AGENT_UNSUBSCRIBED] | room = [' + room_id + '] | conversation = [' + conversation_id + '] - ' + msg)
