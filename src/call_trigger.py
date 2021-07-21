
# Twilio Console
# https://console.twilio.com

from twilio.rest import Client

from config import config
import logging

client = Client()

call_from = config['call_origin']
call_to = config['call_destination']
twiml_url = config['twiml_url']


def make_call():    
    logging.info('making a call ...')
    logging.info('calling from: %s', call_from)
    logging.info('calling: %s', call_to)

    call = client.calls.create(
        from_=call_from,
        to=call_to,
        url=twiml_url
    )

