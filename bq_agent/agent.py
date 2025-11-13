# agent.py
from google.adk.agents import Agent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
import google.auth
import dotenv

dotenv.load_dotenv()

# 1) Application Default Credentials 사용 (서비스 계정/로컬 둘 다 가능)
credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)

# 2) BigQuery Toolset 생성
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config
    # 필요하면 config 더 넣을 수 있음 (write_mode 등)
)

# 3) 에이전트 정의
root_agent = Agent(
    model="gemini-2.5-flash",           # adk create 할 때 선택했던 모델로 맞추기
    name="my_project_bigquery_agent",
    description="NL2SQL agent for my project's BigQuery data.",
    instruction=(
        "You have to say hello to user by talking your role"
        "You're role is a BigQuery analysis agent. "
        "The user will ask questions in natural language. "
        "You must generate a valid BigQuery SQL query, run it using the BigQuery tool, "
        "and then explain the results in Korean in a friendly way. also give the query "
        "If the question is ambiguous, ask a clarification question."
        "You can use project id : bananacode-kek"
    ),
    tools=[bigquery_toolset],           # 🔥 더 이상 google_search 없음
)

def get_bigquery_agent():
    return root_agent

