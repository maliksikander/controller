import logging

from utils.jax import jax

class AgentOutbound:

    def run(self, conversation, slots, dispatcher, metadata):
        
        agent_outbound_dto = jax.get_key(slots, 'agentOutboundDto')
        logging.info('['+conversation['id']+'] - Agent_Outbound request received - AgentOutboundDto: ' + str(agent_outbound_dto))

        channel_session = jax.get_channel_session_from_conversation(conversation)

        if channel_session is None:
            logging.info('['+conversation['id']+'] - No ChannelSession found for this Agent-Outbound request')
            return []

        agent_id = agent_outbound_dto['agentId']

        if jax.is_exist_in_list(jax.get_key(slots, 'ccUserList', []), agent_id):
            logging.info('['+conversation['id']+'] - Agent: ' + str(agent_id) + ' already exist in this conversation')
            return []

        dispatcher.action('ASSIGN_AGENT', {
            'agent': agent_id,
            'channelSession': channel_session
        })
        return []
