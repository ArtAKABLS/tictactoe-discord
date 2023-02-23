import random

GRID = [[None, None, None], [None, None, None], [None, None, None]]
emojis = ['⬅️', '↖️', '↙️', '⬇️',
          '⏺️',
          '⬆️', '↗️', '↘️', '➡️']
X = ':x:'
O = ':o:'
default_symbol = ':white_medium_square:'


async def tic_tac(ctx, bot):
    GRID = [[None, None, None], [None, None, None], [None, None, None]]
    edge_len = 3
    playfield_content = f'{default_symbol * edge_len}\n{default_symbol * edge_len}\n{default_symbol * edge_len}'
    playfield = await ctx.send(playfield_content)
    for emoji in emojis:
        await playfield.add_reaction(emoji)

    used_signs = []

    rnd = random.random()
    first = None
    second = None

    if rnd > 0.5:
        first = ctx.author
        second = ctx.message.mentions[0]
    else:
        first = ctx.message.mentions[0]
        second = ctx.author

    win = 0
    turnplayer_sign = 'X'
    current_player = first


    turn_str = f'\nit\'s your turn {current_player.name}'
    whos_turn = await ctx.send(turn_str)
    await playfield.edit(content=playfield_content)

    while win == 0:
        def check(reaction, user):
            return user == current_player and str(reaction.emoji) in emojis

        reaction, user = await bot.wait_for('reaction_add', timeout=420.0, check=check)
        reaction_str = str(reaction)

        if reaction_str in used_signs:
            continue

        if reaction_str == '⬅️' and GRID[1][0] is None:
            GRID[1][0] = turnplayer_sign
        if reaction_str == '↖️' and GRID[0][0] is None:
            GRID[0][0] = turnplayer_sign
        if reaction_str == '↙️' and GRID[2][0] is None:
            GRID[2][0] = turnplayer_sign
        if reaction_str == '⬇️' and GRID[2][1] is None:
            GRID[2][1] = turnplayer_sign
        if reaction_str == '⏺️' and GRID[1][1] is None:
            GRID[1][1] = turnplayer_sign
        if reaction_str == '⬆️' and GRID[0][1] is None:
            GRID[0][1] = turnplayer_sign
        if reaction_str == '↗️' and GRID[0][2] is None:
            GRID[0][2] = turnplayer_sign
        if reaction_str == '↘️' and GRID[2][2] is None:
            GRID[2][2] = turnplayer_sign
        if reaction_str == '➡️' and GRID[1][2] is None:
            GRID[1][2] = turnplayer_sign
        used_signs.append(reaction_str)

        playfield_content = change_playfield(GRID)
        await playfield.edit(content=playfield_content)

        if (GRID[0][0] == GRID[1][1] == GRID[2][2] is not None) or (GRID[2][0] == GRID[1][1] == GRID[0][2] is not None):
            await ctx.send(f'{current_player.name} wins')
            GRID = [[None, None, None], [None, None, None], [None, None, None]]
            return
        if (GRID[0][0] == GRID[0][1] == GRID[0][2] is not None) or (GRID[1][0] == GRID[1][1] == GRID[1][2] is not None)\
                or (GRID[2][0] == GRID[2][1] == GRID[2][2] is not None):
            GRID = [[None, None, None], [None, None, None], [None, None, None]]
            await ctx.send(f'{current_player.name} wins')
            return
        if (GRID[0][0] == GRID[1][0] == GRID[2][0] is not None) or (GRID[0][1] == GRID[1][1] == GRID[2][1] is not None)\
                or (GRID[0][2] == GRID[1][2] == GRID[2][2] is not None):
            GRID = [[None, None, None], [None, None, None], [None, None, None]]
            await ctx.send(f'{current_player.name} wins')
            return

        if sorted(used_signs) == sorted(emojis):
            await ctx.send(f'tie')


        if turnplayer_sign == 'X':
            turnplayer_sign = 'O'
            current_player = second
        else:
            turnplayer_sign = 'X'
            current_player = first


        new_turn = f'\nit\'s your turn {current_player.name}'
        await whos_turn.edit(content=new_turn)


    return


def change_playfield(grid):
    new_playfield = f''
    for row in grid:
        for j, sym in enumerate(row):
            if sym == None:
                new_playfield += f'{default_symbol}'
            if sym == 'X':
                new_playfield += f'{X}'
            if sym == 'O':
                new_playfield += f'{O}'
            if j == len(row) - 1:
                new_playfield += '\n'

    return new_playfield
