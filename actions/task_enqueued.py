import logging


class TaskEnqueued:
  def run(self, conversation, slots, dispatcher, metadata):
      
    dispatcher.text("You're routed to an agent, he/she will join in a moment.")
    
    return []
