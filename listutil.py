import tweepy
import argparse
import time
from termcolor import colored
import os

debug = True


class LOG_TYPES:
    MAIN = 0
    IN = 1


def conflicting_args(args):
    print('Conflicting argument %s' % args)


def debug_msg(msg, indent, color='cyan'):
    if debug:
        print(colored('\t' * indent + '>>> ' + msg, color))


def error_msg(err):
    print('')
    print('\033[1m', colored(err, 'red'), '\033[0m')


keys = dict(
    consumer_key='',
    consumer_secret='',
    access_token='',
    access_token_secret=''
)

for key in ['TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET', 'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET']:
    if os.getenv(key) is not None and os.getenv(key) != '':
        keys[key.replace('TWITTER_', '').lower()] = os.getenv(
            key)
    else:
        error_msg('No %s provided. Exiting.' % key)
        exit()

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--update', dest='update', action='store_true')
    parser.set_defaults(update=False)
    parser.add_argument(
        '--source_id', help='Source (original) list ID', type=int)
    parser.add_argument(
        '--destination_id', help='Destination (your fork, created with --fork) list ID', type=int)

    parser.add_argument('--remix', dest='remix', action='store_true')
    parser.set_defaults(remix=False)
    parser.add_argument(
        '--name', type=str)
    parser.add_argument(
        '--mode', type=str)
    parser.add_argument(
        '--input', nargs='+',  type=int)

    parser.add_argument(
        '--fork', help='Fork list id to a new list in your account', type=int)

    parser.add_argument(
        '--delay', help='Delay in fetching/updating', type=float, default=0.3)
    parser.add_argument(
        '--debug', help='Debug messages in terminal',  default=True, type=lambda x: (str(x).lower() == 'true'))

    args = parser.parse_args()

    debug = args.debug
    if debug:
        print(colored(' Twitter List Util', 'cyan'))
    if args.fork is not None:
        if args.update:
            conflicting_args(args.update)
        if args.remix:
            conflicting_args(args.remix)
        original_list = api.get_list(list_id=args.fork)
        debug_msg('Forking list: ' + original_list.name, LOG_TYPES.MAIN)
        debug_msg('Mode: ' + original_list.mode, LOG_TYPES.MAIN)

        members = tweepy.Cursor(
            api.list_members, list_id=args.fork).items()
        fork = api.create_list(name=original_list.name,
                               mode=original_list.mode)
        for member in members:
            time.sleep(args.delay)
            try:
                y = api.add_list_member(
                    screen_name=member.screen_name, list_id=fork.id)
            except Exception as e:
                error_msg(e)
            else:
                debug_msg('Added @' + member.screen_name,
                          LOG_TYPES.IN, 'white')
                debug_msg('List member count at: ' +
                          str(y.member_count), LOG_TYPES.IN, 'green')
    else:
        if args.remix:
            if args.update:
                conflicting_args(args.update)
            if len(args.input) < 2:
                error_msg('Two or more list IDs required.')
            if args.name is None or args.name == '':
                error_msg('Name for list is required, use --name to specify.')
            if args.mode is None or args.mode == '':
                error_msg(
                    'Privacy mode is required. [public/private], use --mode to specify.')

            remix = api.create_list(name=args.name,
                                    mode=args.mode)

            debug_msg('Remixing lists: ' + str(args.input), LOG_TYPES.IN)
            members = []
            for twitter_list in args.input:
                for member in tweepy.Cursor(
                        api.list_members, list_id=twitter_list).items():
                    members.append(member.screen_name)
            debug_msg('Total count: ' + str(len(members)), LOG_TYPES.IN)
            for member in list(dict.fromkeys(members)):
                time.sleep(args.delay)
                try:
                    y = api.add_list_member(
                        screen_name=member, list_id=remix.id)
                except Exception as e:
                    error_msg(e)
                else:
                    debug_msg('Added @' + member,
                              LOG_TYPES.IN, 'white')
                    debug_msg('List member count at: ' +
                              str(y.member_count), LOG_TYPES.IN, 'green')
        else:
            if args.update:
                if args.remix:
                    conflicting_args(args.remix)
                if args.source_id is None or args.source_id == '':
                    error_msg(
                        'Source list ID required, use --source_id to specify.')
                if args.destination_id is None or args.destination_id == '':
                    error_msg(
                        'Destination list ID required, use --destination_id to specify.')
                destination_list_members = [member.screen_name for member in tweepy.Cursor(
                    api.list_members, list_id=args.destination_id).items()]
                for member in tweepy.Cursor(
                        api.list_members, list_id=args.source_id).items():

                    if member.screen_name in destination_list_members:
                        continue
                    try:
                        time.sleep(args.delay)
                        y = api.add_list_member(
                            screen_name=member.screen_name, list_id=args.destination_id)
                    except Exception as e:
                        error_msg(e)
                    else:
                        debug_msg('Added @' + member.screen_name,
                                  LOG_TYPES.IN, 'white')
