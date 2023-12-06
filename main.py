import discord
import os
import random

champions_list = [
    'Arha Templar', 'Arha Sensei', 'Water Djinn', 'Psyche Askara',
    'Unbound Emissary', 'Raven Siren', 'Twilight Scout', 'Icarus Steelfoot',
    'Rūt', 'Tyranyx', 'P.R.I.M.E.', 'Hedron Smithy', 'Mechana Initiate',
    'Reactor Monk', 'Bringer of Despair', 'Shadowcaster', 'Demon Slayer',
    'Naka Blackblade', 'Nihilbomber', 'Emri', 'Spike Vixen', 'Tuskrider',
    'Runic Lycanthrope', 'Flytrap Witch'
]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'Logged in as {client.user.name}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower() == '!startdraft':
    await message.channel.send(
        "Hello! Let's start an Ascension Tactics draft. Out of the 24 champions avilable, 6 random champions will be added to a draft eligible pool. Each turn, a player will select a champion to draft. A new champion from the remaining available champions will be added to the draft eligible pool so that there is always 6 champsions in the draft eligible pool. The draft will end once each player has selected 3 champions. How many players will be participating in this draft?"
    )

    def check(m):
      return m.author == message.author and m.channel == message.channel

    msg = await client.wait_for('message', check=check)

    player_count = int(msg.content)
    if player_count < 2 or player_count > 4:
      await message.channel.send("Please choose a number between 2 - 4.")
    else:
      # Create the draft eligible pool from 6 random champions
      draft_eligible = random.sample(champions_list, 6)
      # remove draft eligible champions from the champions list
      remaining_champs = [x for x in champions_list if x not in draft_eligible]

      # create a list for every player
      player_lists = {}  # Dictionary to store lists for each player

      # Create an empty list for each player
      for i in range(player_count):
        player_lists[f"player_{i+1}"] = []

      await message.channel.send(
          f"Let's play a {player_count} player game! \nHere are the champions that are available: {draft_eligible } \nPlayer1 please pick a champion 1-6 to draft"
      )

      # loop over every player and let them pick a card and repopulate the draft pool each turn
      turn_count = 1
      while turn_count <= 3:
        for i in range(player_count):
          msg = await client.wait_for('message', check=check)
          # add card into player list
          player_lists[f"player_{i+1}"].append(
              draft_eligible[int(msg.content) - 1])

          # remove card from draft eligible pool
          draft_eligible.remove(draft_eligible[int(msg.content) - 1])

          # add new card from champs_list to draft eligible pool
          random.shuffle(remaining_champs)
          draft_eligible.append(remaining_champs.pop())

          # print player, selection, eligible pool
          await message.channel.send(
              f"Thanks for drafting  {message.author}!  \nThis is your current roster: {player_lists[f'player_{i+1}']}\nHere are the champions that are available: {draft_eligible } \nNext player please pick a champion 1-6 to draft"
          )

        turn_count += 1

      # print all players drafted champions
      for i in range(player_count):
        await message.channel.send(
            f"\n\nplayer{i+1}\'s champions: {player_lists[f'player_{i+1}']}")


# Replace 'YOUR_TOKEN' with your actual bot token
client.run(os.environ['TOKEN'])
