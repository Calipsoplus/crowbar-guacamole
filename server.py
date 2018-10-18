import logging
from threading import Thread
from urlparse import parse_qs

import configparser
from cryptography.fernet import Fernet
from geventwebsocket import WebSocketApplication, WebSocketServer, Resource
from collections import OrderedDict
from guacamole.client import GuacamoleClient

port = 8000  # Default port for this server


class GuacamoleApplication(WebSocketApplication):
    def __init__(self, ws):
        self.client = None
        super(GuacamoleApplication, self).__init__(ws)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        # self.fernet = Fernet(bytes(self.config['DEFAULT']['FERNET_KEY']))
        logging.basicConfig(filename='crowbar-guacamole.log', level=logging.DEBUG)

    @classmethod
    def protocol_name(cls):
        return "guacamole"

    def on_message(self, message, **kwargs):
        self.client.send(message)

    def on_open(self):
        # TODO implement check for token
        parameters = parse_qs(self.ws.environ['QUERY_STRING'])
        self.client = GuacamoleClient(str(self.config['DEFAULT']['GUACD_HOST']), 4822)
        self.client.handshake(protocol='rdp',
                              hostname=parameters['hostname'][0],
                              port=3389,
                              width=parameters['width'][0],
                              height=parameters['height'][0])
        self.start_read_listener()

    def on_close(self, reason):
        self.client.close()
        self.client = None

    def start_read_listener(self):
        listener = Thread(target=self.read_listener)
        listener.start()

    def read_listener(self):
        """
        A listener that would handle any messages sent from Guacamole server
        and push directly to browser client (over websocket).
        """
        while True:
            instruction = self.client.receive()
            self.ws.send(instruction)


if __name__ == '__main__':
    print "Running on port:", port
    WebSocketServer(('0.0.0.0', port), Resource(OrderedDict([('/', GuacamoleApplication)]))).serve_forever()