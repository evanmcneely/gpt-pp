# GPT Engineer

Adapted from [AntonOsika/gpt/engineer](https://github.com/AntonOsika/gpt-engineer) with a focus on working with existing, large codebases

**Goal:**
_Specify what you want to do and the place to do it, the AI asks for clarification, then makes the changes, and waits for feedback before continuing._

## To Do

- [ ] Adapt project to use langchain, mimicing origional functionality
  - chains
  - memory
- [ ] Implement step to source files that need to be referenced
- [ ] Implement file manager, need to update, delete and create files

## Ideal steps

1. Enter what you want the AI to do with a seed file of roughly where to do it
2. Using the seed file, retrieve all the file imports
   - this can go multiple levels deep, start with just 1
3. Ask the model for any clarifications, let the user clarify (existing)
4. The model will now generate code. Write to the file system.
   - create new files
   - update existing files (to keep output minimal) only ask for the diff and update the files ?? [GitHub - google/diff-match-patch: Diff Match Patch is a high-performance library in multiple languages that manipulates plain text.](https://github.com/google/diff-match-patch)
   - delete files
   - make a commit for this iteration
   - Keep files in program memory
5. Pass back to the user for feedback
   - user provides feedback, repeat steps 2 - 4

_Someday maybe_

- Find test files for the relevant changes
- Write/update test files for the changes
- Run tests and repeat 4 - 6 until tests pass

  - limit the number of retries before prompting the user

## Usage

**Install**:

- `pip install -r requirements.txt`

**Run**:

- Add `OPENAI_API_KEY` to `.env`
- run `python main.py -f ../file/paths/`

**Results**:

- Check the files system for changes

## Limitations

TODO

## Features

Each step in steps.py will have its communication history with GPT4 stored in the logs folder, and can be rerun with scripts/rerun_edited_message_logs.py.
