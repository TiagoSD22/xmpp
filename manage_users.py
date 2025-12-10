#!/usr/bin/env python3
"""
Dynamic User Management Script
Wrapper around ejabberdctl for easy user management
"""

import subprocess
import sys
import re


def run_ejabberd_command(command):
    """Run ejabberdctl command via Docker"""
    full_command = ["docker-compose", "exec", "-T", "ejabberd", "ejabberdctl"] + command
    
    try:
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            cwd="/mnt/c/Users/dante/Documents/pocs/xmpp"
        )
        
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def register_user(username, password, domain="localhost"):
    """Register a new user"""
    print(f"Registering user: {username}@{domain}")
    
    success, stdout, stderr = run_ejabberd_command(["register", username, domain, password])
    
    if success:
        print(f"User {username}@{domain} registered successfully!")
        return True
    else:
        print(f"Registration failed: {stderr}")
        return False


def unregister_user(username, domain="localhost"):
    """Remove a user"""
    print(f"Unregistering user: {username}@{domain}")
    
    success, stdout, stderr = run_ejabberd_command(["unregister", username, domain])
    
    if success:
        print(f"User {username}@{domain} removed successfully!")
        return True
    else:
        print(f"Removal failed: {stderr}")
        return False


def list_users(domain="localhost"):
    """List all registered users"""
    print(f"Users registered on {domain}:")
    
    success, stdout, stderr = run_ejabberd_command(["registered_users", domain])
    
    if success:
        users = stdout.split('\n') if stdout else []
        if users and users[0]:
            for user in users:
                if user.strip():
                    print(f"  {user}@{domain}")
            print(f"\nTotal: {len([u for u in users if u.strip()])} users")
        else:
            print("  No users registered")
        return users
    else:
        print(f"Failed to list users: {stderr}")
        return []


def change_password(username, new_password, domain="localhost"):
    """Change user password"""
    print(f"Changing password for: {username}@{domain}")
    
    success, stdout, stderr = run_ejabberd_command(["change_password", username, domain, new_password])
    
    if success:
        print(f"Password changed for {username}@{domain}")
        return True
    else:
        print(f"Password change failed: {stderr}")
        return False


def user_exists(username, domain="localhost"):
    """Check if user exists"""
    users = list_users(domain)
    return username in [u.strip() for u in users if u.strip()]


def bulk_register_users(user_list):
    """Register multiple users from a list"""
    print(f"Bulk registering {len(user_list)} users...")
    
    success_count = 0
    for username, password in user_list:
        if register_user(username, password):
            success_count += 1
            
    print(f"\nSuccessfully registered {success_count}/{len(user_list)} users")


def main():
    if len(sys.argv) < 2:
        print("XMPP User Management Tool")
        print("\nUsage:")
        print("  python manage_users.py register <username> <password>")
        print("  python manage_users.py unregister <username>")
        print("  python manage_users.py list")
        print("  python manage_users.py password <username> <new_password>")
        print("  python manage_users.py bulk")
        print("\nExamples:")
        print("  python manage_users.py register alice secret123")
        print("  python manage_users.py list")
        print("  python manage_users.py unregister alice")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "register":
        if len(sys.argv) != 4:
            print("Usage: python manage_users.py register <username> <password>")
            sys.exit(1)
        register_user(sys.argv[2], sys.argv[3])
        
    elif command == "unregister":
        if len(sys.argv) != 3:
            print("Usage: python manage_users.py unregister <username>")
            sys.exit(1)
        unregister_user(sys.argv[2])
        
    elif command == "list":
        list_users()
        
    elif command == "password":
        if len(sys.argv) != 4:
            print("Usage: python manage_users.py password <username> <new_password>")
            sys.exit(1)
        change_password(sys.argv[2], sys.argv[3])
        
    elif command == "bulk":
        users_to_create = [
            ("alice", "password123"),
            ("bob", "secret456"),
            ("charlie", "test789"),
        ]
        bulk_register_users(users_to_create)
        
    else:
        print(f"Unknown command: {command}")
        main()


if __name__ == "__main__":
    main()