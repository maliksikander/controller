from .channel_session_expired import ChannelSessionExpired
from .conversation_started import ConversationStarted
from .agent_subscribed import AgentSubscribed
from .agent_unsubscribed import AgentUnSubscribed
from .channel_session_started import ChannelSessionStarted
from .end_chat import EndChat
from .task_state_changed import TaskStateChanged
from .participant_role_changed import ParticipantRoleChanged
from .conversation_paused import ConversationPaused
from .customer_message import CustomerMessage
from .conversation_resumed import ConversationResumed
from .agent_sla_started import AgentSlaStarted
from .agent_sla_expired import AgentSlaExpired
from .customer_sla_started import CustomerSlaStarted
from .customer_sla_expired import CustomerSlaExpired
from .task_enqueued import TaskEnqueued
from .no_response_entity import NoResponseEntity

actions = {
    'CONVERSATION_STARTED': ConversationStarted(),
    'AGENT_SUBSCRIBED': AgentSubscribed(),
    'AGENT_UNSUBSCRIBED': AgentUnSubscribed(),
    'CHANNEL_SESSION_STARTED': ChannelSessionStarted(),
    'CHANNEL_SESSION_EXPIRED': ChannelSessionExpired(),
    'TASK_STATE_CHANGED': TaskStateChanged(),
    'end_chat': EndChat(),
    'PARTICIPANT_ROLE_CHANGED': ParticipantRoleChanged(),
    'CONVERSATION_PAUSED': ConversationPaused(),
    'CUSTOMER_MESSAGE': CustomerMessage(),
    'CONVERSATION_RESUMED': ConversationResumed(),
    'NO_RESPONSE_ENTITY': NoResponseEntity(),
    'TASK_ENQUEUED': TaskEnqueued(),
    'AGENT_SLA_STARTED': AgentSlaStarted(),
    'CUSTOMER_SLA_STARTED': CustomerSlaStarted(),
    'CUSTOMER_SLA_EXPIRED': CustomerSlaExpired(),
    'AGENT_SLA_EXPIRED': AgentSlaExpired(),
}
