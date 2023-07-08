from typing import Tuple

import typer
from halo import Halo
from typing_extensions import Annotated

from gpt_pp.ai import AI
from gpt_pp.steps import get_authenticated_user, get_pr_details, post_pr_review
from gpt_pp.ui import UI

app = typer.Typer()


@Halo(text="Retrieving pull request data", spinner="dots")
def _fetch_github_data(org: str, repo: str, number: int) -> Tuple[str, str, str]:
    user = get_authenticated_user()
    details, diff = get_pr_details(org, repo, number)
    return user, details, diff


@app.command()
def setup(
    org: Annotated[
        str,
        typer.Argument(
            help="The organization that owns the project",
        ),
    ],
    repo: Annotated[
        str,
        typer.Argument(
            help="The name of the repository",
        ),
    ],
    pr_number: Annotated[
        int,
        typer.Argument(
            help="The PR number",
        ),
    ],
):
    try:
        ai = AI()

        user, details, diff = _fetch_github_data(org, repo, pr_number)

        review_notes = ai.generate_review_notes(details, diff, user)
        request_body = ai.generate_pr_post_request_body(details, user, review_notes)

        post_pr_review(org, repo, pr_number, request_body)

        UI.message("Review posted successfully!")

    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()
