import confuse

# HARD CODED
APPNAME = 'leto'

# CONFIG SETUP
###############
config = confuse.Configuration(APPNAME, __name__)

# @TODO remove this and move config files to ~/.config/webserver/
config.set_file('cli/config/external.conf.yml')
config.set_file('cli/config/internal.conf.yml')