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

from HomeAutomation import BaseModule


class PublishModule(BaseModule):
    def __init__(self):
        super(PublishModule, self).__init__()

    def add_extra_arguments(self, parser):
        parser.add_argument('topic', help='Message topic to send')
        parser.add_argument('message', help='Message to send')
        parser.add_argument('--queue', help='Set to send as a queue message',
                            action='store_true')

    def work(self):
        self.send(self.args.topic,
                  self.args.message,
                  self.args.queue)
        self.conn.disconnect()

    def message_received(self, topic, body):
        print 'Message [%s]: %s' % (topic, body)


def run():
    module = PublishModule()
    module.work()
