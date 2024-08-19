import requests
import logging

class API:
    
  @staticmethod
  def get_encrypted_str(customer_identifier: str, agent_id: dict):
    url = "http://192.168.2.48:1880/control/Received1?Mobile_Number=PSTN%3D\"pstnno\"%3BAgentID%3D\"+LoginName"
    response = requests.get(url)
    
    if response.status_code == 200:
      data = response.json()
      logging.info('API - get_encrypted_str - code: 200 - response: '+str(data))
      return data.get('encrypted')
    
    logging.error('API - get_encrypted_str - code: '+response.status_code+' - response: '+str(response.text))
    return ''