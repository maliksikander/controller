import logging
from .utils.utility import Utility


class AgentOutbound:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']

        agent_outbound_dto = Utility.get_key(slots, 'agentOutboundDto')
        self.log_info("Agent_Outbound request received - AgentOutboundDto: " + str(agent_outbound_dto), conversation_id)

        channel_session_id = agent_outbound_dto['channelSessionId']
        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)

        if channel_session is None:
            self.log_info("No ChannelSession found for this Agent-Outbound request", conversation_id)
            return []

        agent_id = agent_outbound_dto['agentId']
        agent = Utility.get_agent_by_id(agent_id, conversation)

        if agent is not None:
            self.log_info('Agent: ' + str(agent_id) + ' already exist in this conversation', conversation_id)
            return []

        dispatcher.action('ASSIGN_AGENT', Utility.get_assign_agent_payload(agent_id, channel_session,
                                                                           'OUTBOUND', False))
        return []

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[AGENT_OUTBOUND] | conversation = [' + conversation_id + '] - ' + msg)
