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

Notes about reviewing a PR:
Leave comments for specific positions in the diff when you have something constructive to say. Be critical as you have high standards. Don't point out the obvious. 

The position value equals the number of lines down from the first "@@" hunk header in the file you want to add a comment. The line just below the "@@" line is position 1, the next line is position 2, and so on. The position in the diff continues to increase through lines of whitespace and additional hunks until the beginning of a new file. You cannot leave a comment on a position that is unchanged.

Keep in mind that a good PR review is thoughtful and contructive with specific and actionable feedback on the changes. Include your overall thoughts on the pull request along with whether or not the PR should be approved, blocked or commented on at the end.
    1. Approve (APRROVE) if everything looks good and you have only minor suggestions about the code. You cannot approve if the PR was authored by {user}.
    2. Request changes (REQUEST_CHANGES) if there there are errors or bugs in the code.
    3. Comment (COMMENT) if the code contains no bugs or errors but there are things that could be improved before approval. You can only comment if the PR was authored by {user}.

Format your response like this:
1. File path: path/to/file.py
Position: 4
Comment: "Contructive comment..."
2. File path: path/to/anouther/file.py
Position: 16
Comment: "Anouther contructive comment ..."
... for as many comments as needed
Overall: Overall thoughts about the changes being proposed and the PR review. Since you are acting on behalf of {user}, you should also sign this message as "AI GENERATED".
Decision: decision to approve, request changes or comment.  You can only comment if the PR was authored by {user}.

Begin!"""  # noqa

format_review_post_request = """Generate the request body to POST the pull request review notes to github. Format your response as a JSON blob.

PR details:
{pr_details}

{review_notes}

Body Parameters
- *body*: string, Required
The body text of the pull request review. Put overall thoughts here.
- *event*: string, Required
The review action you want to perform. Must be `COMMENT` if the pull request was authored by {user}. The review actions include: `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`.
- *comments*: array of objects
    - `body`: string, Required
    Text of the review comment.
    - `path`: string, Required
    The relative path to the file that necessitates a comment. This should not start with a slash.
    - position: integer
    The position in the diff where you want to add a review comment. The position value equals the number of lines down from the first "@@" hunk header in the file you want to add a comment. The line just below the "@@" line is position 1, the next line is position 2, and so on. The position in the diff continues to increase through lines of whitespace and additional hunks until the beginning of a new file.

Remember to format your response as a JSON blob. If the pull request was authored by {user}, only `"event":"COMMENT"` can be made.

Request body:"""  # noqa
