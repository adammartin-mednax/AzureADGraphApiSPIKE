from user_operations import client
import yaml

with open("config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

#user_list = client.users.list(filter="startswith(displayName, 'C')")

user_list = client(cfg).users.list()

for user in user_list:
    print(user.serialize())


