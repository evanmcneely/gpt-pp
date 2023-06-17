# GPT Engineer - WIP

Inspired and adapted from [AntonOsika/gpt/engineer](https://github.com/AntonOsika/gpt-engineer) with a focus on working with existing, large codebases. The current project looks nothing like the origional

**Goal:**
_Specify what you want to do and the place to do it, the AI asks for clarification, then makes the changes, and waits for feedback before continuing._

## Usage

**Install**:

- `pip install -r requirements.txt`

**Run**:

- Add `OPENAI_API_KEY` to `.env`
- Add any other environment variables to serve as overrides to the default configuration (see `config.py`)
- run `python cli_engineer.py` and follow the prompts
  - `--i` to ignore `/workspace` defaults
  - `--r` to add a prefix to the `/logs` directory for keeping multiple logs
- view logs in the `/logs` directory

## Custmomization

Add your own customized instructions in a `/preferences` directory. Add files by programming language name (ex: `javascript`, `python`, etc.) that will be used by the model to followyour best practices in the language. Create a file named `engineering` for general engineering best practices.

To avoid entering the same instructions multiple times, create a `/workspace` directory with files `prompt`, `project` and `files` that the program will use by default to get things going.

## Philosophy

1. This is just a cool toy untill it provides 10x value for what I put in (I don't think it's there yet)
   - **in time**: get 10x work done for the time I need to write instructions and review code
   - **in money**: get 10x value back for all the tokens it consumes (I'm hoping competition wil drive costs/token down)
2. Extensible: easy to add new steps
3. Simple: easy to set up and use

## Ideal steps

1. Enter a project directory and file that you want to work with
2. Using the seed file, retrieve all the relevant files from the file imports
   - this can go multiple levels deep, start with just 1
3. Give instructions on what you want the model to accomplish
4. Model asks for clarifications - let the user clarify instructions. Repeat as many times as needed.
5. The model will now generate code and write to the file system.
   - create new files
   - delete files
   - update files
6. Manage conversation memory - summarize the conversation and save thoughts about the users engineering practices for future reference
7. Pass back to the user for feedback
   - user provides feedback, repeat steps 4 - 7

### Possibilites

- Tests
  - Find test files for the relevant changes
  - Write/update test files for the changes
  - Run tests and repeat until tests pass ?? limit the number of tries
- Open new branches and commit code in project

## Limitations

TODO

## To Do

- [ ] initialization and validation of the project and file paths
- [ ] Retrieve relevant files from the file system
- [ ] Clarification step
- [ ] Coding step
- [ ] Add memory management
