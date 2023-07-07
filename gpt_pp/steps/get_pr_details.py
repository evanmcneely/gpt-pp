import requests

from config import GITHUB_ACCESS_TOKEN

GITHUB_AUTH_HEADERS = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
}

GITHUB_DIFF_HEADERS = {
    **GITHUB_AUTH_HEADERS,
    "Accept": "application/vnd.github.diff",
    "X-GitHub-Api-Version": "2022-11-28",
}

query = """query ($repo: String!, $owner: String!, $number: Int!) {
repository(owner: $owner, name: $repo) {
    pullRequests(number: $number) {
      edges {
        node {
            number
            body
            author {
                login
            }
            title
            body
            url
        }
      }
    }
  }
}"""


def _run_details_query(repo: str, owner: str, number: int) -> dict:
    request = requests.post(
        "https://api.github.com/graphql",
        json={
            "query": query,
            "variables": {"repo": repo, "owner": owner, "number": number},
        },
        headers=GITHUB_AUTH_HEADERS,
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, query
            )
        )


def _run_diff_query(repo: str, owner: str, number: int) -> str:
    return ""


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


def get_pr_details(repo: str, owner: str, number: int) -> tuple(str, str):
    pull_request_details = _run_details_query(repo, owner, number)
    pull_request_diff = _run_diff_query(repo, owner, number)

    return (_format_PR_details(pull_request_details), pull_request_diff)
