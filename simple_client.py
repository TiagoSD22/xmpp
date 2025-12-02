#!/usr/bin/env python3
"""
Minimal XMPP client using threading instead of async
"""

import time
import threading
import sys
from slixmpp import ClientXMPP


class MinimalXMPPClient(ClientXMPP):
    def __init__(self, jid, password, recipient):
        super().__init__(jid, password)
        self.recipient = recipient
        self.connected_event = threading.Event()
        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message_received)
        
    def start(self, event):
        """Handle session start"""
        print(f"Connected as {self.jid}")
        
        self.send_presence()
        self.get_roster()
        
        message = f"Hello from Python XMPP client! Test at {time.strftime('%H:%M:%S')}"
        print(f"Sending: {message}")
        
        self.send_message(
            mto=self.recipient,
            mbody=message,
            mtype='chat'
        )
        
        time.sleep(3)
        print("Disconnecting...")
        self.disconnect()
        
    def message_received(self, msg):
        """Handle incoming messages"""
        if msg['type'] in ('chat', 'normal'):
            print(f"Received from {msg['from']}: {msg['body']}")


def main():
    if len(sys.argv) >= 4:
        sender_jid = sys.argv[1]
        sender_password = sys.argv[2] 
        recipient_jid = sys.argv[3]
    else:
        sender_jid = "user1@localhost"
        sender_password = "password123"
        recipient_jid = "user2@localhost"
    
    print("Starting minimal XMPP client...")
    print(f"From: {sender_jid}")
    print(f"To: {recipient_jid}")
    print("-" * 40)
    
    # Create client
    client = MinimalXMPPClient(sender_jid, sender_password, recipient_jid)
    
    # Connect and run
    try:
        print("Connecting...")
        client.connect()
        client.process(forever=False)
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()