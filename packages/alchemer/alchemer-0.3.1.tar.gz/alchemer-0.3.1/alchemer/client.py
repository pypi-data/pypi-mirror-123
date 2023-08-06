import requests

from .classes import AlchemerObject, Survey, ContactList


class AlchemerSession(requests.Session):
    def __init__(self, api_version, api_token, api_token_secret, auth_method="api_key"):
        self.api_version = api_version
        self.base_url = f"https://api.alchemer.com/{self.api_version}"

        if api_version != "v5":
            raise NotImplementedError(
                "This library currently only works with v5+"
            )  # TODO: add < v5

        if auth_method == "api_key":
            self.auth_params = {
                "api_token": api_token,
                "api_token_secret": api_token_secret,
            }
        elif auth_method == "oauth":
            raise NotImplementedError(
                "This library currently only works with 'api_key' authentication"
            )  # TODO: add oauth

        super(AlchemerSession, self).__init__()

    def request(self, method, url, params, *args, **kwargs):
        params.update(self.auth_params)
        return super(AlchemerSession, self).request(
            method=method, url=url, params=params, *args, **kwargs
        )

    def _api_call(self, method, url, params):
        try:
            r = self.request(method, url=url, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as xc:
            raise xc

    def _api_get(self, url, params):
        return self._api_call(method="GET", url=url, params=params)

    def _api_list(self, url, params):
        all_data = []
        while True:
            response = self._api_get(url=url, params=params)
            print(response)

            data = response.get("data", [])
            if isinstance(data, dict):
                data = [data]

            total_pages = response.get("total_pages", 1)
            page = response.get("page", 1)

            all_data.extend(data)

            if "page" in params:
                break

            if page == total_pages:
                break

            params.update({"page": page + 1})

        return all_data

    @property
    def account(self):
        return AlchemerObject(session=self, name="account")

    @property
    def account_teams(self):
        return AlchemerObject(session=self, name="accountteams")

    @property
    def account_user(self):
        return AlchemerObject(session=self, name="accountuser")

    @property
    def domain(self):
        return AlchemerObject(session=self, name="domain")

    @property
    def sso(self):
        return AlchemerObject(session=self, name="sso")

    @property
    def survey(self):
        return Survey(session=self, name="survey")

    @property
    def survey_theme(self):
        return AlchemerObject(session=self, name="surveytheme")

    @property
    def contact_list(self):
        return ContactList(session=self, name="contactlist")

    @property
    def contact_custom_field(self):
        return AlchemerObject(session=self, name="contactcustomfield")
