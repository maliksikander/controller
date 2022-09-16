import logging

class AgentEWT:
    
    def run(self, conversation, slots, dispatcher, metadata):
        
        logging.info('['+conversation['id']+'] - Going to send a message [agent will join soon]')

        dispatcher.text("You're in queue, please wait an agent will come to you soon")
        return []