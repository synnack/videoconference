"""
Websocket raw SIP handler. Allows us to defer negotiation to the client.
Uses gevent greenlet to wait for data and dispatch events.

Wrote this myself because SIP libraries do not allow me to supply SDP data from
the browser
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

from gevent import socket as gsocket
from gevent import Greenlet
from mimetools import Message
from StringIO import StringIO
import random

class SIP():
    """
    Websockets raw SIP handler.
    """
    def __init__(self, hostname, room, port=5060, method='UDP'):
        """
        Connects to a SIP server and spawns a greenlet which handles the incoming SIP events
        """
        self.method = method
        self.hostname = hostname
        self.port = port
        self.socket = gsocket.create_connection((hostname, port))
        self.greenlet = Greenlet.spawn(self.wait_for_sip_read)
        self.handlers = {}
        self.room = room
        self.contact = None
        self.from_hdr = None
        self.to_hdr = None

    def bind(self, action, fn):
        """
        Bind function as action handler
        """
        if not action in self.handlers:
            self.handlers[action] = []
        self.handlers[action].append(fn)

    def send_invite(self, sdp):
        """
        Send the SIP INVITE as client part and initial step of the SDP negotiation
        """
        self.callid = random.randint(1000,9999999999)
        invite = "INVITE sip:" + self.room + "@" + self.hostname + " SIP/2.0\r\n" + \
                 "Via: SIP/2.0/TCP " + self.hostname + ":" + str(self.port) + ";rport;branch=z9hG4bK1465117333\r\n" + \
                 "From: <sip:attendant@nikhef.nl>;tag=1281328591\r\n" + \
                 "To: <sip:" + self.room + "@" + self.hostname + ">\r\n" + \
                 "Call-ID: " + str(self.callid) + "\r\n" + \
                 "CSeq: 20 INVITE\r\n" + \
                 "Contact: <sip:attendant@nikhef.nl>\r\n" + \
                 "Content-Type: application/sdp\r\n" + \
                 "Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, NOTIFY, MESSAGE, SUBSCRIBE, INFO\r\n" + \
                 "Max-Forwards: 70\r\n" + \
                 "User-Agent: NIKHEF Video conferencing\r\n" + \
                 "Subject: Phone call\r\n" + \
                 "Content-Length: " + str(len(sdp)) + "\r\n\r\n"
        gsocket.wait_write(self.socket.fileno())
        self.socket.send(invite)
        self.socket.send(sdp)

    def send_ack(self):
        """
        Send the SIP ACK as a notification that the MCU SDP offer is accepted by the browser.
        """
        reply = "ACK " + self.contact + " SIP/2.0\r\n" + \
                "Via: SIP/2.0/TCP " + self.hostname + ":" + str(self.port) + ";rport;branch=z9hG4bK1465117333\r\n" + \
                "Max-Forwards: 70\r\n" + \
                "To: " + self.to_hdr + "\r\n" + \
                "From: " + self.from_hdr + "\r\n" + \
                "Call-ID: " + str(self.callid) + "\r\n" + \
                "CSeq: 20 ACK\r\n" + \
                "Content-Length: 0\r\n\r\n"
        gsocket.wait_write(self.socket.fileno())
        self.socket.send(reply)

    def wait_for_sip_read(self):
        """
        This function waits for events and dispatches event handlers.
        This function should run inside a greenlet.
        """
        while True:
            fileno = self.socket.fileno()
            gsocket.wait_read(fileno)
            message = self.socket.recv(8192)
            header, body = message.split("\r\n\r\n", 1)

            sip_status_line, parse_headers = header.split("\r\n", 1)
            sip_status = sip_status_line.split(" ")

            # FIXME Debug info
            print sip_status_line

            if sip_status[0] != "SIP/2.0":
                print "WARNING: Got:", sip_status_line
                print header
                print body
                continue

            headers = Message(StringIO(parse_headers))

            if sip_status[1] == '100' and headers['cseq'] == "20 INVITE":
                if 'trying' in self.handlers:
                    for fn in self.handlers['trying']:
                        fn(headers, body)

            elif sip_status[1] == '180' and headers['cseq'] == "20 INVITE":
                if 'ringing' in self.handlers:
                    for fn in self.handlers['ringing']:
                        fn(headers, body)

            elif sip_status[1] == '200' and headers['cseq'] == "20 INVITE":
                self.contact = headers['contact'][1:-1]
                self.to_hdr = headers['to']
                self.from_hdr = headers['from']

                if 'invite_ok' in self.handlers:
                    for fn in self.handlers['invite_ok']:
                        fn(headers, body)

            elif sip_status[1] == '415' and headers['cseq'] == "20 INVITE":
                if 'media-error' in self.handlers:
                    for fn in self.handlers['media-error']:
                        fn(headers, body)
            else:
                print header, body
                if 'other' in self.handlers:
                    for fn in self.handlers['other']:
                        fn(headers, body)

    def close(self):
        """
        This function sends a BYE on the SIP socket, kills the incoming event handler greenlet and closes the SIP socket
        """
        gsocket.wait_write(self.socket.fileno())
        if self.contact:
            self.socket.send("BYE " + self.contact + " SIP/2.0\r\n" + \
                             "Via: SIP/2.0/TCP " + self.hostname + ":" + str(self.port) + ";rport;branch=z9hG4bK1465117333\r\n" + \
                             "From: " + self.from_hdr + "\r\n" + \
                             "To: " + self.to_hdr + "\r\n" + \
                             "Call-ID: " + str(self.callid) + "\r\n" + \
                             "CSeq: 20 BYE\r\n" + \
                             "Contact: <sip:attendant@nikhef.nl>\r\n" + \
                             "Max-Forwards: 70\r\n" + \
                             "Content-Length: 0\r\n\r\n")
        self.greenlet.kill()
        self.socket.close()

