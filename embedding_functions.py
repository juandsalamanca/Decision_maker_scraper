from openai import AzureOpenAI
import numpy as np
from sklearn.metrics import mean_squared_error
import json

openai_client = AzureOpenAI(api_key="db14efc60e704372abe4416b6ba048e1",  api_version="2024-02-01", azure_endpoint = "https://azo-iknow-ku-01.openai.azure.com/")

def get_embedding(text):
  response = openai_client.embeddings.create(
      input = text,
      model= "text-embedding-3-large"
  )
  json_object = json.loads(response.model_dump_json(indent=2))
  return json_object["data"][0]["embedding"]



def get_decision_makers(new_df, company_data_list):
    positions = ["CEO", "CFO", "COO", "Chief Officer", "President", "VP", "Director", "Board Member", "Chairman", "Principal", "Executive"]
    embedded_positions = np.load("position_embeddings.npy")
    decision_makers = []
    no_decision_makers = []
    empl_position_embeddings = []
    for j, item in enumerate(company_data_list):
        company_decision_makers = []
        new_df.loc[j, "Decision Makers"] = ""
        new_df.loc[j, "LinkedIn Address"] = ""
        if item and "employees" in item:

            for employee in item["employees"]:
                empl_name = employee["employee_name"]
                empl_position = employee["employee_position"]
                empl_url = employee["employee_profile_url"]

                position_embedding = get_embedding(empl_position)
                empl_position_embeddings.append(position_embedding)
                switch = 0
                employee["MSE"] = []
                employee["Match"] = []
                for i, embedding in enumerate(embedded_positions):

                    mse = mean_squared_error(embedding, position_embedding)
                    employee["MSE"].append(mse)
                    if mse < 3.8e-4:
                        switch = 1
                        employee["Match"].append([positions[i], mse])

                if switch == 1:
                    decision_makers.append(employee)
                    company_decision_makers.append(employee)
                    new_df.loc[j, "Decision Makers"] += f" ({empl_name}, {empl_position})"
                    new_df.loc[j, "LinkedIn Address"] += f" {empl_url}"

                else:
                    no_decision_makers.append(employee)

    return new_df
