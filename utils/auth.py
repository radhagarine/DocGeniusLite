import streamlit as st
import bcrypt
import json
import os
from datetime import datetime, timedelta

# File to store user data
USER_DB_FILE = "utils/users.json"

def init_user_db():
    """Initialize the user database if it doesn't exist"""
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def load_users():
    """Load users from the JSON file"""
    init_user_db()
    with open(USER_DB_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to the JSON file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(email, password, name):
    """Register a new user"""
    users = load_users()
    
    if email in users:
        return False, "Email already registered"
    
    users[email] = {
        "password": hash_password(password),
        "name": name,
        "created_at": datetime.now().isoformat(),
        "subscription": "free",
        "total_docs": 0,
        "free_docs_used": 0
    }
    
    save_users(users)
    return True, "Registration successful"

def login_user(email, password):
    """Login a user"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    if not verify_password(password, users[email]["password"]):
        return False, "Invalid password"
    
    # Set session state
    st.session_state["authenticated"] = True
    st.session_state["email"] = email
    st.session_state["name"] = users[email]["name"]
    st.session_state["subscription"] = users[email]["subscription"]
    st.session_state["total_docs"] = users[email]["total_docs"]
    st.session_state["free_docs_used"] = users[email]["free_docs_used"]
    
    return True, "Login successful"

def logout():
    """Logout the current user"""
    for key in ["authenticated", "email", "name", "subscription", "total_docs", "free_docs_used"]:
        if key in st.session_state:
            del st.session_state[key]

def check_authentication():
    """Check if a user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_user_stats():
    """Get current user's statistics"""
    if not check_authentication():
        return None
    
    users = load_users()
    email = st.session_state["email"]
    
    if email not in users:
        return None
    
    return {
        "total_docs": users[email]["total_docs"],
        "free_docs_used": users[email]["free_docs_used"],
        "subscription": users[email]["subscription"]
    }

def update_user_stats(email, stats):
    """Update user statistics"""
    users = load_users()
    if email in users:
        users[email].update(stats)
        save_users(users)
        
        # Update session state
        for key, value in stats.items():
            if key in ["total_docs", "free_docs_used", "subscription"]:
                st.session_state[key] = value 