from flask import Flask
import pandas as pd
import time
from datetime import datetime
from drive_functions import *
from scraping_functions import *
from embedding_functions import *

app = Flask(__name__)


def run_script():
    # Get the result number that we're currently on so we can take off from there:
    print("Process started")
    overall_start = datetime.now()
    folder_id = "1rO51gcWxs7St3r0_pWIDb2bOuwQFZsU8"
    max_number = get_max_file_number(folder_id)
    print("Max number obtained:", max_number)
    lim = max_number + 100
    start = max_number
    df = pd.read_csv("Past NOW CFO Clients  - Current_and_Former_NowCFO_Clients.csv")
    df = df[start:lim].reset_index().drop(columns=["index", "Unnamed: 0"])
    names_list = df["Business_Name"].to_list()
    linkedin_url_list = []

    # Get the LinkedIn URLS for each company:
    error_count = 0
    try:
        for q, name in enumerate(names_list):
            l_url = get_linkedin_url(name)
            linkedin_url_list.append(l_url)
            time.sleep(1)
            if error_count > 5:
                break
    except Exception as e:
        error_count += 1
    print("LI URLs done in time:", datetime.now()- overall_start)

    linkedin_urls = pd.DataFrame({"Business_LinkedIn_URL":linkedin_url_list})
    l=len(linkedin_urls)
    new_df = pd.concat([df[:l], linkedin_urls], axis=1)
    company_data_list = []

    # Now get the company info from the LinkedIN URLs
    for i in linkedin_urls["Business_LinkedIn_URL"]:
        if i != "":
            company_data = get_company_linkedin_data(i)
            company_data_list.append(company_data)
        else:
            company_data_list.append({})

    print("Company data done in time:", datetime.now()- overall_start)

    new_df = get_decision_makers(new_df, company_data_list)

    print("Decision makers done in time:", datetime.now()- overall_start)
    # Save and upload the csv
    upload_file_name = f"results_{str(lim)}.csv"
    new_df.to_csv(upload_file_name)
    drive_upload(upload_file_name, folder_id)
    print("Latency:", datetime.now() - overall_start)


    return "Upload script executed!", 200

if __name__ == '__main__':
    run_script()
