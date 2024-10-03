import logging
from .utils.api import API
from .utils.utility import Utility

class NoResponseEntity:
  def run(self, conversation, slots, dispatcher, metadata):
    session = Utility.get_latest_channel_session(conversation)
    dispatcher.action('FIND_AGENT', {'queue': session.get('channel',{}).get('channelConfig',{}).get('routingPolicy',{}).get('routingObjectId',None), 'type': 'ID', 'lastAgentId': API.get_last_agent(conversation['customer']['_id'])})
    logging.info('NoResponseEntity - dispatching FIND_AGENT')
    
    return []
