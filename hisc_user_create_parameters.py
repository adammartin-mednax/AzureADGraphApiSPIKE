from azure.graphrbac.models import UserBase

class HISCUserCreateParameters(UserBase):

    _validation = {
        'account_enabled': {'required': True},
        'display_name': {'required': True},
        'password_profile': {'required': True},
        'user_principal_name': {'required': True},
        'mail_nickname': {'required': True},
    }

    _attribute_map = {
        'immutable_id': {'key': 'immutableId', 'type': 'str'},
        'usage_location': {'key': 'usageLocation', 'type': 'str'},
        'given_name': {'key': 'givenName', 'type': 'str'},
        'surname': {'key': 'surname', 'type': 'str'},
        'user_type': {'key': 'userType', 'type': 'str'},
        'account_enabled': {'key': 'accountEnabled', 'type': 'bool'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'password_profile': {'key': 'passwordProfile', 'type': 'PasswordProfile'},
        'user_principal_name': {'key': 'userPrincipalName', 'type': 'str'},
        'mail_nickname': {'key': 'mailNickname', 'type': 'str'},
        'other_mails': {'key': 'otherMails', 'type': '[str]'},
        'mail': {'key': 'mail', 'type': 'str'}, # Only useable if we actually have the mail attribute
    }

    def __init__(self, 
        account_enabled, 
        display_name, 
        password_profile, 
        user_principal_name, 
        mail_nickname, 
        immutable_id=None, 
        usage_location=None, 
        given_name=None, 
        surname=None, 
        user_type=None, 
        mail=None,
        other_mails=None):
        super(HISCUserCreateParameters, self).__init__(
            immutable_id=immutable_id, 
            usage_location=usage_location, 
            given_name=given_name, 
            surname=surname, 
            user_type=user_type)
        self.account_enabled = account_enabled
        self.display_name = display_name
        self.password_profile = password_profile
        self.user_principal_name = user_principal_name
        self.mail_nickname = mail_nickname
        self.mail = mail
        self.other_mails = other_mails