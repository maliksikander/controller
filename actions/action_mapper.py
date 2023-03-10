from .channel_session_expired import ChannelSessionExpired
from .conversation_started import ConversationStarted
from .agent_subscribed import AgentSubscribed
from .agent_unsubscribed import AgentUnSubscribed
from .channel_session_started import ChannelSessionStarted
from .end_chat import EndChat
from .default import Default
from .task_state_changed import TaskStateChanged

actions = {
    'CONVERSATION_STARTED': ConversationStarted(),
    'AGENT_SUBSCRIBED': AgentSubscribed(),
    'AGENT_UNSUBSCRIBED': AgentUnSubscribed(),
    'CHANNEL_SESSION_STARTED': ChannelSessionStarted(),
    'CHANNEL_SESSION_EXPIRED': ChannelSessionExpired(),
    'TASK_STATE_CHANGED': TaskStateChanged(),
    'end_chat': EndChat(),
    'default': Default()
}
