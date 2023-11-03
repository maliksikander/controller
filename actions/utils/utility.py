class Utility:
    @staticmethod
    def get_key(obj: dict, key: str, default=None):
        if key in obj.keys():
            return obj[key]
        else:
            return default

    @staticmethod
    def get_routing_mode(conversation):
        return str(conversation['channelSession']['channel']['channelConfig']['routingPolicy']['routingMode'])
    
    @staticmethod
    def get_latest_channel_session(conversation: dict):
        try:
            return conversation['metadata']['lastUsedChannelSession']
        except KeyError:
            return None

    @staticmethod
    def is_customer_present(conversation):
        return len(Utility.get_channel_sessions(conversation)) > 0

    @staticmethod
    def get_agent_by_id(agent_id, conversation):
        agents = Utility.get_agents(conversation)
        for agent in agents:
            if agent['id'] == agent_id:
                return agent
        return None

    @staticmethod
    def get_channel_session_by_id(channel_session_id, conversation):
        channel_sessions = Utility.get_channel_sessions(conversation)
        for channel_session in channel_sessions:
            if channel_session['id'] == channel_session_id:
                return channel_session
        return None

    @staticmethod
    def get_channel_sessions(conversation):
        return Utility.get_participants(conversation, 'CUSTOMER')

    @staticmethod
    def get_agents(conversation):
        return Utility.get_participants(conversation, 'AGENT')

    @staticmethod
    def get_bots(conversation):
        return Utility.get_participants(conversation, 'BOT')

    @staticmethod
    def get_participants(conversation, participant_type):
        participants = conversation['participants']
        result = []

        for participant in participants:
            if participant['type'] == participant_type:
                result.append(participant['participant'])

        return result

    @staticmethod
    def get_bot_participant(conversation):
        participants = conversation['participants']

        for participant in participants:
            if participant['type'] == 'BOT':
                return participant

        return None

    @staticmethod
    def dispatch_flushed_task_msg(dispatcher, task, msg):
        if task['state']['name'] == 'CLOSED' and task['state']['reasonCode'] == 'FORCE_CLOSED':
            task_type = task['activeMedia'][len(task['activeMedia']) - 1]['type']
            if not (task_type['direction'] == 'DIRECT_CONFERENCE' and task_type['mode'] == 'QUEUE'):
                dispatcher.text(msg)

    @staticmethod
    def change_bot_participant_role(role, dispatcher, conversation):
        bot_participant = Utility.get_bot_participant(conversation)
        if bot_participant is not None and bot_participant['role'] != role:
            bot_id = bot_participant['participant']['id']
            dispatcher.action('CHANGE_PARTICIPANT_ROLE', {"participantId": bot_id, "role": role})

    @staticmethod
    def create_agent_state(state, direction):
        return {
            "state": state,
            "direction": direction
        }
    
    @staticmethod
    def is_all_agent_in_wrap_up(conversation):
        participants = conversation['participants']
        agent_count = 0
        agent_wrap_up_count = 0
        if participants is None:
            return False
    
        for p in participants:
            if p['type'] == 'AGENT':
                agent_count += 1
                if p['role'] == 'WRAP_UP':
                    agent_wrap_up_count += 1
    
        return agent_count > 0 and agent_count == agent_wrap_up_count

      
