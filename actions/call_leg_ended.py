import logging

from .utils.utility import Utility
from .utils.events import schedule, slot


class CallLegEnded:
    def run(self, conversation, slots, dispatcher, metadata):
        conversation_id = conversation['id']
        self.log_info("Intent received", conversation_id)

        call_leg_ended_dto = Utility.get_key(slots, 'callLegEndedDto')
        channel_session_id = str(call_leg_ended_dto['channelSessionId'])
        agent_id = str(call_leg_ended_dto['agent']['id'])

        channel_session = Utility.get_channel_session_by_id(channel_session_id, conversation)
        legs = Utility.get_call_legs(slots, channel_session['id'])
        events = []

        if not channel_session:
            del legs[channel_session['id']]
            return [slot.set('legs', legs)]

        self.remove_leg(legs, channel_session['id'], agent_id)
        events.append([slot.set('legs', legs)])

        # Start inactivity timer if no Call Legs left
        if not legs.get(channel_session['id']):
            events.extend(self.start_inactivity_timer(slots, conversation_id, channel_session))

        return events

    @staticmethod
    def remove_leg(legs, channel_session_id, agent_id):
        leg = next((x for x in legs.get(channel_session_id) if x["agent_id"] == agent_id), None)

        if leg is not None:
            legs.get(channel_session_id).remove(leg)
            return True

        return False

    @staticmethod
    def start_inactivity_timer(slots, conversation_id, channel_session):
        channel_session_sla_map = Utility.get_key(slots, 'channel_session_sla_map', {})

        # Customer inactivity already running, return...
        if channel_session_sla_map[channel_session['id']]:
            return []

        # Start customer inactivity timer
        events = []
        channel_session_sla_map[channel_session['id']] = True
        inactivity_timeout = Utility.get_inactivity_timeout(channel_session)

        events.append(slot.set('channel_session_sla_map', channel_session_sla_map))
        events.append(schedule.customer_sla(conversation_id, channel_session['id'], inactivity_timeout))

        return events

    @staticmethod
    def log_info(msg, conversation_id):
        logging.info('[CALL_LEG_ENDED] | conversation = [' + conversation_id + '] - ' + msg)
