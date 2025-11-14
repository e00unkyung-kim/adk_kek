from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
import google.auth
import dotenv

dotenv.load_dotenv()

credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config
)

root_agent = Agent(
    model="gemini-2.0-flash",   
    name="my_project_bigquery_agent",
    description="NL2SQL agent for my project's BigQuery data.",
    instruction=(
        "You have to say hello to user by talking your role. "
        "You're role is a BigQuery analysis agent. "
        "The user will ask questions in natural language. "
        "You must generate a valid BigQuery SQL query, run it using the BigQuery tool, "
        "and then explain the results in Korean in a friendly way. "
        "Also give the query. "
        "If the question is ambiguous, ask a clarification question. "
        "You can use project id : bananacode-kek"
    ),
    tools=[bigquery_toolset],
)

def get_bigquery_agent():
    return root_agent

