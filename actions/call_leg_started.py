import logging

from .utils.utility import Utility


class CallLegStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Intent received", conversation_id)

        call_leg_started_dto = Utility.get_key(slots, 'callLegStartedDto')

        channel_session = Utility.get_channel_session_by_id(str(call_leg_started_dto['channelSessionId']), conversation)
        agent_id = str(call_leg_started_dto['agent']['id'])
        agent = Utility.get_agent_by_id(agent_id, conversation)

        # Return if associated voice channel session is not present
        if channel_session is None:
            self.log_info('Associated channel session not found, returning...', conversation_id)
            return []

        # Return if the requesting agent is already in the conversation
        if agent is not None:
            self.log_info('Agent is already in the conversation, returning...', conversation_id)
            return []

        self.log_info('Dispatching ASSIGN_AGENT action', conversation_id)
        dispatcher.action('ASSIGN_AGENT', {
            'agent': agent_id,
            'channelSession': channel_session,
            'type': 'CISCO_VOICE'
        })
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CALL_LEG_STARTED] | conversation = [' + conversation_id + '] - ' + msg)
