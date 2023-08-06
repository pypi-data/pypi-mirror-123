
import re, uuid
from tinydb import Query, where
from typing import Tuple
from arnparse import arnparse
from awsee.messages import Messages
from awsee.style import Style
from awsee.emoticons import Emoticons
from awsee.utils import Utils
from awsee.tableargs import TableArgs
from awsee.prettytable import PrettyTable
from awsee.repository import CredentialsRepository, RoleRepository
from awsee.general import *

from awsee.completers_suggesters import *
from awsee.completers_suggesters import _request_confirm_y_n as confirm_y_n
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML as Prompt_HTML
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth

class RoleManager:

    def __init__(self):
        self.credentialsRepository = CredentialsRepository()
        self.roleRepository        = RoleRepository()

    def _list_profiles(self, list_only_with_role=False) -> Tuple[str,list,dict]:
        index            = 0
        sizeSeparator    = 120
        sizeLabelProfile = 18
        output           = ""
        output           += Style.GREEN + "-".ljust(sizeSeparator,"-") + "\n"
        output           += f" {Style.IBLUE}PROFILES:\n{Style.GREEN}"
        profiles          = []
        profile_dict      = {}
        for c in self.credentialsRepository.all():
            list_roles = self.roleRepository.searchByQuery(where('profile') == c['profile'])

            add_profile_to_list = True
            if list_only_with_role and len(list_roles) < 1:
                add_profile_to_list = False

            if add_profile_to_list:
                index    += 1
                profiles.append(c['profile'])
                pn        = c['profile'] + " ".rjust(sizeLabelProfile -len(c['profile']), " ")
                account   = c['account']
                profile_dict[c['profile']]            = {}
                profile_dict[c['profile']]['account'] = account
                line      = f"  {Style.IBLUE}{index:02d} -->{Style.GREEN} {pn} {Style.IBLUE}Account..:{Style.GREEN} {account}"
                labelRole = "Roles..: "
                roles     = ""
                profile_dict[c['profile']]['roles'] = []
                for idx, r in enumerate(list_roles):
                    if len(roles) > 1:
                        roles += "\n" + " ".ljust(len(Utils.removeCharsColors(line)) + len(labelRole) + 1," ")
                    roles += f"{Style.BLUE}{idx+1:02d}{Style.GREEN}-{r['role-arn']} {Style.BLUE}({r['role-name']})"
                    profile_dict[c['profile']]['roles'].append(r['role-name'])
                if len(roles) > 1:
                    roles = f"{Style.IBLUE}{labelRole}{Style.GREEN}{roles}{Style.GREEN}"
                output += line + f" {roles}\n"

        output += "-".ljust(sizeSeparator,"-")
        return output, profiles, profile_dict

    def _request_input_profile(self, profiles) -> str:
        message = [('class:green', f' {Emoticons.pin()} Profile - '),('class:green2','start typing'),('class:green',' or '),('class:green2','<TAB>'),('class:green','..: ')]
        session = PromptSession()
        toolbar = Prompt_HTML(f'{toolbar_margin}&#9001;{toolbar_key_style_open}TAB{toolbar_key_style_close}&#9002;<i>List Profiles</i>{toolbar_separator}{toolbar_default}')
        result  = session.prompt(message,style=Prompt_Style,completer=MyCustomCompleter(profiles),
                                 complete_while_typing=True,validate_while_typing=False,
                                 validator=MyValidator(profiles,"profile not valid!"),
                                 key_bindings=general_bindings,bottom_toolbar=toolbar,
                                 auto_suggest=MySuggestion(profiles),rprompt='<<<    Profile ',color_depth=ColorDepth.TRUE_COLOR)
        if result == "":
           return None
        if result not in profiles:
            Messages.showWarning(f"Profile \"{Style.IBLUE}{result}{Style.IGREEN}\" not found!")
            return None
        return result

    def _request_input_role_name(self, suggestion_list=None, my_validator_list=None) -> str:
        auto_suggest_list = ["dev","prod","admin","developer","production"]
        if suggestion_list:
            auto_suggest_list = suggestion_list

        my_completer = None
        if my_validator_list:
            my_completer = MyCustomCompleter(my_validator_list)
         
        message   = [('class:green', f' {Emoticons.pin()} Role Name........................: ')]
        session   = PromptSession()
        toolbar   = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
        role_name = session.prompt(message,style=Prompt_Style,complete_while_typing=True,validate_while_typing=True,
                                   validator=MyNegativeValidator([" "],"Role Name not valid!"),
                                   key_bindings=general_bindings,bottom_toolbar=toolbar,
                                   auto_suggest=MySuggestion(auto_suggest_list),
                                   completer=my_completer,
                                   lexer=PygmentsLexer(AwsArnLexer),rprompt='<<<  Role Name ',color_depth=ColorDepth.TRUE_COLOR)
        if role_name == "":
           return None                        
        spacesFound = re.search(" ",role_name)
        if spacesFound:
            Messages.showWarning(f"Invalid Role Name \"{Style.IBLUE}{role_name}{Style.IGREEN}\", spaces are not allowed")
            return None
        return role_name

    def _request_input_role_arn(self, profile, profile_dict: dict, auto_suggestion_enable=True, list_roles=None, role_name=None) -> str:
        list_suggest_role_arn = []
        suggest_role_arn      = 'arn:aws:iam::' + profile_dict[profile]['account'] + ":role/" if 'account' in profile_dict[profile] else ''
        list_suggest_role_arn.append(suggest_role_arn)

        if role_name:
            list_suggest_role_arn.append(suggest_role_arn + role_name)

        role_arn_completer = MyCustomCompleter(list_suggest_role_arn)
        if list_roles:
            role_arn_completer = MyCustomCompleter(list_roles)
        
        suggestion = None
        if auto_suggestion_enable:
            suggestion = MySuggestion(list_suggest_role_arn)

        message  = [('class:green', f' {Emoticons.pin()} Role Arn.........................: ')]
        session  = PromptSession()
        toolbar  = Prompt_HTML(f'{toolbar_margin}&#9001;{toolbar_key_style_open}TAB{toolbar_key_style_close}&#9002;<i>Suggest Role Arn</i>{toolbar_separator}{toolbar_default}')
        role_arn = session.prompt(message,style=Prompt_Style,complete_while_typing=True,validate_while_typing=False,
                                   validator=AwsArnValidator(),
                                   completer=role_arn_completer,
                                   key_bindings=general_bindings,bottom_toolbar=toolbar,
                                   lexer=PygmentsLexer(AwsArnLexer),
                                   auto_suggest=suggestion,rprompt='<<<   Role Arn ',color_depth=ColorDepth.TRUE_COLOR)
        if role_arn == "":
           return None                        
        spacesFound = re.search(" ",role_arn)
        if spacesFound:
            Messages.showWarning(f"Invalid Role Arn \"{Style.IBLUE}{role_arn}{Style.IGREEN}\", spaces are not allowed")
            return None
        try:
            arnparse(role_arn)
        except:
            Messages.showWarning(f"Invalid MFA Device \"{Style.IBLUE}{role_arn}{Style.IGREEN}\"")
            return None
        return role_arn

    def addRole(self):
        Messages.showMessage(f"{Style.IYELLOW}ADD{Style.GREEN} ROLE TO PROFILE")

        output, profiles, profile_dict = self._list_profiles(list_only_with_role=False)
        printPy(output)

        ### Profile
        profile = self._request_input_profile(profiles)
        if not profile or profile == "":
           return None

        ### Role Name
        role_name = self._request_input_role_name()
        if not role_name or role_name == "":
           return None

        ### Role Arn
        role_arn = self._request_input_role_arn(profile, profile_dict, role_name=role_name)
        if not role_arn or role_arn == "":
           return None

        output  = "\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{profile}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role Name..........: {Style.IBLUE}{role_name}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role ARN...........: {Style.IBLUE}{role_arn}{Style.RESET}\n"
        printPy(output)

        confirm = confirm_y_n()
        if confirm and confirm.lower() == "y":
            record = {
                "id": str(uuid.uuid4()),
                "profile": profile,
                "role-name": role_name,
                "role-arn": role_arn
            }
            self.roleRepository.insert(record)
            output = f"{Style.GREEN} {Emoticons.ok()} Saved!{Style.RESET}"
            printPy(output)
    
    def removeRole(self):
        Messages.showMessage(f"{Style.IYELLOW}REMOVE{Style.GREEN} ROLE")

        output, profiles, profile_dict = self._list_profiles(list_only_with_role=True)
        printPy(output)

        ### Profile
        profile = self._request_input_profile(profiles)
        if not profile or profile == "":
           return None
        
        ### Role
        list_roles = []
        for p in profile_dict:
            if p == profile and "roles" in profile_dict[p]:
                for role in profile_dict[p]["roles"]:
                    list_roles.append(role)
        if len(list_roles) < 1:
            list_roles = None
        role_name = self._request_input_role_name(suggestion_list=list_roles,my_validator_list=list_roles)
        if not role_name or role_name == "":
           return None
        
        roleToRemove = self.roleRepository.searchByQuery(
            (Query()['role-name'] == role_name) &
            (Query()['profile'] == profile)
        )
        roleToRemove = roleToRemove[0]
        
        output  = "\n"
        output += f"  {Emoticons.pointRight()} {Style.IYELLOW}Removing Role:\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{roleToRemove['profile']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role Name..........: {Style.IBLUE}{roleToRemove['role-name']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role ARN...........: {Style.IBLUE}{roleToRemove['role-arn']}{Style.RESET}\n"
        printPy(output)

        confirm = confirm_y_n()
        if confirm and confirm.lower() == "y":
            self.roleRepository.remove(Query().id == roleToRemove['id'])
            output  = "\n"
            output += f"{Style.GREEN} {Emoticons.ok()} Removed!{Style.RESET}"
            printPy(output)
    
    def listRoles(self, filterByProfile):
        listRoles = None
        if filterByProfile:
            listRoles = self.roleRepository.searchByQuery(where('profile') == filterByProfile)
        else:
            listRoles = self.roleRepository.all()

        if len(listRoles) < 1:
            if filterByProfile:
               msg = f"There's no role added to the profile {Style.IBLUE}{filterByProfile}{Style.RESET}"
            else:
               msg = f"There's no role added"
            Messages.showWarning(msg)
            return None
        
        activeRole = os.environ['AWS_ROLE'] if 'AWS_ROLE' in os.environ else None
        tableArgs = TableArgs()
        # Hightlight the current Role
        if activeRole:
           tableArgs.setArguments("| " + activeRole + " ")
        header = ["#","Profile","Role Name","Role ARN"]
        prettyTable = PrettyTable(header)
        for idx, r in enumerate(listRoles):
            columns = [ idx+1, r['profile'], r['role-name'], r['role-arn']]
            prettyTable.addRow(columns)
        prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
        prettyTable.ascendingOrder(not tableArgs.desc)
        output = "\n" + Style.RESET + prettyTable.printMe("listRoles",False,tableArgs)
        Messages.showMessage("ROLES", output)