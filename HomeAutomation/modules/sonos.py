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

import soco

from HomeAutomation import BaseModule


class SonosModule(BaseModule):
    def __init__(self):
        super(SonosModule, self).__init__()
        self.subscribe('music.sonos.topology.request',
                       True,
                       exclusive=True)

    def message_received(self, topic, body):
        if topic == 'music.sonos.topology.request':
            self.send('music.sonos.topology.response',
                      {player.ip_address: player.player_name
                       for player in soco.discover()})


def run():
    module = SonosModule()
    module.work()
