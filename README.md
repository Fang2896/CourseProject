# Multimedia Interface Course Project

## Introduction

This bot brings the power of ChatGPT to your Discord server! Engage in real-time conversations with ChatGPT and get instant grammar corrections after each chat session. Developed using `discord.py` to leverage the existing Discord UI, it reduces the need for a separate UI development, streamlining the user experience. The main backend logic integrates OpenAI's API and is built upon the LangChain framework.


## Key Features

1. **Real-time Chatting** : Users can engage in real-time text conversations with ChatGPT.
2. **Grammar Correction** : After the chat session concludes, the app will automatically detect and correct any grammatical errors made by the user, providing suggested revisions.


## Setup and Usage

1. **Invite the Bot** : Use the provided link to invite the Chat-Correction bot to your Discord server.
2. **Start a Chat** : Simply mention the bot (e.g., `@ChatCorrectionBot`) followed by your message to initiate a conversation.
3. **End Chat & View Corrections** : Once you want to conclude the conversation, type `@ChatCorrectionBot end`. The bot will then provide a list of suggested corrections for any grammatical errors detected during the conversation.

## Technical Details

* **Framework** : The bot is built on the LangChain framework, ensuring robust language processing capabilities.
* **Integration** : OpenAI's API powers the core chat and correction functionalities, providing accurate and reliable responses.
* **Development** : The bot was developed using `discord.py`, allowing it to function seamlessly within the Discord environment.

## Notes

* The app requires an internet connection to communicate with the ChatGPT servers.
* The correction feature may not catch all grammatical errors; users should use their discretion when deciding to accept suggestions.
