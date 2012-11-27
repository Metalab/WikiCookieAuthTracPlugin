"""
WikiCookieAuth: a plugin for Trac to share cookies with MediaWiki
http://trac.edgewall.org
"""

import os

from trac.config import ListOption
from trac.core import *
from trac.web import auth
from trac.web.api import IAuthenticator
from trac.web.main import RequestDispatcher
from trac.env import open_environment
from trac.env import IEnvironmentSetupParticipant

class GenericObject(object):
    def __init__(self, **kw):
        for key, item in kw.items():
            setattr(self, key, item)


class WikiCookieAuth(Component):

    ### class-level data
    implements(IAuthenticator, IEnvironmentSetupParticipant)

    ### method for IAuthenticator

    def authenticate(self, req):

        if req.remote_user:
            return req.remote_user

        if 'wiki_cookie_auth' in req.environ:
            return req.environ['wiki_cookie_auth']
        else:
            req.environ['wiki_cookie_auth'] = None
            if req.incookie.has_key('trac_auth'):
                for project, dispatcher in self.dispatchers().items():
                    agent = dispatcher.authenticate(req)
                    if agent != 'anonymous':
                        req.authname = agent
                        req.environ['wiki_cookie_auth'] = agent
                        return agent

        return None

    ### methods for IEnvironmentSetupParticipant

    """Extension point interface for components that need to participate in the
    creation and upgrading of Trac environments, for example to create
    additional database tables."""

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

    ### internal methods

    def dispatchers(self):
        if not hasattr(self, '_dispatchers'):

            dispatchers = {}
            base_path, project = os.path.split(self.env.path)
            projects = [ i for i in os.listdir(base_path)
                         if i != project ]

            for project in projects:
                path = os.path.join(base_path, project)
                try:
                    env = open_environment(path)
                    rd = RequestDispatcher(env)
                except:
                    continue
                dispatchers[project] = rd

            self._dispatchers = dispatchers
        return self._dispatchers
