# GPT Pair Programming

Inspired and adapted from [AntonOsika/gpt/engineer](https://github.com/AntonOsika/gpt-engineer) with a focus on working with existing, large codebases. The current project looks nothing like the origional so I renamed it to `gpt-pp` for "pair programming".

## Philosophy

1. Value: Create tools I would use daily because they work. I don't want this to be just a cool toy. It has to provide value. There will be no trinkets. Do the basics well.
2. Extensible: Easy to add new steps, new models and new AI interactions
3. Efficient: Consume the minimum number of tokens

## Usage

### Setup

**Install**:

- create a virtual environment however you want
- `pip install -r requirements.txt`
- Add `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` keys to `.env`
- Add any other environment variables to serve as overrides to the default configuration (see `config.py`)

### AI Pair Programming

_Specify a project and file you want to work with and intructions to carry out in those files. AI models asks for clarification. Code will be written to the filesystem._

Run `python cli_engineer.py`

- `--no-workspace` to ignore `/workspace` defaults
- `--no-imports` to skip loading imported files to context
- `--log-prefix` to save chat logs to the `logs` directory

Follow the prompts

1. Enter the relative path to the project you want to work with
   - create a `project` file in the `workspace` directory to skip this prompt
2. Enter the relative path to the file you want to work with
   - create a `file` file in the `workspace` directory to skip this prompt
3. Enter the instruction prompt for the model
   - create a `prompt` file in the `workspace` directory to skip this prompt
4. Answer the questions to give the model more clarity on the instructions
5. Provide feedback and keep working

#### Possibilities

- Commit code to a project for distinct iterations
- Start with multiple projects and files
- Use models more efficiently. Only generate the code that needs to be updated and write that to the file in the correct place
- Better logging and visibility of the models thinking

#### Limitations

- Limited testing. There are bugs.
- Error messaging could be better
- Changes permissions in the file system to access and update files (they get changed back). No way around this.

### AI Chat

_Specify and project and file you want to work with. Have a conversational chat about the files._

TODO

### AI Code Review

_Provide the organisation, repository and pull request number and get an AI code review posted to Github._

Done - just doesn't exist here yet
