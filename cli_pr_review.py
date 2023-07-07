import typer
from typing_extensions import Annotated

from gpt_pp.steps import get_PR_details
from gpt_pp.ui import UI

app = typer.Typer()


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
        """
        1. Done -  command line app - require org, repo, PR #
        2. Done - gql query - retrieve PR detials (engineer, description, date, etc.)
        3. get PR diff
        4. generate review comments
        5. generate POST request
        6. post to github
        """

        details, diff = get_PR_details(org, repo, pr_number)
    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()

# review_pull_request = LLMChain(
#     llm=get_openai_llm(temperature=0.5),
#     prompt=make_PR_review_notes,
#     output_key="review_notes",
#     verbose=True,
# )

# post_PR_comments = APIPostChain.from_llm_and_api_docs(
#     get_openai_llm(),
#     GITHUB_PR_DOCS,
#     question_key="review_notes",
#     api_url_prompt=make_post_PR_review_url,
#     api_response_prompt=summarize_PR_review,
#     headers=GITHUB_HEADERS,
#     verbose=True,
# )


# review_pull_request = SequentialChain(
#     input_variables=["question"],
#     chains=[
#         get_PR_details,
#         get_PR_diff,
#         determine_technologies_used,
#         determine_codebase_search,
#         understand_the_code,
#         comment_on_best_practices,
#         review_pull_request,
#         post_PR_comments,
#     ],
#     verbose=True,
# )
