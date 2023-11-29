
# Discord Grammar Correction Bot

## Overview

This project is a Discord bot that enables users to join a Discord group and interact with a bot powered by GPT (Generative Pretrained Transformer). Users can chat freely with the bot, and after the conversation, they can use specific commands to check for grammatical and spelling errors in their messages. This bot is a tool for users looking to improve their language skills or just have fun chatting with an AI.

## Features

- **Join the Discord Group**: Users can join the Discord group through the link: [Join Discord](https://discord.gg/JJ8Yysgg).
- **Chat with the Bot**: Once in the group, users can freely chat with the bot.
- **Grammar and Spelling Check**: By typing `#correct`, the bot will check for grammatical and spelling errors in the user's messages.
- **Reset Chat History**: Users can clear all chat history by typing `#reset`.

## Installation and Usage

### Prerequisites

- Python 3.8
- Libraries: `openai`, `discord`, `json`, `dotenv`, `aiohttp`

### Setup

1. Clone the repository to your local machine.
2. Install the required libraries:
   ```bash
   pip install openai discord json dotenv aiohttp
   ```
3. Create a `.env` file in the main directory and fill in the following keys:
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `DISCORD_BOT_TOKEN`: Your Discord bot token.
4. Run the bot:
   ```bash
   python main.py
   ```

## Development TODOs

1. [ ] Experiment with improved prompts for better interaction.

* [ ] Develop a more advanced interaction/correction system.
* [ ] Implement voice interaction capabilities.

* [ ] Explore the use of GPT in JSON mode.

## Contribution

Contributions to the project are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License

[MIT License](LICENSE)

---

请根据您项目的具体情况调整此 `README.md` 文件。例如，您可能需要提供更详细的安装指南、使用说明、贡献指南，或者任何其他相关信息。此外，确保更新任何特定的链接或细节以匹配您的项目的实际情况。
