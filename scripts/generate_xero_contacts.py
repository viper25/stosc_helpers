""" 
Generate Xero Contacts File that contains mapping of Xero contactID to memberID for 
future easy lookup
"""
import tomllib
from utils import utils
# https://github.com/CodeForeverAndEver/ColorIt
from colorama import init, Fore
import pandas as pd
import logging

init(autoreset=True)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def _get_Xero_Contacts():
    has_more_pages = True
    page = 0
    contacts = []
    _contacts = {}
    # Go through pages (100 per page)
    while has_more_pages:
        page += 1
        print(f"{Fore.YELLOW}  Processing Page {page} of contacts...")
        url = f'https://api.xero.com/api.xro/2.0/Contacts?summaryOnly=True&page={page}'
        xero_contacts = utils.xero_get(url)
        if len(xero_contacts["Contacts"]) == 0:
            has_more_pages = False
        else:
            _contacts = [
                {
                    "memberCode": _contact['AccountNumber'],
                    "Name": _contact['FirstName'] + ' ' + _contact['LastName'] if 'LastName' in _contact else '',
                    "ContactID": _contact['ContactID']
                }
                for _contact in xero_contacts['Contacts']
                if (
                        'AccountNumber' in _contact
                        # Exclude other contacts who have account numbers
                        and len(_contact['AccountNumber']) == 4
                        and _contact['ContactStatus'] == 'ACTIVE'
                )
            ]
            contacts.extend(_contacts)
    return contacts


def generate_xero_contact_list(save_file_path: str = config['gb_eligibility']['FILE_ELIGIBLE_GB_MEMBERS']):
    # TODO: Ask for path to save CSV file
    print(f"{Fore.WHITE}Getting Member List...")
    list_Contacts = _get_Xero_Contacts()
    print(f"{Fore.YELLOW}Retrieved {Fore.GREEN}{len(list_Contacts)}{Fore.YELLOW} members. Sample Listing:")
    df_contacts = pd.DataFrame(list_Contacts)
    print(f"{Fore.BLUE}{df_contacts.head(2)}\n")
    df_contacts.sort_values(by=['memberCode']).to_csv(save_file_path, index=False)
    print(f"{Fore.WHITE}Written to {save_file_path}")
    return save_file_path


if __name__ == '__main__':
    _ = generate_xero_contact_list()
