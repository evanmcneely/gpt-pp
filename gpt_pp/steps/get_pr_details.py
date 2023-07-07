import requests
from halo import Halo

from config import GITHUB_ACCESS_TOKEN

GITHUB_HEADERS = {
    "Accept: application/vnd.github+json"
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

GITHUB_DIFF_HEADERS = {
    **GITHUB_HEADERS,
    "Accept": "application/vnd.github.diff",
}


def _format_pr_url(owner: str, repo: str, number: int) -> str:
    return f"https://api.github.com/{owner}/{repo}/pulls/{number}"


def _run_details_query(owner: str, repo: str, number: int) -> dict:
    request = requests.get(
        _format_pr_url(owner, repo, number),
        headers=GITHUB_HEADERS,
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, _format_pr_url(owner, repo, number)
            )
        )


def _run_diff_query(owner: str, repo: str, number: int) -> str:
    request = requests.get(
        _format_pr_url(owner, repo, number),
        headers=GITHUB_DIFF_HEADERS,
    )
    if request.status_code == 200:
        return request.text
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, _format_pr_url(owner, repo, number)
            )
        )


def _format_PR_details(pull_request: dict) -> str:
    number = pull_request["number"]
    body = pull_request["body"]
    author_login = pull_request["author"]["login"]
    title = pull_request["title"]
    url = pull_request["url"]

    formatted_data = f"Pull Request #{number}: {title}\n"
    formatted_data += f"Author: {author_login}\n"
    formatted_data += f"URL: {url}\n"
    formatted_data += f"Body: {body}\n"

    return formatted_data


@Halo(text="Retrieveing PR details from Github", spinner="dots")
def get_pr_details(owner: str, repo: str, number: int) -> tuple(str, str):
    pull_request_details = _run_details_query(owner, repo, number)
    pull_request_diff = _run_diff_query(owner, repo, number)

    return (_format_PR_details(pull_request_details), pull_request_diff)
