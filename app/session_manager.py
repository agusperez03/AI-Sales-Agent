from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import threading

class SessionManager:
    """Manages conversation sessions for multiple users (phone numbers)."""
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.sessions: Dict[str, List[Tuple[str, str]]] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self.lock = threading.Lock()
    
    def get_session(self, phone_number: str) -> List[Tuple[str, str]]:
        """Get the conversation history for a phone number."""
        with self.lock:
            self._cleanup_expired_session(phone_number)
            return self.sessions.get(phone_number, [])
    
    def update_session(self, phone_number: str, messages: List[Tuple[str, str]]):
        """Update the conversation history for a phone number."""
        with self.lock:
            self.sessions[phone_number] = messages
            self.last_activity[phone_number] = datetime.now()
    
    def add_message(self, phone_number: str, role: str, content: str):
        """Add a single message to the session."""
        with self.lock:
            if phone_number not in self.sessions:
                self.sessions[phone_number] = []
            self.sessions[phone_number].append((role, content))
            self.last_activity[phone_number] = datetime.now()
    
    def clear_session(self, phone_number: str):
        """Clear the session for a phone number."""
        with self.lock:
            if phone_number in self.sessions:
                del self.sessions[phone_number]
            if phone_number in self.last_activity:
                del self.last_activity[phone_number]
    
    def _cleanup_expired_session(self, phone_number: str):
        """Remove session if it has expired."""
        if phone_number in self.last_activity:
            if datetime.now() - self.last_activity[phone_number] > self.session_timeout:
                self.clear_session(phone_number)
    
    def cleanup_all_expired(self):
        """Clean up all expired sessions."""
        with self.lock:
            expired = [
                phone for phone, last_time in self.last_activity.items()
                if datetime.now() - last_time > self.session_timeout
            ]
            for phone in expired:
                self.clear_session(phone)

# Global session manager instance
session_manager = SessionManager(session_timeout_minutes=30)
