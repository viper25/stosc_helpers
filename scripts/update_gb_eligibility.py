"""
Generate and Update GB eligible members.

As of GB Date if they have dues of > 6 months (from the date of the GB) they are not eligible

Let’s say annual subscription is $600 and if the member has paid $300 which is equal to 6 months. So in Sept, (Month 9)
he doesn't have 6 months of outstanding; only July - Sept (3 months) hence the member is eligible.

The invoices are checked to see if they were modified at the beginning of this year (as they should be when creating new
invoices after Jan 1). If this check is not there, in Xero, we will get all invoices from years past.

Principle: Loop through all members. For each member, check each invoice. Set eligibility to False and prove it's True
by checking invoices. The moment you can prove eligibility is False, break the loop and check the next member.
"""
import datetime

from scripts import generate_xero_contacts
from utils import utils

# https://github.com/CodeForeverAndEver/ColorIt
from colorit import *
import pandas as pd
from datetime import date, datetime
from dateutil import relativedelta
from utils import db
import tomllib

all_members = []
# For all invoices Updated after since_date i.e. created this year
since_date = datetime.now().strftime("%Y-01-01T00:00:00")
# Next year's invoices are created sometime in Dec the previous year
since_date = f"str{datetime.now().year}-12-01T00:00:00"

# INV-21
INVOICE_YEAR = f"INV-{str(date.today().year)[2:]}"
# Initialize the Set that shows members who have changed their GB status
MEMBERS_STATUS_CHANGE_ELIGIBLE = set()
MEMBERS_STATUS_CHANGE_INELIGIBLE = set()
init_colorit()


def update_CRM(m, e):
    db.update_gb_eligibility(m, e, MEMBERS_STATUS_CHANGE_ELIGIBLE, MEMBERS_STATUS_CHANGE_INELIGIBLE)


def process_eligible_GB_members(save_file: str, update_db_flag: bool = False) -> list:
    member_list_file_path = generate_xero_contacts.generate_xero_contact_list()
    # Loop through all members
    with open(member_list_file_path, "r") as f:
        for line in f:
            eligibility = False
            line = line.strip()
            if line.startswith("memberCode"):
                continue
            if line:
                memberCode, Name, contactID = line.split(",")
                if memberCode in EXLUSION_LIST:
                    continue
                print(color(f"Processing {Name} ({memberCode})", Colors.blue))
                invoices = utils.get_Invoices(contactID)
                if invoices["Invoices"]:
                    subscription_invoices = list(
                        filter(lambda x: x['InvoiceNumber'].startswith('INV-'), invoices["Invoices"]))
                    # Sorted in ascending order (2022, 2023 etc.)
                    subscription_invoices_sorted = sorted(subscription_invoices, key=lambda x: x['InvoiceNumber'])
                    for invoice in subscription_invoices_sorted:
                        print(color(
                            f"\t   {invoice['InvoiceNumber']}: {invoice['Status']}. Due: ${invoice['AmountDue']}. Total: ${invoice['Total']}",
                            Colors.white))
                        # If latest years subscription has been paid then he's considered eligible.
                        if invoice["InvoiceNumber"].startswith(INVOICE_YEAR) and invoice["Status"] == "PAID":
                            eligibility = True
                            print(color(f"\t{Name} ({memberCode}) is Eligible", Colors.green))
                            break
                        if invoice["Status"] == "PAID":
                            continue
                        elif invoice["Status"] == "AUTHORISED":
                            # Check year
                            year_of_invoice = int("20" + invoice["InvoiceNumber"].split("-")[1])
                            per_month_dues = invoice["Total"] / 12
                            months_paid_for = invoice["AmountPaid"] / per_month_dues
                            if months_paid_for != 0:
                                date_paid_till = datetime.strptime(f"{int(months_paid_for)} 1 {year_of_invoice}",
                                                                   "%m %d %Y")
                                # r interval of time dues haven't been paid for as of GB date. If this is > 6 months, he's not eligible
                                r = relativedelta.relativedelta(date_paid_till, DATE_OF_GB_ELIGIBILITY_CHECK)
                                days_diff_bw_last_payment_and_gb_date = r.months * 30 + r.years * 12 * 30 + r.days
                                if days_diff_bw_last_payment_and_gb_date > -180:
                                    eligibility = True
                                    print(color(f"\tSetting {Name} ({memberCode}) Eligible", Colors.green))
                                else:
                                    eligibility = False
                                    print(color(f"\t{Name} ({memberCode}) is Ineligible", Colors.red))
                                    break
                            # Has not paid in the prior year, Not eligible. No need to check further.
                            elif year_of_invoice < datetime.now().year and months_paid_for == 0:
                                eligibility = False
                                print(color(f"\tSetting {Name} ({memberCode}) Ineligible", Colors.red))
                                break
                            # Not yet paid for this year. Set to eligibility = True and check previous year invoices
                            # where if not paid, it'll be reset to False.
                            # If the invoice being checked is for the current year, but it's not 6 months yet, he is toggle to eligibile
                            elif year_of_invoice == datetime.now().year and datetime.now().month <= 6:
                                eligibility = True
                                print(color(f"\tSetting {Name} ({memberCode}) Eligible", Colors.green))

            all_members.append({"MemberCode": memberCode, "Name": Name, "Eligibility": eligibility})
            if update_db_flag:
                update_CRM(memberCode, eligibility)

    save_to_file(all_members, save_file)

    # Return success code
    return [MEMBERS_STATUS_CHANGE_ELIGIBLE, MEMBERS_STATUS_CHANGE_INELIGIBLE]


def save_to_file(members, save_file: str):
    df = pd.DataFrame(members)
    df.to_csv(save_file, index=False)
    print(f"\n⛔ Members who became ineligible: {MEMBERS_STATUS_CHANGE_INELIGIBLE}")
    print(f"✅ Members who became eligible: {MEMBERS_STATUS_CHANGE_ELIGIBLE}")
    print("DONE")


if __name__ == "__main__":
    # Load config
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    # Date to compare against. This should be the date of GB announcement
    DATE_OF_GB_ELIGIBILITY_CHECK = datetime.strptime(config['gb_eligibility']['DATE_OF_GB_ELIGIBILITY_CHECK_STR'],
                                                     '%d-%m-%Y %I:%M%p')
    EXLUSION_LIST = config['gb_eligibility']['EXLUSION_LIST']

    eligibility_lists = process_eligible_GB_members(
        member_list_file_path=config['gb_eligibility']['FILE_MEMBERS'],
        update_db_flag=config['gb_eligibility']['UPDATE_CRM_DB'],
        save_file=config['gb_eligibility']['FILE_ELIGIBLE_GB_MEMBERS']
    )
