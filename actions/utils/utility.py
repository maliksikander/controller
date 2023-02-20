from typing import List


class Utility:
    @staticmethod
    def is_exist_in_list(list: List[dict], key: str, key_type: str = 'id'):
        for item in list:
            if item[key_type] == key:
                return True
        return False

    @staticmethod
    def get_from_list(list: List[dict], key: str, key_type: str = 'id', default = None):
        return next((x for x in list if x[key_type] == key), default)

    @staticmethod
    def get_key(object: dict, key: str, default = None):
        if key in object.keys():
            return object[key]
        else:
            return default
    
    @staticmethod
    def get_latest_channel_session(conversation: dict):
        try:
            return conversation['metadata']['lastUsedChannelSession']
        except KeyError:
            return None
    
    @staticmethod
    def get_inactivity_timeout(channel_session):
        return channel_session['channel']['channelConfig']['customerActivityTimeout']
    
    @staticmethod
    def get_routing_mode_from(channel_session: dict):
        try:
            return channel_session['channel']['channelConfig']['routingPolicy']['routingMode']
        except KeyError:
            return 'PUSH'

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
    def create_agent_state(state, direction):
        return {
            "state": state,
            "direction": direction
        }

    @staticmethod
    def get_assign_agent_payload(agent_id, channel_session, direction, update_task):
        return {
            'agent': agent_id,
            'channelSession': channel_session,
            'direction': direction,
            'updateTask': update_task
        }

    @staticmethod
    def get_find_agent_payload(queue_name, queue_type, offer_to_agent):
        return {
            "queue": queue_name,
            "type": queue_type,
            "offerToAgent": offer_to_agent
        }
