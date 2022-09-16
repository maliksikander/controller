import logging

class AgentReserved:
    
    def run(self, conversation, slots, dispatcher, metadata):

        logging.info('['+conversation['id']+'] - An agent has been reserved for this conversation')

        dispatcher.text('An agent has been reserved for you, please wait agent will join you soon')
        return []
