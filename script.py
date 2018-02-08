from user_operations import client, update_user
import json
import yaml

with open("config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

#user_list = client.users.list(filter="startswith(displayName, 'C')")
def print_user(user):
    user.enable_additional_properties_sending() # yuck!
    print(json.dumps(user.serialize()))

user_list = client(cfg).users.list()

for user in user_list:
    print_user(user)
    print('********************************')
