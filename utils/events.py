
class schedule:

    @staticmethod
    def customer_sla(conversation_id: str, channel_session_id: str, timeout: int):
        return {
            'type': 'schedule_a_reminder',
            'name': 'customer_sla' + '_' + conversation_id + '_' + channel_session_id,
            'intent': 'customer_sla',
            'entities':{'customer_sla_metadata': channel_session_id},
            'duration': timeout,
            'kill_on_customer_message': False,
            'metadata': 'the metadata'
        }


class slot:
    
    @staticmethod
    def set(name: str, value: any):
        return {
            'type': 'set_a_slot',
            'name': name,
            'value': value
        }


class unschedule:

    @staticmethod
    def customer_sla(conversation_id: str, channel_session_id: str):
        return {
            'type': 'unschedule_a_reminder',
            'name': 'customer_sla' + '_' + conversation_id + '_' + channel_session_id
        }
