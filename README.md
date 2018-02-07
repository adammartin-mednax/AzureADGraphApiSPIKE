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

* I am not sure what drives the user id login functionality between `signInNames`, `userPrincipalName`, `displayName`, `mailNickname`, and `mail` attribute.
* I am not sure about the relationship between the `mail` attribute and Exchange Online access.
* There are multiple API's for interacting with user identities.  The two most notable are the Azure AD Graph API and the Microsoft Graph API.  Azure B2C is constrained to the Azure AD Graph API.
* There are several attributes which may or may not be important we cannot edit:
  * `mail` - This attibute cannot be modified per Microsoft: `Because the mail attribute is tied to Exchange Online, we don't permit you to write to that attribute unless you have an Exchange Online license.  When you activate a license for the user, Exchange Online will update the field with the correct mailbox mail address during the creation of the user's mailbox.  You can utilize "MailNickName" and " otherMails" during the creation of a user.  This field will also depend upon if it is a "local account (B2C)" or "work or school account".`
  * `creationType` - This attribute which can have the value of `Invitation` is not editable.  I'm curious to know if this is what drives the send invitation process through B2C.
  * `proxy_addresses` - I am unsure about the purpose or usage of this attribute but it is not settable.
* The [Azure AD Graph API SDK](https://github.com/Azure/azure-sdk-for-python/tree/master/azure-graphrbac) is rather badly written and you virtually must extend to get the desired funcationality.  Luckily it seems to be designed for extension as I was easily able to extend the `UserBase` object.  If there is concern you can go one level down as `UserBase` extends `Model` which is a component in the completely seperate [MSRest Project](https://github.com/Azure/msrest-for-python).
* Sign In Names seems to be the key to what you use to login as but not sure how this ties in to anything yet.  [Create Local User Account](https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/users-operations#CreateLocalAccountUser)

## TODO

I want to figure out how to do an Update on behalf of an owner for a change.

I want to figure out how to do a Deactivate of a user.

Learn a little more from [This Tutorial](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-devquickstarts-graph-dotnet)

Biggest concerns -

* Given the learnings above how do we create users who are able to use their identity?
* Perhaps we completely skip programmatic creation and simply figure out how to programmatically send invitations to join the B2C directory.  Topics to interrogate:
   * [Custom Policies](https://docs.microsoft.com/en-us/azure/active-directory-b2c/active-directory-b2c-overview-custom)
   * [Sending JWT Invitation request to B2C](https://github.com/Azure-Samples/active-directory-b2c-advanced-policies/blob/master/wingtipgamesb2c/src/WingTipGamesWebApplication/Controllers/InvitationController.cs#LC90)
   * [Example JWT policy definition for receipt of a request](https://github.com/Azure-Samples/active-directory-b2c-advanced-policies/blob/master/wingtipgamesb2c/Policies/b2ctechready.onmicrosoft.com_B2C_1A_invitation.xml)
   * [Example App](https://wingtipgamesb2c.azurewebsites.net/Invitation/Create)
