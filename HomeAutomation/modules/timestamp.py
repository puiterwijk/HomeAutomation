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

import time

from HomeAutomation import BaseModule


class TimeModule(BaseModule):
    def __init__(self):
        super(TimeModule, self).__init__()
        self.subscribe('time.get.request',
                       True,
                       exclusive=True)

    def work(self):
        while True:
            self.send('time.tick',
                      {'timestamp': int(time.time())})
            time.sleep(5)

    def message_received(self, topic, body):
        if topic == 'time.get.request':
            self.send('time.get.response',
                      {'timestamp': int(time.time())})


def run():
    module = TimeModule()
    module.work()
