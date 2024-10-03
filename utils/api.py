import requests
import logging

class API:

    @staticmethod
    def get_last_agent(customer_id):
        url = 'http://ef-conversation-manager-svc.expertflow.svc:8080/customer-topics/' + customer_id + '/last-routed-agent'
        response = requests.get(url)

        logging.info('API - get_last_agent - url = '+str(url) + ' code = ' + str(response.status_code) + ' content = ' + str(response.text))

        if response.status_code == 200 and str(response.text) != '':
            return str(response.text)

        return None
