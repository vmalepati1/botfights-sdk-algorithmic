# countdown.py -- botfights SDK for countdown game


import sys, json, re, random


GAME_ID = 'countdown'
GAME_NAME = 'Countdown'


DEFAULT_OPTIONS = {'min_target': 1, 'max_target': 1000, 'num_operands': 10, 'min_operand': 1, 'max_operand': 100, 'num_rounds': 1, 'must_use_all': False, 'allow_reuse': False, 'operators': '+-/*'}


def game_factory():
    return Game_Countdown()


def evaluate(data, code, options):
    stack = []
    used = {}
    for i in code.split():
        if None != re.match('^[0-9]+$', i):
            x = int(i)
            if (not options.get('allow_reuse', False)) and x in used:
                raise Exception('reusing numbers not allowed')
            used[x] = True
            stack.append(int(data[x]))
        else:
            if not i in options.get('operators', ''):
                raise Exception('operator "%s" not allowed')
            if 0 :
                pass
            elif '+' == i:
                stack.append(stack.pop() + stack.pop())
            elif '-' == i:
                right = stack.pop()
                left = stack.pop()
                if (right > left):
                    raise Exception('negative numbers not allowed')
                stack.append(left - right)
            elif '*' == i:
                stack.append(stack.pop() * stack.pop())
            elif '/' == i:
                denominator = stack.pop()
                numerator = stack.pop()
                if (0 != (numerator % denominator)):
                    raise Exception('fractions not allowed')
                stack.append(numerator // denominator)
            elif '%' == i:
                denominator = stack.pop()
                numerator = stack.pop()
                stack.append(numerator % denominator)
            else:
                raise Exception('code not recognized "%s"' % i)
    if (options.get('must_use_all', True)) and (len(used) != len(data)):
        raise Exception('must use all data')
    if 1 != len(stack):
        raise Exception('expected stack length of 1')
    return stack[0]


class Game_Countdown:


    def __init__(self):
        pass


    def get_game_id(self):
        return GAME_ID


    def get_name(self):
        return GAME_NAME


    def get_default_options(self):
        return DEFAULT_OPTIONS


    def gen_client_state(self, fight_id, options, state):
        a = {}
        a['rounds'] = {}
        rng = random.Random(options.get('seed', fight_id))
        for i in range(options.get('num_rounds')):
            target = rng.randrange(options['min_target'], options['max_target'])
            operands = []
            for j in range(options['num_operands']):
                operands.append(rng.randrange(options['min_operand'], options['max_operand']))
            a['rounds']['%d' % i] = (target, operands)
        if 'score' in state:
            a['score'] = state.get('score')
        return a


    def handle_play(self, fight_id, options, state, play):
        # state is None for new fight. return (status, state)
        # a non-None score implies fight is finished.
        # state is hidden from user but persists.
        # response is shown to the user.
        if None == state:
            status = 'RUNNING'
            seed = fight_id
            state = {'fight_id': fight_id}
        else:
            status = 'FINISHED'
            client_state = self.gen_client_state(fight_id, options, state)
            score = 0
            for i in range(options['num_rounds']):
                round_num = str(i)
                code = play.get(round_num)
                target = int(client_state['rounds'][round_num][0])
                operands = client_state['rounds'][round_num][1]
                result = 0
                try:
                    result = evaluate(operands, code, options)
                except:
                    pass
                score += (target - result) ** 2
            state = {'score': score}
        return (status, state)


def main(argv):
    c = argv[0]
    if 0:
        pass

    elif 'evaluate' == c:
        x = json.loads(sys.stdin.read())
        code = x['code']
        data = x['data']
        options = DEFAULT_OPTIONS
        options.update(x['options'])
        x = evaluate(data, code, options)
        sys.stdout.write('%d\n' % x)


if __name__ == '__main__':
    main(sys.argv[1:])

