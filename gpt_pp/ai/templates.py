clarify = """Respond with a single question that you would need to ask to gain more clarity about how to follow the most recent instructions or feedback. Return just the question. If everything is clear, return the string "nothing left to clarify". You have been trusted to make assumptions, not every small detail needs to be clarified.

Chat History: 
{chat_history}
"""  # noqa

generate_all_code = """Write the code that meets the instructions. 

Start by thinking about how you are going to implement the code. Document your thoughts.

Then write the code needed for each file. Please note that the code should be fully functional. No placeholders.

Be consise, only write the code that is required to implement the changes. 
"""  # noqa

diff = """Generate the universal diff that would need to be applied the file at path "{file_path}" to create the changes outlined in the chat history below.

{chat_history}
"""  # noqa

file_content = """{chat_history}
---
Given this chat conversation, generate the exact file content that should be pasted into the file at path "{file_path}". 
Return only the code block for this file. The code should be fully functional.
Ensure to implement all code, if you are unsure, write a plausible implementation.

Code for file {file_path}:
"""  # noqa


file_imports = """Determine the paths to all the files imported into the files below from the project root directory with the correct file extension. File paths should start with "./". Don't include the path to the files provided.
Return the result as a comma separated list of file paths. Don't return anything else, just the file paths. 
If there are no files imported into the file below, return the string 'nothing to import'

{file}
"""  # noqa

files_requiring_changes = """Return a list of file paths matched with the operation ("create", "patch" or "delete") that should be applied to the file to implement the instructions.

Format the response like this:
PATH, OPERATION
PATH, OPERATION
PATH, OPERATION
... as many times as needed

PATH is the path to the file from the project directory, e.g. ./path/to/file.py
OPERATION is either "create" (file needs to be created), "patch" (file content needs to be updated), or "delete" (file needs to be deleted)

Example output:
./path/to/file.py, create
./anouther/file.py, patch
./last/file.py, delete


{chat_history}
"""  # noqa


create_review_notes = """Create review comments for this pull request. You are reviewing this PR on behalf of {user}.

{pr_details}

PR diff:
{pr_diff}

--------

Notes about reviewing a PR:
Leave comments for specific positions in the diff when you have something constructive to say. Don't point out the obvious. Lean towards being mildly critical as you have high standards.

The position value equals the number of lines down from the first "@@" hunk header in the file you want to add a comment. The line just below the "@@" line is position 1, the next line is position 2, and so on. The position in the diff continues to increase through lines of whitespace and additional hunks until the beginning of a new file. You cannot leave a comment on a position that is unchanged.

Keep in mind that a good PR review is thoughtful and contructive with specific and actionable feedback on the changes. Include your overall thoughts on the pull request along with whether or not the PR should be approved, blocked or commented on at the end.
    1. Approve (APRROVE) if everything looks good and you have only minor suggestions about the code.
    2. Block (REQUEST_CHANGES) if there there are errors or bugs in the code.
    3. Comment (COMMENT) if the code contains no bugs or errors but there are things that could be improved before approval. If the PR was opened by {user}, you can only Comment, not Approve or Block

When you are done reviewing the pull request, respond with a summary of the PR details (including the owner, repo and pull request number) along with a list of the comments you wish to make. Finish with your overall thoughts

Example - Format your response like this:

1. File path: path/to/file.py
Position: 4
Comment: "Anything you want to say..."

2. File path: path/to/anouther/file.py
Position: 16
Comment: "Anything you want to say ..."

... repeat for as many comments as you wish

Overall: <leave overall thoughts like a pirate about the changes being proposed and the PR review including decision to approve, block or comment>. Since you are acting on behalf of {user}, you should also sign this message as AI generated

Begin!"""  # noqa

format_review_post_request = """Generate the request body to POST the pull request review to github. Format your response as a JSON blob.

API Docs:
**Create a Review Comment for a Pull Request**: 
Add a review comment[s] for a pull request
POST https://api.github.com/repos/OWNER/REPO/pulls/PULL_NUMBER/reviews
Path parameters:
- *owner*: string, Required
The account owner of the repository. The name is not case sensitive.
- *repo*: string, Required
The name of the repository. The name is not case sensitive.
- *pull_number*: integer, Required
The number that identifies the pull request.
Body parameters:
- *body*: string, Required
The body text of the pull request review
- *event*: string, Required
The review action you want to perform. The review actions include: APPROVE, REQUEST_CHANGES, or COMMENT. Can be one of: APPROVE, REQUEST_CHANGES, COMMENT
- *commit_id*: string
The SHA of the commit that needs a review. Not using the latest commit SHA may render your review comment outdated if a subsequent commit modifies the line you specify as the position. Defaults to the most recent commit in the pull request when you do not specify a value.
- *comments*: array of objects
    - body: string, Required
    Text of the review comment.
    - path: string, Required
    The relative path to the file that necessitates a comment. This should not start with a slash.
    - position: integer
    The position in the diff where you want to add a review comment. The position value equals the number of lines down from the first "@@" hunk header in the file you want to add a comment. The line just below the "@@" line is position 1, the next line is position 2, and so on. The position in the diff continues to increase through lines of whitespace and additional hunks until the beginning of a new file.
----
PR details:
{pr_details}

Review Notes:
{review_notes}
----

Remember to format your response as a JSON blob.

API url and data:"""  # noqa
