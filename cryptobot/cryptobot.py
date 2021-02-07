
from twilio.rest import Client as twilio_client
import time
import sys
## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('../..')
    import config_secured as config
else:
    import config
    
    
class Cryptobot:
    """
    Created this class to bundle all functions and attributes that are applicable to all objects.
    """

    def __init__(self):
        print('cryptobot is initialized...')
        params = config.twilio_parameters
        self._twilio_client = twilio_client(params['account'], params['token'])
        print('Client is initialized...')
        self.from_phone = params['from_phone']
        self.to_phone = params['to_phone']
        
    def why_this_bot(self):
        print('just for fun')
    
    def _send(self, message):
        self._twilio_client.messages.create(body=message, from_=self.from_phone, to=self.to_phone)

    def create_alert(self, msg, permission = False, sleep = config.twilio_sleep):
        self._send(msg)
        if permission:
             action = self._wait_for_permission(sleep)
             return action
        return 'continue'

    def _wait_for_permission(self, sleep_seconds):
        time.sleep(sleep_seconds)
        last_messages = self._twilio_client.messages.list(limit=2)
        for record in last_messages:
            if (record.direction == 'inbound') & ('ee' in record.body.lower()):
                self._send('Process will be interupted.')
                return 'stop'
        self._send('Process will continue.')
        return 'continue'

if __name__ == "__main__":
    Alert = Cryptobot()
    text = 'We gaan 10.000 euro in niks investeren'
    action = Alert.create_alert(text)
