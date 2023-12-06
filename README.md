# Ascension Tactics Discord Bot

This Discord bot enables users to conduct an Ascension Tactics draft game. It randomly selects champions for a draft pool and allows each player to pick champions in turns until each player has selected three champions. 

## How to Use

1. **Setup**
   - Make sure you have Python installed.
   - Install the required `discord.py` library. You can install it using `pip`:

     ```
     pip install discord.py
     ```

2. **Running the Bot**
   - Clone the repository to your local machine:

     ```
     git clone git@github.com:Shafquat/ascension-discord-bot.git
     ```

   - Replace `'YOUR_TOKEN'` in the Python file (`ascension_bot.py`) with your actual bot token obtained from the Discord Developer Portal.

   - Run the bot:

     ```
     python ascension_bot.py
     ```

3. **Commands**
   - Use the command `!startdraft` to begin the draft process.
   - Follow the bot's instructions to select champions during the draft.

## Functionality

- Upon using the `!startdraft` command, the bot initiates a draft, randomly selects six champions, and prompts users to specify the number of participating players (between 2 and 4).
- Each player in the draft selects one champion per turn until each player has selected three champions.
- The draft pool is updated after each selection, ensuring six champions are always available for drafting.

## Bot Implementation Details

- The bot is implemented in Python using the `discord.py` library.
- It utilizes Discord's `on_message` event to listen for commands and user inputs.
- The bot uses Discord's `Intents` to manage message content and functionality.

## Acknowledgments

- This bot is created based on the Ascension Tactics card game.
- Credits to the original game developers for the concept of the draft and champion selection mechanism.

## Disclaimer

This bot is created for educational and entertainment purposes and is not affiliated with Ascension Tactics or its developers.
