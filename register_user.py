#!/usr/bin/env python3
"""
XMPP User Registration Client
Allows dynamic user registration through XMPP protocol
"""

import sys
from slixmpp import ClientXMPP


class RegistrationClient(ClientXMPP):
    def __init__(self, jid, password):
        # For registration, we use a temporary JID
        super().__init__(jid, password)
        self.register_success = False
        
        # Register event handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)
        
    def start(self, event):
        """Handle session start - not used for registration"""
        print("✅ Session started (this shouldn't happen during registration)")
        
    def register(self, iq):
        """Handle registration response"""
        if iq['type'] == 'result':
            print(f"✅ User {self.requested_jid} registered successfully!")
            self.register_success = True
        else:
            print(f"❌ Registration failed: {iq['error']['text']}")
        
        self.disconnect()
        
    def register_user(self, username, password, server="localhost"):
        """Register a new user"""
        self.requested_jid = f"{username}@{server}"
        
        print(f"📝 Registering user: {self.requested_jid}")
        
        # Send registration request
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = username
        resp['register']['password'] = password
        
        try:
            resp.send()
            return True
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False


def main():
    if len(sys.argv) != 3:
        print("Usage: python register_user.py <username> <password>")
        print("Example: python register_user.py newuser mypassword")
        sys.exit(1)
        
    username = sys.argv[1]
    password = sys.argv[2]
    server = "localhost"
    
    print("🔗 XMPP User Registration Tool")
    print(f"👤 Username: {username}")
    print(f"🏠 Server: {server}")
    print("-" * 40)
    
    # Create registration client (we need a temporary connection)
    temp_jid = f"temp@{server}"
    client = RegistrationClient(temp_jid, "temp")
    
    # Enable in-band registration
    client.register_plugin('xep_0077')  # In-band registration
    
    try:
        print("🔌 Connecting for registration...")
        
        # Connect without authentication for registration
        if client.connect(("127.0.0.1", 5222)):
            # Register the user
            if client.register_user(username, password, server):
                client.process(forever=False)
                
                if client.register_success:
                    print(f"🎉 User {username}@{server} is ready to use!")
                else:
                    print("❌ Registration process failed")
            else:
                print("❌ Failed to send registration request")
        else:
            print("❌ Failed to connect to server")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()