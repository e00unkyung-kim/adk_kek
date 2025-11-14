from fastapi import FastAPI
from bq_agent.agent import get_bigquery_agent as root_agent

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(question: str):
    answer = await root_agent.run(question)
    return {"answer": answer}

