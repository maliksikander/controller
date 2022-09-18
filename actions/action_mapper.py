from .conversation_started import ConversationStarted
from .agent_ewt import AgentEwt
from .agent_message import AgentMessage
from .agent_outbound import AgentOutbound
from .agent_reserved import AgentReserved
from .agent_subscribed import AgentSubscribed
from .agent_unsubscribed import AgentUnSubscribed
from .channel_session_started import ChannelSessionStarted
from .channel_session_ended import ChannelSessionEnded
from .customer_message import CustomerMessage
from .customer_sla import CustomerSla
from .action_message import ActionMessage
from .bot_message import BotMessage
from .no_agent_available import NoAgentAvailable
from .end_chat import EndChat
from .default import Default


actions = {
    'CONVERSATION_STARTED': ConversationStarted(),
    'AGENT_EWT': AgentEwt(),
    'AGENT_MESSAGE': AgentMessage(),
    'AGENT_OUTBOUND': AgentOutbound(),
    'AGENT_RESERVED': AgentReserved(),
    'AGENT_SUBSCRIBED': AgentSubscribed(),
    'AGENT_UNSUBSCRIBED': AgentUnSubscribed(),
    'CHANNEL_SESSION_STARTED': ChannelSessionStarted(),
    'CHANNEL_SESSION_ENDED': ChannelSessionEnded(),
    'CUSTOMER_MESSAGE': CustomerMessage(),
    'ACTION_MESSAGE': ActionMessage(),
    'BOT_MESSAGE': BotMessage(),
    'NO_AGENT_AVAILABLE': NoAgentAvailable(),
    'end_chat': EndChat(),
    'customer_sla': CustomerSla(),
    'default': Default()
}