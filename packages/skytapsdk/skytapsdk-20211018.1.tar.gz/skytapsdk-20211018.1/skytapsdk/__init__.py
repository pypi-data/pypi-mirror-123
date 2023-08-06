"""
Python SDK for accessing Skytap APIs
"""
import typing
import requests
import logging
import time
import json

# Disable excessive DEBUG messages.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

__all__ = ["SkytapAPI"]

RETRY_TIMEOUT = 10
RETRIES = 6
RETRY_STATUS_CODES = [
    "423",
    "429",
]
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30
BASE_URL = "https://cloud.skytap.com"
RUNSTATES = ["running", "stopped", "halted", "suspended"]
RUNSTATE_CURRENT_TO_PROPOSED_TRUTH_TABLE = {
    "running": {
        "running": False,
        "reset": True,
        "stopped": True,
        "halted": True,
        "suspended": True,
    },
    "stopped": {
        "running": True,
        "reset": False,
        "stopped": False,
        "halted": False,
        "suspended": False,
    },
    "suspended": {
        "running": True,
        "reset": False,
        "stopped": False,
        "halted": True,
        "suspended": False,
    },
}


def _call_api(
    request_method: str = "GET",
    url: str = BASE_URL,
    path: str = None,
    params: typing.Dict = None,
    data=None,
    files=None,
    credentials: typing.Dict = None,
    response_type="json",
    api_version: int = 1,
    retry_count: int = RETRIES,
):
    """
    Query URL for JSON response.
    :param request_method: REST action 'GET', 'POST', 'PUT', 'DELETE'
    :param url: FQDN of URL
    :param path: Path after TLD of URL
    :param params: Dictionary of query values (after "?" of URL)
    :param data: Data file
    :param files: Files?
    :param credentials: {'username': 'blah', 'token': 'blah'}
    :param response_type: 'json', 'content', 'text', or 'response'
    :param api_version: Either 1 or 2
    :param retry_count: Number of times to try if server is busy.
    :return: JSON response
    """
    url = f"{url}/{path}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_version == 2:
        headers.update({"Accept": "application/vnd.skytap.api.v2+json"})
    if "username" in credentials and "token" in credentials:
        auth = (credentials["username"], credentials["token"])
    else:
        raise "No username or token key in credentials dict."

    if data:
        data = json.dumps(data)

    try:
        response = requests.request(
            method=request_method,
            url=url,
            auth=auth,
            headers=headers,
            params=params,
            data=data,
            files=files,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
        )
        if response.status_code not in [requests.codes.ok]:
            response.raise_for_status()
        if response.status_code in RETRY_STATUS_CODES:
            if retry_count > 0:
                logging.warning(
                    f"HTTP status code: {response.status_code}.  Waiting {RETRY_TIMEOUT}s to try again."
                )
                time.sleep(RETRY_TIMEOUT)
                retry_count -= 1
                _call_api(
                    request_method=request_method,
                    url=url,
                    path=path,
                    params=params,
                    data=data,
                    files=files,
                    credentials=credentials,
                    response_type=response_type,
                    api_version=api_version,
                    retry_count=retry_count,
                )
            else:
                raise f"Max tries hit.  Abort."
        if response_type == "json":
            return response.json()
        elif response_type == "content":
            return response.content
        elif response_type == "text":
            return response.text
        elif response_type == "response":
            return response
    except requests.Timeout:
        raise f"Connection to {url} timed out."
    except requests.ConnectionError:
        raise f"Connection to {url} failed:  DNS failure, refused connection or some other connection related issue."
    except requests.TooManyRedirects:
        raise f"Request to {url} exceeds the maximum number of predefined redirections."
    except Exception as e:
        raise f"A requests exception has occurred that we have not yet detailed an 'except' clause for.  Error: {e}"


class SkytapAPI:
    """
    Interacts with the Skytap RESTful API.
    """

    def __init__(self, username: str, token: str):
        """
        Initialize a "SkytapAPI" object with username and token.
        :param username: Skytap username
        :param token: Skytap token
        """
        self.credentials = {"username": username, "token": token}

    # ################################# ENVIRONMENTS METHODS ######################################################## #
    def get_environment(self, environment_id: int = None, **kwargs):
        """
        Get a list of environments or pass environment_id of a specific one.
        :param environment_id: ID of an environment
        :param kwargs: Optional variables to be passed as query_vars (after ? in URL)
        :return: JSON
        """
        path = "configurations"
        if environment_id:
            path = f"{path}/{environment_id}.json"
        return _call_api(
            path=path,
            params=kwargs,
            credentials=self.credentials,
            api_version=2,
        )

    def post_environment(self, template_id: int, **kwargs):  # TODO: Test this.
        """
        Create an Environment
        :param template_id: ID of source template
        :param kwargs: Optional variables to be passed as query_vars (after ? in URL)
        :return:
        """
        json_data = {
            "template_id": template_id,
        }
        if "project_id" in kwargs:
            json_data["project_id"] = kwargs["project_id"]
        if "name" in kwargs:
            json_data["name"] = kwargs["name"]
        return _call_api(
            path=f"configurations.json",  # FIXME
            params=json_data,
            credentials=self.credentials,
            api_version=2,
            request_method="POST",
        )

    def put_environment(self, environment_id: int, **kwargs):  # TODO: Test this.
        """
        Update existing Environment.  Send all "kwargs" values as query_vars.
        :param environment_id: ID of environment to update.
        :param kwargs: Options to update
        :return: JSON
        """
        return _call_api(
            path=f"configurations/{environment_id}",
            params=kwargs,
            credentials=self.credentials,
            api_version=2,
            request_method="PUT",
        )

    def put_environment_owner(
        self, environment_id: int, owner_id: int, project_id: int = None
    ):  # TODO: Test this.
        """
        Change owner of this Environment.  project_id is mandatory if owner_id is a restricted account.
        :param environment_id: ID of environment ot update.
        :param owner_id: ID of user to set as owner.
        :param project_id: ID of project to set owner_id as owner.
        :return: JSON
        """
        path = f"configurations/{environment_id}.json"

        json_data = {"owner_id": owner_id}
        if project_id:
            json_data["project_id"] = project_id

        return _call_api(
            request_method="PUT",
            path=path,
            params=json_data,
            credentials=self.credentials,
            api_version=2,
        )

    def put_environment_runstate(self, environment_id: int, runstate: str):
        path = f"configurations/{environment_id}.json"

        json_data = {"runstate": runstate}
        environment = self.get_environment(environment_id=environment_id)
        if type(environment) is dict:
            current_runstate = environment["runstate"]
        else:
            raise f"Current environment state is not known.  Cannot change its runstate."
        if RUNSTATE_CURRENT_TO_PROPOSED_TRUTH_TABLE[current_runstate][runstate]:
            result = _call_api(
                request_method="PUT",
                path=path,
                params=json_data,
                credentials=self.credentials,
                api_version=2,
            )
        else:
            result = {
                "error": f"Current runstate {current_runstate} to requested runstate {runstate} not permitted."
            }

        return result

    # ################################# USERS METHODS ######################################################## #
    def get_users(self, user_id: int = None):
        """
        GET action on 'users' API for a specific user ID
        :param user_id:
        :return: JSOn
        """
        path = "users"
        if user_id:
            path = f"{path}/{user_id}"
        return _call_api(
            path=path,
            params={},
            credentials=self.credentials,
        )
