# sample-bot.py -- sample bot to play countdown on botfights.ai


def get_play_adder(target, operands):
    "just add up all the operands"
    code = ''
    for i in range(len(operands)):
        code += '%d ' % i
    for i in range(len(operands) - 1):
        code += '+ '
    return code



def get_play(game_id, options, fight_id, status, client_state, version):
    "botfights get_play function for countdown"
    if None == client_state:
        return None
    plays = {}
    for round_id, round_data in client_state['rounds'].items():
        target = round_data[0]
        operands = round_data[1]
        code = get_play_adder(target, operands)
        plays[round_id] = code
    return plays

