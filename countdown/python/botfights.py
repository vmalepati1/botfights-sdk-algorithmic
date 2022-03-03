#! /usr/bin/env python

# botfights.py -- python botfights harness for playing games on botfights.ai


import sys, getopt, json, importlib, base64, time, os, logging


USAGE = '''\
botfights.py -- python command line interface for https://botfights.ai/

USAGE:

    python botfights.py [options] <command> [arguments]

OPTIONS:

    -u, --user_id <user_id>                 set botfights.ai user_id (defaults to environment's "BF_USERNAME")
    -p, --password <password>               set botfights.ai password (defaults to environment's "BF_PASSWORD")
    -t, --tournament_id <tournament_id>     set tournament_id
    -o, --options <options_json>            set fight options to options_json
    -o, --options @fn                       read fight options from fn
    -l, --log-level <level>                 set log level (INFO, DEBUG, ... )


COMANDS:

    human
    local
    remote
    api

EXAMPLES:

    Play bot get_play() in sample-boy.py in game countdown locally:

        $ python botfights.py local countdown sample-bot.get_play

    Play bot get_play() in sample-boy.py in game countdown on botfights.ai:

        $ python botfights.py remote countdown sample-bot.get_play

    Play bot get_play() in sample-boy.py in game countdown on botfights.ai in tournament_id botfights_vi:

        $ python botfights.py --tournament_id botfights_vi remote countdown sample-bot.get_play

'''


API = 'https://api.botfights.ai/api/v1/'


def python2or3_urllib_request_urlopen(url, headers, data, method):
    has_request = True
    try:
        import urllib.request
        import urllib.error
    except:
        has_request = False

    if has_request:
        request = urllib.request.Request(url=url, headers=headers, data=data)
        request.get_method = lambda: method
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            content = e.read()
            raise Exception("HTTPError: code: %s, reason: %s, content: %s" % (e.code, e.reason, content))
    else:
        import urllib2
        request = urllib2.Request(url=url, headers=headers, data=data)
        request.get_method = lambda: method
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            content = e.read()
            raise Exception("HTTPError: code: %s, reason: %s, content: %s" % (e.code, e.reason, content))
    return response


def python2or3_gzip_decompress(s):
    import gzip
    has_gzip_decompress = True
    try:
        foo = gzip.decompress
    except:
        has_gzip_decompress = False
    if has_gzip_decompress:
        return gzip.decompress(s)
    else:
        import StringIO
        return gzip.GzipFile(fileobj=StringIO.StringIO(s)).read()


def call_api(api, username, password, method, path, payload = None):
    url = '%s%s' % (api, path)
    headers = {}
    headers['Authorization'] = 'Basic %s' % (base64.b64encode(('%s:%s' % (username, password)).encode()).decode())
    headers['Accept-Encoding'] = 'gzip'
    data = None
    if None != payload:
        headers['Content-type'] = 'application/json'
        data = json.dumps(payload).encode()
    response = python2or3_urllib_request_urlopen(url, headers, data, method)
    response_data = response.read()
    if response.info().get('Content-Encoding') == 'gzip':
        response_data = python2or3_gzip_decompress(response_data)
    response_value = json.loads(response_data)
    return response_value


def load_bot(s):
    fn, func = s.split('.')
    module = importlib.import_module(fn)
    bot = getattr(module, func)
    return bot


def load_game(s):
    module = importlib.import_module(s)
    game = getattr(module, 'game_factory')()
    return game


def human_play(game_id, options, fight_id, status, client_state, version):
    print('game_id: %s, fight_id: %s, status: %s, version: %s\n' % (game_id, fight_id, status, version))
    print('options: %s\n' % json.dumps(options))
    print('client_state: %s\n' % json.dumps(client_state))
    print('What is your move, human?')
    s = sys.stdin.readline()
    play = json.loads(s)
    return play


def get_bot_play(bot, game_id, options, fight_id, status, client_state, version):
    play = bot(game_id, options, fight_id, status, client_state, version)
    return play


