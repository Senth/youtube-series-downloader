from os import path, system
from typing import Pattern
import sys
import site
import importlib.util

config_dir = path.join('config', __name__)
config_file = path.join(config_dir, 'config.py')
example_file = path.join(config_dir, 'config.example.py')

# Search for config file in sys path
sys_config = path.join(sys.prefix, config_file)
user_config = path.join(site.getuserbase(), config_file)
config_file = ''
if path.exists(sys_config):
    config_file = sys_config
elif path.exists(user_config):
    config_file = user_config
# User hasn't configured the program yet
else:
    sys_config_example = path.join(sys.prefix, example_file)
    user_config_example = path.join(site.getuserbase(), example_file)
    if path.exists(sys_config_example):
        config_example_file = sys_config_example
        config_file = path.join(sys.prefix, config_file)
    elif path.exists(user_config_example):
        config_example_file = user_config_example
        config_file = path.join(site.getuserbase(), config_file)
    # Couldn't find the example file
    else:
        print("Error: no configuration found. It should be here: '" + user_config + "'")
        print('run: locate ' + example_file)
        print('This should help you find the current config location.')
        print('Otherwise you can download the config.example.py from https://github.com/Senth/youtube-series-downloader/tree/main/config and place it in the correct location')
        sys.exit(1)

    print("This seems like it's the first time you run this program.")
    print("For this program to work properly you have to configure it by editing '" + user_config + "'.")
    print("In the same folder there's an example file 'config.example.py' you can copy to 'config.py'.")
    sys.exit(0)

spec = importlib.util.spec_from_file_location("config", user_config)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

def _print_missing(variable_name):
    print('Missing ' + variable_name + ' variable in config file: ' + user_config)
    print('Please add it to you config.py again to continue')
    sys.exit(1)

# Add default values
THREADS = 1
SPEED_UP_DEFAULT = 1

# Get optional variables
try:
    THREADS = config.THREADS
except AttributeError:
    pass

try:
    SPEED_UP_DEFAULT = config.SPEED_UP_DEFAULT
except AttributeError:
    pass

# Check if all required variables are set
try:
    SERIES_DIR = config.SERIES_DIR
except AttributeError:
    _print_missing('SERIES_DIR')

try:
    CHANNELS = config.CHANNELS
except AttributeError:
    _print_missing('CHANNELS')


# Check syntax of CHANNELS
def _check_regex(channel_name, list_name, info):
    if list_name in info:
        # Should be a list
        if type(info[list_name]) is list:
            # All values should be regex
            for value in info[list_name]:
                if not isinstance(value, Pattern):
                    print('Channel ({}) has an invalid {} item ({}) that is not a Regex pattern in config file: {}'.format(
                        channel_name,
                        list_name,
                        str(value),
                        user_config
                    ))
                    sys.exit(1)
        else:
            print('Channel ({}), {} is not list in config file: {}'.format(
                channel_name,
                list_name,
                user_config
            ))
            sys.exit(1)


_CHANNEL_ID_EXAMPLE = 'UCcJgOeune0II4a_qi9OMkRA'
for name, info in CHANNELS:
    # Name is string
    if type(name) is not str:
        print('Channel ({}) name is not a string in config file: {}'.format(name, user_config))
        sys.exit(1)

    # Channel id required
    if 'channel_id' in info:
        # Channel id valid format
        if type(info['channel_id']) is not str or len(info['channel_id']) != len(_CHANNEL_ID_EXAMPLE):
            print('Channel ({}), channel_id ({}) does not look like a valid channel id in config file: {}'.format(
                name, info['channes_id'], user_config
            ))
            print('Here is an example of a channel id {}'.format(_CHANNEL_ID_EXAMPLE))
            sys.exit(1)
    else:
        print('Channel ({}) missing channel_id in config file: {}'.format(name, user_config))
        sys.exit(1)

    # Dir (optional)
    if 'dir' in info and type(info['dir']) is not str:
        print('Channel ({}) dir ({}) is not a string in config file: {}'.format(
            name, str(info['dir'], user_config)
        ))
        sys.exit(1)

    # Speed (optional)
    if 'speed' in info and type(info['speed']) is not int and type(info['speed']) is not float:
        print('Channel ({}) speed ({}) is not a number in config file {}'.format(
            name, str(info['speed'], user_config)
        ))
        sys.exit(1)

    # Include & Exclude (optional)
    _check_regex(name, 'include', info)
    _check_regex(name, 'exclude', info)


