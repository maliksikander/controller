import logging

from .utils.utility import Utility
from .utils.events import unschedule, slot


class CallLegStarted:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Intent received", conversation_id)

        call_leg_started_dto = Utility.get_key(slots, 'callLegStartedDto')

        channel_session_id = call_leg_started_dto['dialog']['id']
        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)

        # Return if associated voice channel session is not present
        if channel_session is None:
            self.log_info('Associated channel session not found, returning...', conversation_id)
            return []

        # Stop Customer Inactivity Timer if running
        events = self.stop_inactivity_timer_if_running(slots, conversation_id, channel_session_id)

        agent_id = call_leg_started_dto['agent']['id']
        legs = Utility.get_call_legs(slots, channel_session_id)

        if self.is_agent_present(legs, channel_session_id, agent_id):
            return events

        # Add New Leg to Voice Channel Session
        legs.get(channel_session_id).append(self.create_leg(call_leg_started_dto))
        events.append(slot.set('legs', legs))

        dispatcher.action('ASSIGN_AGENT', {
            'agent': agent_id,
            'channelSession': channel_session,
            'type': 'CISCO_VOICE'
        })

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CALL_LEG_STARTED] | conversation = [' + conversation_id + '] - ' + msg)

    @staticmethod
    def create_leg(call_leg_started_dto):
        return {
            "leg_id": call_leg_started_dto['leg'],
            "agent_id": call_leg_started_dto['agent']['id']
        }

    @staticmethod
    def stop_inactivity_timer_if_running(slots, conversation_id, channel_session_id):
        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})
        events = []

        if Utility.get_key(channel_session_sla_map, channel_session_id, False):
            events.append(unschedule.customer_sla(conversation_id, channel_session_id))
            channel_session_sla_map[channel_session_id] = False
            events.append(slot.set('channel_session_sla_map', channel_session_sla_map))

        return events

    @staticmethod
    def is_agent_present(legs, channel_session_id, agent_id):
        for leg in legs.get(channel_session_id):
            if leg['agent_id'] == agent_id:
                return True
        return False
