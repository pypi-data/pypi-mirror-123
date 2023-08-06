
import re, uuid
from typing import Dict, Tuple
from tinydb import Query, where
from arnparse import arnparse
from awsee.messages import Messages
from awsee.style import Style
from awsee.emoticons import Emoticons
from awsee.utils import Utils
from awsee.tableargs import TableArgs
from awsee.prettytable import PrettyTable
from awsee.repository import CredentialsRepository, MfaRepository
from awsee.general import *

from awsee.completers_suggesters import *
from awsee.completers_suggesters import _request_confirm_y_n as confirm_y_n
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML as Prompt_HTML
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth

class MFAManager:

    def __init__(self):
        self.credentialsRepository = CredentialsRepository()
        self.mfaRepository         = MfaRepository()

    def _list_profiles(self, list_only_with_mfa=False) -> Tuple[str,list,dict]:
        index            = 0
        sizeSeparator    = 120
        sizeLabelProfile = 18
        output           = ""
        output           += Style.GREEN + "-".ljust(sizeSeparator,"-") + "\n"
        output           += f" {Style.IBLUE}MFA DEVICES:\n{Style.GREEN}"
        profiles          = []
        profile_dict      = {}
        for c in self.credentialsRepository.all():
            list_mfas  = self.mfaRepository.searchByQuery(where('profile') == c['profile'])

            add_profile_to_list = True
            if list_only_with_mfa and len(list_mfas) < 1:
                add_profile_to_list = False

            if add_profile_to_list:
                index     += 1
                pn         = c['profile'] + " ".rjust(sizeLabelProfile -len(c['profile']), " ")
                account    = c['account']
                profiles.append(c['profile'])
                profile_dict[c['profile']] = {}
                profile_dict[c['profile']]['account'] = account
                line       = f"  {Style.IBLUE}{index:02d} -->{Style.GREEN} {pn} {Style.IBLUE}Account..:{Style.GREEN} {account}"
                labelMfa   = "MFA Devices..: "
                mfaDevices = ""
                profile_dict[c['profile']]['mfa-devices'] = []
                for idx, r in enumerate(list_mfas):
                    if len(mfaDevices) > 1:
                        mfaDevices += "\n" + " ".ljust(len(Utils.removeCharsColors(line)) + len(labelMfa) + 1," ")
                    mfaDevices += f"{Style.BLUE}{idx+1:02d}{Style.GREEN}-{r['mfa-device']}"
                    profile_dict[c['profile']]['mfa-devices'].append(r['mfa-device'])
                if len(mfaDevices) > 1:
                    mfaDevices = f"{Style.IBLUE}{labelMfa}{Style.GREEN}{mfaDevices}{Style.GREEN}"
                output += line + f" {mfaDevices}\n"

        output += "-".ljust(sizeSeparator,"-")
        return output, profiles, profile_dict

    def _request_input_profile(self, profiles) -> str:
        message = [('class:green', f' {Emoticons.pin()} Profile - '),('class:green2','start typing'),('class:green',' or '),('class:green2','<TAB>'),('class:green','....: ')]
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

    def _request_input_mfa_device(self, profile, profile_dict: dict, auto_suggestion_enable=True, list_mfas=None) -> str:
        suggest_mfa   = 'arn:aws:iam::'
        suggest_mfa  += profile_dict[profile]['account'] + ":mfa/" if 'account' in profile_dict[profile] else ''

        mfa_completer = MyCustomCompleter([suggest_mfa])
        if list_mfas:
            mfa_completer = MyCustomCompleter(list_mfas)
        
        suggestion = None
        if auto_suggestion_enable:
            suggestion = MySuggestion([suggest_mfa])

        message   = [('class:green', f' {Emoticons.pin()} MFA Device.........................: ')]
        session   = PromptSession()
        toolbar   = Prompt_HTML(f'{toolbar_margin}&#9001;{toolbar_key_style_open}TAB{toolbar_key_style_close}&#9002;<i>Suggest MFA Device</i>{toolbar_separator}{toolbar_default}')
        mfaDevice = session.prompt(message,style=Prompt_Style,complete_while_typing=True,validate_while_typing=False,
                                   validator=AwsArnValidator(),
                                   completer=mfa_completer,
                                   key_bindings=general_bindings,bottom_toolbar=toolbar,
                                   lexer=PygmentsLexer(AwsArnLexer),
                                   auto_suggest=suggestion,rprompt='<<< MFA Device ',color_depth=ColorDepth.TRUE_COLOR)
        if mfaDevice == "":
           return None                        
        spacesFound = re.search(" ",mfaDevice)
        if spacesFound:
            Messages.showWarning(f"Invalid MFA Device \"{Style.IBLUE}{mfaDevice}{Style.IGREEN}\", spaces are not allowed")
            return None
        try:
            arnparse(mfaDevice)
        except:
            Messages.showWarning(f"Invalid MFA Device \"{Style.IBLUE}{mfaDevice}{Style.IGREEN}\"")
            return None
        return mfaDevice
    
    def _request_input_user_name(self,suggest_username):
        message   = [('class:green', f' {Emoticons.pin()} User Name..........................: ')]
        session   = PromptSession()
        toolbar   = Prompt_HTML(f'{toolbar_margin}&#9001;{toolbar_key_style_open}TAB{toolbar_key_style_close}&#9002;<i>Suggest User Name</i>{toolbar_separator}{toolbar_default}')
        user_name = session.prompt(message,style=Prompt_Style,complete_while_typing=True,validate_while_typing=False,
                                   completer=MyCustomCompleter([suggest_username]),
                                   key_bindings=general_bindings,bottom_toolbar=toolbar,
                                   auto_suggest=MySuggestion([suggest_username]),rprompt='<<<  User Name ',color_depth=ColorDepth.TRUE_COLOR)
        if user_name == "":
           return None                        
        spacesFound = re.search(" ",user_name)
        if spacesFound:
            Messages.showWarning(f"Invalid User Name \"{Style.IBLUE}{user_name}{Style.IGREEN}\", spaces are not allowed")
            return None
        return user_name

    def addMfa(self):
        Messages.showMessage(f"{Style.IYELLOW}ADD{Style.GREEN} MFA DEVICE TO PROFILE")
        
        output, profiles, profile_dict = self._list_profiles()
        printPy(output)

        ### Profile
        profile = self._request_input_profile(profiles)
        if not profile or profile == "":
           return None

        ### MFA Device
        mfaDevice = self._request_input_mfa_device(profile, profile_dict)
        if not mfaDevice or mfaDevice == "":
           return None                        

        ### User Name
        #'<<<  User Name '
        search_mfa_name  = ":mfa/"
        index_mfa_name   = mfaDevice.index(search_mfa_name) if search_mfa_name in mfaDevice else None
        sugges_user_name = ""
        if index_mfa_name: 
           sugges_user_name = mfaDevice[index_mfa_name:].replace(search_mfa_name,"")
        userName = self._request_input_user_name(sugges_user_name)
        if not userName or userName == "":
            return None

        output  = "\n"
        output += f"  {Emoticons.pointRight()} {Style.IYELLOW}Adding MFA Device to Profile:\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{profile}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}MFA Device.........: {Style.IBLUE}{mfaDevice}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}User Name..........: {Style.IBLUE}{userName}{Style.RESET}\n"
        printPy(output)

        confirm = confirm_y_n()
        if confirm and confirm.lower() == "y":
            record = {
                "id": str(uuid.uuid4()),
                "profile": profile,
                "mfa-device": mfaDevice,
                "user-name": userName
            }
            self.mfaRepository.insert(record)
            output = f"{Style.GREEN} {Emoticons.ok()} Saved!{Style.RESET}"
            printPy(output)
    
    def removeMFADevice(self):
        Messages.showMessage(f"{Style.IYELLOW}REMOVE{Style.GREEN} MFA DEVICE")
        
        output, profiles, profile_dict = self._list_profiles(list_only_with_mfa=True)
        printPy(output)

        ### Profile
        profile = self._request_input_profile(profiles)
        if not profile or profile == "":
           return None
        
        ### MFA Device
        list_mfas = []
        for p in profile_dict:
            if p == profile  and "mfa-devices" in profile_dict[p]:
                for mfa_device in profile_dict[p]["mfa-devices"]:
                    list_mfas.append(mfa_device)
        if len(list_mfas) < 1:
            list_mfas = None
        mfaDevice = self._request_input_mfa_device(profile, profile_dict, auto_suggestion_enable=True, list_mfas=list_mfas)
        if not mfaDevice or mfaDevice == "":
           return None 

        result_query = self.mfaRepository.searchByQuery(Query().profile == profile and Query()["mfa-device"] == mfaDevice)
        if len(result_query) == 0:
            Messages.showWarning(f"MFA Device {Style.IYELLOW}{mfaDevice}{Style.GREEN} for profile {Style.IYELLOW}{profile}{Style.GREEN}, was not found!")
            return None
        if len(result_query) > 1:
            Messages.showWarning(f"Ops... something is wrong! More than one MFA Device was listed!")
            output = ""
            for m in result_query:
                output += f"  --> {result_query['mfa-device']}\n"
            printPy(output)
            return None

        mfa_device_found = result_query[0]

        output  = "\n"
        output += f"  {Emoticons.pointRight()} {Style.IYELLOW}Removing MFA Device:\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{mfa_device_found['profile']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}MFA Device.........: {Style.IBLUE}{mfa_device_found['mfa-device']}{Style.RESET}\n"
        printPy(output)

        confirm = confirm_y_n()
        if confirm and confirm.lower() == "y":
            self.mfaRepository.remove(Query().id == mfa_device_found['id'])
            output  = "\n"
            output += f"{Style.GREEN} {Emoticons.ok()} Removed!{Style.RESET}"
            printPy(output)

    def _list_mfa_devices(self, filterByProfile):
        listmfaDevices = None
        if filterByProfile:
            listmfaDevices = self.mfaRepository.searchByQuery(where('profile') == filterByProfile)
        else:
            listmfaDevices = self.mfaRepository.all()

        if len(listmfaDevices) < 1:
            if filterByProfile:
               msg = f"There's no MFA Device added to the profile {Style.IBLUE}{filterByProfile}{Style.RESET}"
            else:
               msg = f"There's no MFA Device added" 
            Messages.showWarning(msg)
            return None
        
        tableArgs = TableArgs()
        header = ["#","Profile","MFA Device", "User Name"]
        prettyTable = PrettyTable(header)
        for idx, r in enumerate(listmfaDevices):
            columns = [ idx+1, r['profile'], r['mfa-device'], r['user-name']]
            prettyTable.addRow(columns)
        prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
        prettyTable.ascendingOrder(not tableArgs.desc)
        output = "\n" + Style.RESET + prettyTable.printMe("listMfaDevices",False,tableArgs)
        return output

    def listmfaDevices(self, filterByProfile):
        output = self._list_mfa_devices(filterByProfile)
        if output:
           Messages.showMessage("MFA Devices", output)