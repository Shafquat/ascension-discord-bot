import discord
import os
import random

champions_list = [
    'Arha Templar', 'Arha Sensei', 'Water Djinn', 'Psyche Askara',
    'Unbound Emissary', 'Raven Siren', 'Twilight Scout', 'Icarus Steelfoot',
    'Rut', 'Tyranyx', 'PRIME', 'Hedron Smithy', 'Mechana Initiate',
    'Reactor Monk', 'Bringer of Despair', 'Shadowcaster', 'Demon Slayer',
    'Naka Blackblade', 'Nihilbomber', 'Faerie Commander', 'Spike Vixen',
    'Tuskrider', 'Runic Lycanthrope', 'Flytrap Witch'
]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Dictionary to store draft details for each channel
draft_sessions = {}


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower() == '!startdraft':
    if message.channel.id in draft_sessions:
      await message.channel.send("A draft is already in progress.")
      return

    await message.channel.send(
        "Hello! Let's start an Ascension Tactics draft. Out of the 24 champions available, 6 random champions will be added to a draft eligible pool. Each turn, a player will select a champion to draft. A new champion from the remaining available champions will be added to the draft eligible pool so that there is always 6 champions in the draft eligible pool. The draft will end once each player has selected 3 champions. How many players will be participating in this draft?"
    )

    def check(m):
      return m.author != client.user and m.channel == message.channel and m.content.isdigit(
      ) and 2 <= int(m.content) <= 4

    msg = await client.wait_for('message', check=check)
    player_count = int(msg.content)

    draft_eligible = random.sample(champions_list, 6)
    remaining_champs = [x for x in champions_list if x not in draft_eligible]
    player_lists = {f"player_{i+1}": [] for i in range(player_count)}

    draft_sessions[message.channel.id] = {
        'player_count': player_count,
        'draft_eligible': draft_eligible,
        'remaining_champs': remaining_champs,
        'player_lists': player_lists,
        'turn_count': 0,
        'current_player': 1
    }

    await message.channel.send(
        f"Let's play a {player_count} player game! \nHere are the champions that are available: {draft_eligible}"
    )
    await draft_phase(message.channel)


async def draft_phase(channel):
  session = draft_sessions[channel.id]

  while session['turn_count'] < 3 * session['player_count']:
    current_player = session['current_player']
    await channel.send(
        f"Player {current_player}, please pick a champion 1-6 to draft")
    for index, champs in enumerate(session['draft_eligible']):
      await channel.send(f'**{index + 1}. {champs}**')
      await channel.send(file=discord.File('ascension heroes/' + champs +
                                           '.jpeg'))

    def check(m):
      return m.author != client.user and m.channel == channel and m.content.isdigit(
      ) and int(m.content) in range(1, 7)

    msg = await client.wait_for('message', check=check)
    selection = int(msg.content) - 1

    player_list_key = f"player_{current_player}"
    session['player_lists'][player_list_key].append(
        session['draft_eligible'][selection])

    session['draft_eligible'].pop(selection)
    new_champ = session['remaining_champs'].pop(
        random.randint(0,
                       len(session['remaining_champs']) - 1))
    session['draft_eligible'].append(new_champ)

    session['turn_count'] += 1
    session['current_player'] = 1 if current_player == session[
        'player_count'] else current_player + 1

    # Print all players' drafted champions
    for i in range(session['player_count']):
      player_list_key = f"player_{i+1}"
      await channel.send(
          f"\n\nPlayer {i+1}'s champions: {session['player_lists'][player_list_key]}"
      )

  del draft_sessions[channel.id]  # Clear the draft session after completion


# Replace 'YOUR_TOKEN' with your actual bot token
client.run(os.environ['TOKEN'])
