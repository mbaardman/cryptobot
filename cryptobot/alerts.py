"""
Author: Marc Baardman
"""

import os
import sys
from twilio.rest import Client as twilio_client
import time
import config

class SMSAlerts(object):

    def __init__(self, account, token, from_phone, to_phone):
        self.client = twilio_client(account, token)
        self.from_phone = from_phone
        self.to_phone = to_phone

    def _send(self, message):
        message = self.client.messages.create(body = message,
                                    from_ = self.from_phone,
                                    to = self.to_phone)


    def alert(self, test_message, ask_permission = False, sleep_seconds = 40):
        self._send(test_message)
        if ask_permission:
             action = self._wait_for_permission(sleep_seconds)
             return action
        return 'continue'

    def _wait_for_permission(self, sleep_seconds):
        time.sleep(sleep_seconds)
        last_messages = Alert.client.messages.list(limit=2)
        for record in last_messages:
            if (record.direction == 'inbound') & ('ee' in record.body.lower()):
                self._send('Process will be interupted.')
                return 'stop'
        self._send('Process will continue.')
        return 'continue'


if __name__ == "__main__":
    Alert = SMSAlerts(config.twilio_account, config.twilio_token, config.twilio_from_phone, config.twilio_to_phone)
    text = 'We gaan 10.000 euro in niks investeren'
    action = Alert.alert(text, ask_permission = True, sleep_seconds = config.sleep_seconds)
    print('komt per ongeluk in de name==main')
    messages = Alert.client.messages.list(limit=20)#
    #
    for record in messages:
        print(record.direction)
        print(record.body)
        print(record.sid)
