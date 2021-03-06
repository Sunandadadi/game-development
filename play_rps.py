"""
Author: J. Weible jweible@illinois.edu

Connects to the PZ-server to play a game of Rock, Paper, Scissors.

This can be called from a command line to authenticate with an existing
authorized netid and player_key and it will query the game_types to find the
right id, then request a match and wait for opponent to compete.

The opponent might be another running instance of this program using different
credentials.

Usage:
  play_rps.py [options] <netid> <player_key>

Options:
  --server=<url>  Specify PZ-Server base URL [default: https://jweible.web.illinois.edu/pz-server/games/]
  -h --help       Show this screen.

"""

import requests
import docopt
from random import choice, randint
import json
from time import sleep
import logging
# logging.basicConfig(level=logging.DEBUG)


def play_rps(pz_server_url: str, netid: str, player_key: str):

    # start a fresh session with blank cookies:
    session = requests.Session()
    session.headers = {"Connection": "close"}  # Disables HTTP Keep-Alive

    # query the available game_types to find the RPS id:
    game_search = session.get(url=pz_server_url + "game-types",
                               json={"netid": netid,
                                     "player_key": player_key})

    # TODO: there's not sufficient error checking here...
    try:
        result = game_search.json()['result']
    except Exception as e:
        print('unexpected response:')
        print(game_search.content)
        print('\nfollowed by exception:' + str(e))
        return

    # search for a multi-round, 2-player "Rock, Paper, Scissors":
    game_id = False
    for g in result:
        if (g['category'] == 'RPS' or 'scissors' in g['fullname'].lower()) \
                and 'rounds' in g['fullname'] and g['num_players'] == 2:
            game_id = g['id']

    if game_id:
        print('Found matching game-type: ', game_id)
    else:
        print('Game not available now.')
        exit()

    # Now request a single match of that game type:
    request_match = session.post(url=pz_server_url + "game-type/{}/request-match".format(game_id),
                           json={"netid": netid,
                                 "player_key": player_key})

    print(request_match.text)
    match_id = request_match.json()['result']['match_id']

    # This game has multiple "rounds" or "turns".  So loop through a
    # sequence of alternating between requests "await-turn" and "move":

    while True:
        # wait for my turn:
        while True:
            print('\n\nrequesting await-turn now.')
            await_turn = session.get(url=pz_server_url + "match/{}/await-turn".format(match_id))
            # print(await_turn.text)
            result = await_turn.json()["result"]
            print('Update on previous move(s): ' + json.dumps(result))
            if result["match_status"] == "in play":
                turn_status = result["turn_status"]
                if turn_status == "your turn":
                    # Yea! There was much rejoicing.
                    break  # exit the while loop.
                if "Timed out" in turn_status:
                    print('PZ-server said it timed out while waiting for my turn to come up...')
                print('waiting for my turn...')
                sleep(3)
                continue
            elif result["match_status"] in ["game over", "scored, final"]:
                print('Game over?  Who won?')
                return
            elif result["match_status"] == "awaiting more player(s)":
                print('match has not started yet. sleeping a bit...')
                sleep(5)
            else:
                raise ValueError('Unexpected match_status: ' + result["match_status"])

        # Ok, now it's my turn...

        # submit my move:
        move_instruction = choice(["rock", "paper", "scissors"])
        print("\nshhh... sending my choice of", move_instruction)
        print("-------------------------------------------------------------------------------------------")
        print("url is", pz_server_url + "match/{}/move".format(match_id))
        print("json is", {"move": move_instruction})
        print("-------------------------------------------------------------------------------------------")
        submit_move = session.post(url=pz_server_url + "match/{}/move".format(match_id),
                               json={"move": move_instruction})
        move_result = submit_move.json()["result"]
        print(move_result)
        if move_result["match_status"] in ["game over", "scored, final"]:
            print('Game over?  Who won?')
            break

        """Insert a small delay to reduce the chance of cPanel server throttling
        this client, and to simulate the "thinking time" of a more challenging game."""
        sleep(3)

    return


if __name__ == '__main__':

    opt = docopt.docopt(__doc__)
    # print(opt)
    netid = opt.get('<netid>')
    player_key = opt.get('<player_key>')
    pz_server = opt.get('--server')

    play_rps(pz_server, netid, player_key)
