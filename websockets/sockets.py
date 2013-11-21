"""
Websocket code to keep track of all open connections.
"""

__copyright__ = """
Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2013

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class WebSockets():
    local = None
    local_conference = None
    sip_connections = {}
    clients = []
    subscriptions = {}

    def _convert_message(self, message_type, message_data):
        return json.dumps({ 
            'message_type': message_type, 
            'data': message_data
        })

    def send_local(self, message_type, message_data):
        data = self._convert_message(message_type, message_data)
        self.local.send(data)

    def send_conference(self, message_type, message_data):
        data = self._convert_message(message_type, message_data)
        for client in list(self.subscriptions[self.local_conference]):
            try:
                client.send(data)
            except:
                self.close(client)

    def send_broadcast(self, message_type, message_data):
        data = self._convert_message(message_type, message_data)
        for client in list(self.clients):
            try:
                client.send(data)
            except:
                self.close(client)


    def subscribe(self, ws, conference):
        self.local_conference = conference
        self.local = ws
        self.clients.append(ws)
        if not conference in self.subscriptions:
            self.subscriptions[conference] = []

        self.subscriptions[conference].append(ws)

    def add_sip(self, conn):
        self.sip_connections[self.local] = conn
        return conn

    def close(self, client):
        self.clients.remove(client)
        if client in self.sip_connections:
            self.sip_connections[client].close()
            del self.sip_connections[client]
        for conference in self.subscriptions:
            self.subscriptions[conference].remove(self.local)

