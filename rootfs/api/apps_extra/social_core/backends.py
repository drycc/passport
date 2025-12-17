import json
from os.path import join, dirname
from pathlib import Path
from social_core.backends.oauth import BaseOAuth2
from social_core.backends.github import GithubOAuth2 as BaseGithubOAuth2
from social_core.backends.google import GoogleOAuth2 as BaseGoogleOAuth2
from social_core.backends.weixin import WeixinOAuth2 as BaseWeixinOAuth2


def icon_path(name):
    return Path(join(dirname(__file__), "icons", f"{name}.svg"))


class GithubOAuth2(BaseGithubOAuth2):
    icon = icon_path("github").read_text(encoding="utf-8")


class GoogleOAuth2(BaseGoogleOAuth2):
    name = "google"
    icon = icon_path("google").read_text(encoding="utf-8")


class WeixinOAuth2(BaseWeixinOAuth2):
    icon = icon_path("weixin").read_text(encoding="utf-8")


class FeiShuOAuth2(BaseOAuth2):
    """FeiShu OAuth2 authentication backend"""
    name = 'feishu'
    icon = icon_path("feishu").read_text(encoding="utf-8")

    AUTHORIZATION_URL = 'https://accounts.feishu.cn/open-apis/authen/v1/authorize'
    ACCESS_TOKEN_URL = 'https://open.feishu.cn/open-apis/authen/v2/oauth/token'
    USER_INFO_URL = 'https://open.feishu.cn/open-apis/authen/v1/user_info'

    DEFAULT_SCOPE = ['']
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires'),
        ('union_id', 'union_id'),
        ('access_token', 'access_token'),
    ]

    def request_access_token(self, *args, **kwargs):
        """Override to send JSON request provided by FeiShu"""
        if 'data' in kwargs:
            kwargs['data']['app_id'] = self.setting('KEY')
            kwargs['data']['app_secret'] = self.setting('SECRET')
            kwargs['data'] = json.dumps(kwargs['data'])
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/json; charset=utf-8'
        return super().request_access_token(*args, **kwargs)

    def get_user_details(self, response):
        """Return user details from FeiShu account"""
        return {
            'username': response.get('name', ''),
            'email': response.get('email', ''),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = self.get_json(
            self.USER_INFO_URL,
            headers=headers
        )
        # FeiShu returns data wrapped in 'data' field
        if 'data' in response:
            response.update(response['data'])

        response['union_id'] = response.get('union_id', '')
        return response


__all__ = [GithubOAuth2, GoogleOAuth2, WeixinOAuth2, FeiShuOAuth2]
