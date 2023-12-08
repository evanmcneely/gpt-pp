<<<<<<< HEAD
# GPT Pair Programming - WIP

Inspired and adapted from [AntonOsika/gpt/engineer](https://github.com/AntonOsika/gpt-engineer) with a focus on working with existing, large codebases. The current project looks nothing like the origional.

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
=======
# GPT Pair Programming

Inspired and adapted from [AntonOsika/gpt/engineer](https://github.com/AntonOsika/gpt-engineer) with a focus on working with existing, large codebases. The current project looks nothing like the origional so I renamed it to `gpt-pp` for "pair programming".
>>>>>>> 91a1c3e6f856ecf6320b8530a0e0da3196c64212

## Philosophy

1. Value: It has to provide value. Not just a cool toy. No fancy AI task automation just for the coolness of it. Do the basics well.
2. Extensible: Easy to add new steps, new models and new AI interactions.
3. Efficient: Consume the minimum number of tokens. Compatible with adding value - don't add more featrues and automation that increase costs.
4. Usable: Must work consistently with the most widley used (can't rely on GPT-4 to make things possible).

## Setup

This is the simplest set up with Open AI. See `config.py` for more customization.

**Install**:

- Create a virtual environment however you want. I'm newish to python so I can't provide instructions or automation.
- Run `poetry install`
- Add `OPENAI_API_KEY` keys to `.env`
- Add `GITHUB_ACCESS_TOKEN` to `.env` (only required for AI code reviews)

## AI Pair Programming

_Specify a project and file you want to work with and instructions to carry out in those files. AI model asks for clarification. Code will be written to the filesystem._

### Usage

Run `python cli_engineer.py <path to project> <path to file>`

- project path is required
- file path is optional
- `--no-imports` to skip loading imported files to context

Follow the prompts

1. Enter the relative path to the project you want to work with (only if project path is invalid)
2. Enter the relative path to the file you want to work with (only if file path is not provided or invalid)
3. Enter the instruction prompt for the model
4. Answer the questions to give the model more clarity on the instructions
5. Provide feedback and keep working

### Possibilities

- This can be a lot more robust
- Update existing files in a granular way
- Commit code to the project
- Work with multiple projects and multiple files

### Limitations

- Built on mac OS, can't garuntee all compatibility with all OS
- Doesn't work to well at the moment
- Changes permissions in the file system to access and update files.

## AI Chat

_Specify and project and file you want to work with. Have a conversational chat with the files._

### Usage

Run `python cli_chat.py <path to project> <path to file>`

- project path is required
- file path is optional
- `--no-imports` to skip loading imported files to context

Follow the prompts

1. Enter the relative path to the project you want to work with (only if project path is invalid)
2. Enter the relative path to the file you want to work with (only if file path is not provided or invalid)
3. Open ended chat - ask questions about the code, responses streamed to stdout

### Possibilities

- Initiate pair programming session from here

### Limitations

- Built on mac OS, can't garuntee all compatibility with all OS
- Changes permissions in the file system to read files.

## AI Code Review

_Provide the organisation, repository and pull request number and get an AI code review posted to Github._

### Usage

Run `python cli_pr_review.py <owner> <repo> <pull request number>`

A PR review will be posted to Github

### Possibilities

- Access files locally to understand codebase and changes better before review

### Limitations

- Can only see PR diff to generate review comments.
