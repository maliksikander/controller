import logging


class NoResponseEntity:
  def run(self, conversation, slots, dispatcher, metadata):
    
    dispatcher.action('FIND_AGENT', {'queue': 'Queue-1', 'type': 'NAME'})
    logging.info('NoResponseEntity - dispatching FIND_AGENT')
    
    return []
