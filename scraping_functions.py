import requests
from apify_client import ApifyClient


# Replace with your actual API Key and Search Engine ID
API_KEY = "search_engine_api_key"
CX = "search_engine_id"

def get_linkedin_url(company_name):
    """
    Uses Google Custom Search API to find the LinkedIn company URL.
    """
    query = f"{company_name} site:linkedin.com/company"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

    try:
        response = requests.get(url)
        data = response.json()

        # Extract the first result URL
        if "items" in data:
            return data["items"][0]["link"]
        else:
            #print("[-] No results found")
            return None

    except Exception as e:
        print(f"[-] Error fetching LinkedIn URL: {e}")
        return None
    

ApifyKey='apify_api_znMc9b2OhMyPdUzfPLeMVsGQR25kIG1QQBin'
appify_client = ApifyClient(ApifyKey)

def get_company_linkedin_data(linkedin_url):
    run_input = {
        "proxy": {
            "useApifyProxy": True
        },
        "urls": [linkedin_url]
    }
    actor_call = appify_client.actor("sanjeta/linkedin-company-profile-scraper").call(run_input=run_input)
    res=[]
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in appify_client.dataset(actor_call["defaultDatasetId"]).iterate_items():
        return item