def play_local(game, fight_id, bot, options):
    version = 0
    the_options = game.get_default_options()
    if None != options:
        the_options.update(options)
    logging.info('fight_id: %s' % fight_id)
    logging.info('options: %s' % json.dumps(the_options))
    state = None
    play = get_bot_play(bot, game.get_game_id(), the_options, None, None, None, None)
    version = 0
    while True:
        status, state = game.handle_play(fight_id, the_options, state, play)
        client_state = game.gen_client_state(fight_id, the_options, state)
        version += 1
        logging.info('status: %s' % status)
        logging.info('state: %s' % json.dumps(state))
        logging.info('client_state: %s' % json.dumps(client_state))
        if 'FINISHED' == status:
            return state['score']
        play = get_bot_play(bot, game.get_game_id(), the_options, fight_id, status, client_state, str(version))
        logging.info('play: %s' % json.dumps(play))


def play_remote(game, bot, tournament_id, options, api, username, password):
    logging.info('Creating fight on botfights.ai ...')
    the_options = game.get_default_options()
    if None != options:
        the_options.update(options)
    play = get_bot_play(bot, game.get_game_id(), the_options, None, None, None, None)
    payload = {"game_id": game.get_game_id(), "options": the_options, "tournament_id": tournament_id, "play": play}
    logging.debug('payload\t%s' % json.dumps(payload))
    time_create = time.time()
    response = call_api(api, username, password, 'PUT', 'fight/', payload)
    logging.debug('response\t%s' % json.dumps(response))
    fight_id = response['fight_id']
    state = response['state']
    version = response['version']
    options = response['options']
    status = response['status']
    logging.info('Fight created: https://botfights.ai/fight/%s' % fight_id)
    while True:
        logging.info('Calling bot ...')
        play = get_bot_play(bot, game.get_game_id(), options, fight_id, status, state, version)
        payload = {"play": play, "version": version, "game_id": game.get_game_id()}
        logging.info('Calling API ...')
        logging.debug('payload\t%s' % json.dumps(payload))
        time.sleep(max(0.0, 1.0 - (time.time() - time_create)))
        response = call_api(api, username, password, 'PATCH', 'fight/%s' % fight_id, payload)
        logging.debug('response\t%s' % json.dumps(response))
        state = response['state']
        status = response['status']
        version = response['version']
        if 'FINISHED' == status:
            logging.info('Fight finished. Score: %s' % state['score'])
            logging.info('https://botfights.ai/fight/%s' % fight_id)
            break


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ha:o:u:p:t:l:f:", ["help", "api=", "options=", "username=", "password=", "tournament_id=", "log-level=", "fight_id="])
    except getopt.GetoptError as err:
        print(err)
        print(USAGE)
        sys.exit(2)
    options = None
    username = os.environ.get('BF_USERNAME')
    password = os.environ.get('BF_PASSWORD')
    tournament_id = None
    loglevel = 'INFO'
    api = API
    fight_id = None
    for o, a in opts:
        if 0:
            pass
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--options"):
            if a.startswith('@'):
                options = json.loads(open(a[1:]).read())
            else:
                options = json.loads(a)
        elif o in ("-u", "--username"):
            username = a
        elif o in ("-p", "--password"):
            password = a
        elif o in ("-a", "--api"):
            api = a
        elif o in ("-t", "--tournament_id"):
            tournament_id = a
        elif o in ("-f", "--fight_id"):
            fight_id = a
        elif o in ("-l", "--log-level"):
            loglevel = a
        else:
            assert False, "unhandled option"

    logging.basicConfig(level=loglevel, format='%(asctime)s\t%(levelname)s\t%(message)s', stream=sys.stdout)

    if None == fight_id:
        fight_id = str(int(time.time()))

    if 0 == len(args):
        print(USAGE)
        sys.exit()
    c = args[0]
    if 0:
        pass
    elif "help" == c:
        print(USAGE)
        sys.exit()
    elif "human" == c:
        game = load_game(args[1])
        play_local(game, fight_id, human_play, options)
    elif "local" == c:
        game = load_game(args[1])
        bot = load_bot(args[2])
        play_local(game, fight_id, bot, options)
    elif "remote" == c:
        game = load_game(args[1])
        bot = load_bot(args[2])
        play_remote(game, bot, tournament_id, options, api, username, password)
    elif "api" == c:
        method = args[1]
        path = args[2]
        payload = None
        if method in ('PUT', 'PATCH'):
            payload = json.loads(sys.stdin.read())
        x = call_api(api, username, password, method, path, payload)
        sys.stdout.write(json.dumps(x, indent=2))
    else:
        print(USAGE)
        sys.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
