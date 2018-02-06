from azure.common.credentials import ServicePrincipalCredentials
from azure.graphrbac import GraphRbacManagementClient
from azure.graphrbac.models import PasswordProfile
from hisc_user_create_parameters import HISCUserCreateParameters

def create_user(fname, lname, email, config):
	return client(config).users.create(_user_create_parameters(fname, lname, email, config))

def client(config):
	credentials = ServicePrincipalCredentials( client_id = config['client_id'], secret = config['client_key'], tenant = config['tenant_id'], resource=config['ad_graph_url'] )
	return GraphRbacManagementClient(credentials, config['tenant_id'])

def _user_create_parameters(fname, lname, email, config):
	mail_nickname = '{}#EXT#'.format(_format_email(email))
	principle_name = config['principle_template'].format(mail_nickname)
	
	return HISCUserCreateParameters(
		account_enabled=True,
		display_name='{}.{}'.format(fname, lname),
		password_profile=_password_profile(config),
		user_principal_name=principle_name,
		mail_nickname=mail_nickname,
		given_name=fname,
		surname=lname,
		user_type='Guest',
		other_mails=[email],
		usage_location='US'
    )

def _format_email(email):
	return email.replace('@', '_')

def _password_profile(config):
	return PasswordProfile(password=config['default_password'], force_change_password_next_login=True)