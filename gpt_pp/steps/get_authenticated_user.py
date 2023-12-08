import requests
from halo import Halo

from config import GITHUB_ACCESS_TOKEN

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_authenticated_user():
    response = requests.get(
        "https://api.github.com/user",
        headers=GITHUB_HEADERS,
    )
    if response.status_code == 200:
        return response.json().get("login")
    else:
        raise Exception(
            "Get failed by returning code of {}. {}".format(
                response.status_code, "https://api.github.com/user"
            )
        )
