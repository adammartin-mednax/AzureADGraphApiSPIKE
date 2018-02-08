# SPIKE: Using Azure AD Graph API to create a user

The intent of this code is to act as a spike on how to create a user via the Azure AD Graph API.  Specifically we want to create a B2C user.  From the initial testing it appears we can create them with limits described below.  In addition this specific spike shows the logic for creating virtually any type of user via the Graph API.

## Pre-requisites

In order to execute the code in this spike you must have the following:

* Python version 3.6.3 [It is likely you can use a lower version but it is tested and constrained via pyenv to 3.6.3]
* Pip
* The Tenant Id in Azure AD that you wish to operate on.
* An application in Azure AD with rights to at least create users in Azure (and the associated Client ID/Client Key)

### Installing

N/A This is a spike it is not intended to be installed.

### Configuration File

This spike assumes a `config` directory with a `config.yml` file

The config file should be formatted as:

```
tenant_id: [NA Tenant Identity]
client_id: [Custom application 'Object Id']
client_key: [Created custom application Client Key]
ad_graph_url: 'https://graph.windows.net' 
default_password: [Default Password we want to use]
principle_template: '{}@HISCFederationDev.onmicrosoft.com'

```

## Running Tests

N/A This is a spike

## Deployment

N/A This is a spike

## Lessons Learned

There have been several lessons learned -

* Sign In Names seems to be the key to what you use to login as but not sure how this ties in to anything yet.  [Create Local User Account](https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/users-operations#CreateLocalAccountUser) and [Create Consumer Accounts](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-devquickstarts-graph-dotnet#create-consumer-user-accounts)
  * If it is not `signInNames` that drives the login then it may be `userPrincipalName`, `displayName`, `mailNickname`, and `mail` attribute.
* I am not sure about the relationship between the `mail` attribute and Exchange Online access.
* There are multiple API's for interacting with user identities.  The two most notable are the Azure AD Graph API and the Microsoft Graph API.  Azure B2C is constrained to the Azure AD Graph API. At some point Azure AD Graph will be replaced by Microsoft Graph API and we will need to move.  [This](https://blogs.msdn.microsoft.com/aadgraphteam/2016/07/08/microsoft-graph-or-azure-ad-graph/) provides an understanding of the difference.
* There are several attributes which may or may not be important we cannot edit:
  * `mail` - This attibute cannot be modified per Microsoft: `Because the mail attribute is tied to Exchange Online, we don't permit you to write to that attribute unless you have an Exchange Online license.  When you activate a license for the user, Exchange Online will update the field with the correct mailbox mail address during the creation of the user's mailbox.  You can utilize "MailNickName" and " otherMails" during the creation of a user.  This field will also depend upon if it is a "local account (B2C)" or "work or school account".`
  * `creationType` - This attribute which can have the value of `Invitation` is not editable.  I'm curious to know if this is what drives the send invitation process through B2C.
  * `proxy_addresses` - I am unsure about the purpose or usage of this attribute but it is not settable.
* The [Azure AD Graph API SDK](https://github.com/Azure/azure-sdk-for-python/tree/master/azure-graphrbac) is rather badly written and you must extend to get the desired funcationality.  Luckily it seems to be designed for extension as I was easily able to extend the `UserBase` object.  If there is concern you can go one level down as `UserBase` extends `Model` which is a component in the completely seperate and public [MSRest Project](https://github.com/Azure/msrest-for-python).
  * Biggest issue with the graph api is that in approximately version 0.40 of the package they added `additional_properties` argument.  While this argument takes a dict it only handles simple mappings not a case where a key contiains a list of values. As such `otherMails` and `signInNames` are not supported in the current implementation.
  * I suspect that several object will need to be dealt with: `user_create_parameters`, `user_update_parameters`, and `user_get_parameters` probably all need some massaging.
  * Filtration (i.e. finding specific records or groups of records) will require knowledge of how to generate [Filters](https://msdn.microsoft.com/library/azure/ad/graph/howto/azure-ad-graph-api-supported-queries-filters-and-paging-options#-filter)
  * The [API Documentation](http://azure-sdk-for-python.readthedocs.io/en/latest/graphrbac.html) is fairly anemic.
  * Available [User Attributes](https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/entity-and-complex-type-reference#user-entity) are documented.
* Deactivate is fundamentally an update from what I see in the documentation.  Note the ability to do a delete can only be granted via PowerShell but I don't think this is a required capability.
* Group manipulations look strateforward once you understand the user api [Group Operations](https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/groups-operations).  We again may need custom objects.
* Semi useless but there is documentation on the [Azure Error Codes](https://msdn.microsoft.com/en-us/library/azure/ad/graph/howto/azure-ad-graph-api-error-codes-and-error-handling)
* If we need greater ganularity on Azure AD Graph API Client Instantiation there is an [ADAL Client](https://docs.microsoft.com/en-us/python/azure/python-sdk-azure-authenticate?view=azure-python#mgmt-auth-token).  I did not see a reason to use it.
* Configuration of a B2C tenant and it's API information is [Documented](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-devquickstarts-graph-dotnet) but most of this should already be accomplished by the time an engineering team gets involved.

Extension Attributes lessons learned -
* Extension Attributes aren't normally accessable from the Azure AD Graph API.
* Followed instructions on [Adding Extension Attributes](https://msdn.microsoft.com/en-us/library/azure/ad/graph/howto/azure-ad-graph-api-directory-schema-extensions#SampleRequests) to create a franchises attribute for use associated to the `Consumer IAM` application.  The instructions are very out of date in many ways.
  * URL To create extension attributes: `https://graph.windows.net/[Tenant ID]/applications/[Application ID]/extensionProperties?api-version=1.6`
  * URL to find the object Id is easiest here `https://graph.windows.net/[Tenant ID]/applications?api-version=1.6`
  * Body looks like:

```

{
    "name": "franchises",
    "dataType": "String",
    "targetObjects": [
        "User"
    ]
}

```

## TODO

Learn a little more from [This Tutorial](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-devquickstarts-graph-dotnet)

Biggest concerns -

* Can't use ExtensionAttribute5 had to create `extension_e26ba073fd5142af9fa6455daecdcc9c_franchises`
* Was I right that signInName is the correct attribute.
* What is the interaction really like for an end user?
* Perhaps we completely skip programmatic creation and simply figure out how to programmatically send invitations to join the B2C directory.  Topics to interrogate:
   * [Custom Policies](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-overview-custom)
   * [Sending JWT Invitation request to B2C](https://github.com/Azure-Samples/active-directory-b2c-advanced-policies/blob/master/wingtipgamesb2c/src/WingTipGamesWebApplication/Controllers/InvitationController.cs#LC90)
   * [Example JWT policy definition for receipt of a request](https://github.com/Azure-Samples/active-directory-b2c-advanced-policies/blob/master/wingtipgamesb2c/Policies/b2ctechready.onmicrosoft.com_B2C_1A_invitation.xml)
   * [Example App](https://wingtipgamesb2c.azurewebsites.net/Invitation/Create)
