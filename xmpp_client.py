#!/usr/bin/env python3
"""
Simple XMPP client for testing ejabberd server
Connects to the server and sends a test message
"""

import asyncio
import logging
import sys
import os
from slixmpp import ClientXMPP


class SimpleXMPPClient(ClientXMPP):
    def __init__(self, jid, password, recipient):
        super().__init__(jid, password)
        self.recipient = recipient
        self.connected = False
        
        # Disable SSL/TLS for simple testing
        self.disable_starttls = True
        self.use_tls = False
        
        # Register event handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message_received)

    async def start(self, event):
        """Handle session start"""
        print(f"✓ Connected as {self.jid}")
        self.connected = True
        
        # Send initial presence
        self.send_presence()
        await self.get_roster()
        
        # Send a test message
        await self.send_test_message()

    def message_received(self, msg):
        """Handle incoming messages"""
        if msg['type'] in ('chat', 'normal'):
            print(f"📩 Received message from {msg['from']}: {msg['body']}")

    async def send_test_message(self):
        """Send a simple test message"""
        message = "Hello from Python XMPP client! 🚀"
        print(f"📤 Sending message to {self.recipient}: {message}")
        
        self.send_message(
            mto=self.recipient,
            mbody=message,
            mtype='chat'
        )
        
        # Keep connection open for a moment to receive any replies
        await asyncio.sleep(2)
        self.disconnect()


def main():
    """Main function to run the XMPP client"""
    # Configuration
    SERVER_HOST = "127.0.0.1"  # Use IP instead of hostname
    SERVER_PORT = 5222
    
    # Get credentials from command line arguments or use defaults
    if len(sys.argv) >= 4:
        # Command line: python xmpp_client.py <sender_jid> <password> <recipient_jid>
        SENDER_JID = sys.argv[1]
        SENDER_PASSWORD = sys.argv[2]
        RECIPIENT_JID = sys.argv[3]
    else:
        # Use environment variables or defaults
        SENDER_JID = os.getenv("XMPP_SENDER_JID", "testuser@localhost")
        SENDER_PASSWORD = os.getenv("XMPP_SENDER_PASSWORD", "password123")
        RECIPIENT_JID = os.getenv("XMPP_RECIPIENT_JID", "admin@localhost")
    
    print("🔗 Starting XMPP client...")
    print(f"📍 Server: {SERVER_HOST}:{SERVER_PORT}")
    print(f"👤 User: {SENDER_JID}")
    print(f"🎯 Recipient: {RECIPIENT_JID}")
    print("-" * 50)
    
    # Create and configure the XMPP client
    client = SimpleXMPPClient(SENDER_JID, SENDER_PASSWORD, RECIPIENT_JID)
    
    # Connect to server
    try:
        # Connect to the XMPP server
        print("🔌 Connecting to server...")
        
        # Connect and process
        print("⏳ Attempting connection...")
        if client.connect((SERVER_HOST, SERVER_PORT)):
            print("✅ Connected successfully!")
            client.process(forever=False)
        else:
            print("❌ Failed to connect to server")
            print("Make sure the ejabberd server is running and the user is registered")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the ejabberd server is running and accessible")


def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python xmpp_client.py [sender_jid] [password] [recipient_jid]")
    print("")
    print("Examples:")
    print("  python xmpp_client.py                                    # Use defaults")
    print("  python xmpp_client.py user1@localhost pass123 admin@localhost")
    print("")
    print("Environment variables (alternative to command line):")
    print("  XMPP_SENDER_JID=user1@localhost")
    print("  XMPP_SENDER_PASSWORD=pass123")
    print("  XMPP_RECIPIENT_JID=admin@localhost")


if __name__ == "__main__":
    # Show usage if requested
    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0)
    
    # Set up logging (optional, for debugging)
    logging.basicConfig(level=logging.WARNING)
    
    # Run the client
    main()