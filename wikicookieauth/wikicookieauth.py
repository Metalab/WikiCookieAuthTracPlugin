"""
WikiCookieAuth: a plugin for Trac to share cookies with MediaWiki
http://trac.edgewall.org
"""

import os

from trac.core import *
from trac.web.api import IAuthenticator
from trac.env import IEnvironmentSetupParticipant

PHP_SESSION_PATH = '/var/lib/php5/'
SESSION_COOKIE = 'metalabwiki_session'
TOKEN_COOKIE = 'metalabwikiToken'


class WikiCookieAuth(Component):
    implements(IAuthenticator, IEnvironmentSetupParticipant)

    def authenticate(self, req):
        if req.remote_user:
            return req.remote_user

        if 'wiki_cookie_auth' in req.environ:
            return req.environ['wiki_cookie_auth']
        else:
            wiki_session = req.incookie.get(SESSION_COOKIE)
            wiki_token = req.incookie.get(TOKEN_COOKIE)
            req.environ['wiki_cookie_auth'] = None
            if wiki_session and wiki_token:
                agent = self.wiki_auth(wiki_session.value, wiki_token.value)
                if agent and agent != 'anonymous':
                    agent = agent.lower()
                    req.authname = agent
                    req.environ['wiki_cookie_auth'] = agent
                    return agent

        return None


    def environment_created(self):
        """Called when a new Trac environment is created."""


    def environment_needs_upgrade(self, db):
        """Called when Trac checks whether the environment needs to be upgraded.
        
        Should return `True` if this participant needs an upgrade to be
        performed, `False` otherwise.
        """
        return False
        

    def upgrade_environment(self, db):
        """Actually perform an environment upgrade.
        
        Implementations of this method should not commit any database
        transactions. This is done implicitly after all participants have
        performed the upgrades they need without an error being raised.
        """


    def wiki_auth(self, session, token):
        """Lookup MediaWiki's session file and compare tokens.
        Returns the wiki username (or None if unsuccessful."""

        try:
            session_file = os.path.join(PHP_SESSION_PATH, 'sess_%s' % session)
            with open(session_file, 'r') as fp:
                session_data = fp.read().strip(';')
        except IOError:
            # no such session exists
            return None

        items = dict(item.split('|') for item in session_data.split(';'))
        session_token = items.get('wsToken').split(':')[-1].strip('"')
        session_user = items.get('wsUserName').split(':')[-1].strip('"')

        if session_token == token:
            return session_user

        return None
