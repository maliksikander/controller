from typing import List

class jax:
    
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
    def get_channel_session_from_conversation(conversation: dict):
        try:
            return conversation['metadata']['lastUsedChannelSession']
        except KeyError:
            return None
    
    @staticmethod
    def get_timeout_from_channel_session(channel_session: dict):
        try:
            return channel_session['channel']['channelConfig']['customerActivityTimeout']
        except KeyError:
            return 20
    
    @staticmethod
    def get_routing_mode_from_channel_session(channel_session: dict):
        try:
            return channel_session['channel']['channelConfig']['routingPolicy']['routingMode']
        except KeyError:
            return 'PUSH'
    

        