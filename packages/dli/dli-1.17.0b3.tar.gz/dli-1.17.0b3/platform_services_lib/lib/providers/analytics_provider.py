import os

from injector import singleton as singleton_scope, provider
from requests import Session

from ..authentication.auth import sam_app_flow
from ..context.environments import _Environment
from ..handlers.analytics_handler import AnalyticsHandler, AnalyticsSender
from ..providers.base_provider import BaseModule


class AnalyticsDependencyProvider(BaseModule):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        config = {
            'version': 'latest',
            'app_name': 's3proxy',
            'consumption_env': os.environ.get('CONSUMPTION_API_URL'),
            'strict': False,
            'logger': None
        }

        catalogue_url = os.environ.get('CATALOGUE_API_URL')  # 'https://catalogue-qa.udpmarkit.net'
        environment = _Environment(catalogue_url)
        decoded_token = sam_app_flow(environment)
        # if DLI_ACCESS_KEY_ID and DLI_SECRET_ACCESS_KEY is
        # not valid we cannot retrieve a JWT from SAM.
        if decoded_token is not None:
            session = Session()
            session.headers.update({'Authorization': f"Bearer {decoded_token}"})
        else:
            session = None

        rest_analytics_sender = AnalyticsSender(config, session)
        self._analytics_handler = AnalyticsHandler(rest_analytics_sender)

    @singleton_scope
    @provider
    def analytics_handler(self) -> AnalyticsHandler:
        return self._analytics_handler
