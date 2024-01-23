# Grammar Correct Bot for Discord

## Overview

Grammar Correct Bot is an Discord bot designed to assist in English learning. It's built on GPT and offers interactive, engaging ways to improve language skills.

## Features

### Modes

* **Free Mode**: Engage in casual conversations. The bot acts as a friend, initiating various topics for a natural chat experience.
* **Image Mode**: Describe an image. The bot provides a random image and guides the user through the process of describing it in detail.
* **Scene Mode**: Role-play with preset scenarios. The bot generates character and scene settings, allowing for immersive role-playing sessions.

### Special Commands

* **`#mode [Free/Image/Scene]`**: Switch between the three modes.
* **`#correct`**: Summarizes the user's conversation and provides grammar and vocabulary corrections.
* **`#reset`**: Clears the current conversation history.
* **`#setRole`**: In Free or Scene modes, allows users to set the bot's role.

## Installation and Setup

1. **Prerequisites**:

   * A Discord bot in your server.
   * An OpenAI key.
   * Your Discord channel ID.
   * The bot's token.

2. **Environment Setup**:

   * Create a `.env` file in the project directory.

   * Add the following content:

     ```
     makefileCopy codeOPENAI_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxx"
     DISCORD_TOKEN = "MTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
     GROUP_ID = "11xxxxxxxxxxxxxxxxxxx"
     ```

3. **Required Libraries**:

   * Install the necessary libraries in a virtual environment using 

     ```
     conda
     ```

      or 

     ```
     pip
     ```

     :

     * `discord`
     * `openai`
     * `aiofiles`
     * `aiohttp`
     * `python-dotenv`

4. **Running the Bot**:

   * Execute the bot using the command:

     ```
     python src/main.py
     ```

   * The bot will go online in the specified Discord channel and is ready for interaction.

## Project Structure

* **`gpt_client.py`**: Manages interactions with the OpenAI API.
* **`dialogue_history.py`**: Manages conversation history and bot prompt settings during mode switches.
* `discord_bot.py`: The main functional file, defining all bot `functionalities`.
* **`prompt_config_manager.py`**: Manages the `prompt_config.json` file for easy prompt management.
* **`token_config_manager.py`**: Manages the `.env` file containing keys, tokens, and IDs.
* **`history` folder**: Stores conversation history files.
* **`image` folder**: Stores images sent by the bot.
