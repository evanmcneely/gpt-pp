import json

import requests

from config import GITHUB_ACCESS_TOKEN

GITHUB_HEADERS = {
    "Accept: application/vnd.github+json"
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def _format_pr_url(owner: str, repo: str, number: int) -> str:
    return f"https://api.github.com/repos/repos/{owner}/{repo}/pulls/{number}/comments"


def _post_review(owner: str, repo: str, number: int, body: dict):
    response = requests.post(
        _format_pr_url(owner, repo, number),
        data=json.dumps(body),
        headers=GITHUB_HEADERS,
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            "Post failed by returning code of {}. {}".format(
                response.status_code, _format_pr_url(owner, repo, number)
            )
        )


def post_pr_review(owner: str, repo: str, number: int, request_body: dict):
    response = _post_review(owner, repo, number, request_body)
    return response
