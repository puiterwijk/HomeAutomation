# Copyright (c) 2014, Patrick Uiterwijk <patrick@puiterwijk.org>
# All rights reserved.
#
# This file is part of HomeAutomation.
#
# HomeAutomation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HomeAutomation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HomeAutomation.  If not, see <http://www.gnu.org/licenses/>.

from abc import ABCMeta, abstractmethod
import time
import stomp
import json
import logging
import argparse

logging.basicConfig()

PREFIX = 'org.puiterwijk.homeautomation'


class BaseModule(object):
    __metaclass__ = ABCMeta

    def __init__(self, description='A homeautomation module',
                 extra_arguments=[]):
        self.args = self._get_params(description,
                                     extra_arguments)

        self.environment = self.args.environment

        self.conn = stomp.Connection(
            host_and_ports=[(self.args.server, self.args.port)],
            use_ssl=True,
            ssl_ca_certs=self.args.cacert,
            ssl_cert_file=self.args.cert,
            ssl_key_file=self.args.key)

        self.conn.set_listener('me', self)
        self.conn.start()
        self.conn.connect()

    def _get_params(self, description, extra_arguments):
        # TODO: Read from config file
        # TODO: Add extra_arguments
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--server', help='Server address',
                            default='queue.puiterwijk.org')
        parser.add_argument('--port', help='Server port',
                            default=61614)
        parser.add_argument('--cacert', help='CA cert file',
                            default='cacert.pem')
        parser.add_argument('--cert', help='Certificate file',
                            default='testcert.pem')
        parser.add_argument('--key', help='Certificate key',
                            default='testcert.key')
        parser.add_argument('--environment', help='environment',
                            default='test')
        return parser.parse_args()

    def work(self):
        while True:
            time.sleep(5)

    def _create_url(self, is_queue, topic):
        parts = [PREFIX, self.environment, topic]
        topic = '.'.join(parts)
        if is_queue:
            return '/queue/%s' % topic
        else:
            return '/topic/%s' % topic

    def send(self, topic, message, is_queue=False, **kwargs):
        url = self._create_url(is_queue, topic)
        self.conn.send(url, json.dumps(message), **kwargs)

    def subscribe(self, topic, is_queue=False, name=None, **kwargs):
        url = self._create_url(is_queue, topic)
        if not name:
            name = topic
        self.conn.subscribe(destination=url,
                            id=name,
                            **kwargs)

    def on_error(self, headers, message):
        print 'ERROR! Heades: %s, message: %s' % (headers, message)

    def on_message(self, headers, message):
        _, msgtype, destination = headers['destination'].split('/')
        if not destination.startswith(PREFIX):
            # We do not care about this message
            return
        destination = destination[len(PREFIX)+1:]
        destination = destination.split('.', 1)
        if destination[0] != self.environment:
            # Wrong environment
            return
        topic = destination[1]
        try:
            body = json.loads(message)
        except:
            body = None
        self.message_received(topic, body)

    @abstractmethod
    def message_received(self, topic, body):
        pass
