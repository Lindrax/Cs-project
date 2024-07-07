import random
import django.contrib.sessions.backends.db as db

class SessionStore(db.SessionStore):
    def _get_new_session_key(self):
        while True:
            session_key = 'session-' + str(random.randint(1, 10))
            if not self.exists(session_key):
                return session_key