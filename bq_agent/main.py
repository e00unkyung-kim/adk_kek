from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from bq_agent.agent import get_bigquery_agent

app = FastAPI()
root_agent = get_bigquery_agent()   # Agent 객체 생성 (중요)

###########################################################
# 1) 메인 페이지 (버튼 UI)
###########################################################
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>ADK Agent Service</title>
            <style>
                body { font-family: Arial; text-align: center; padding-top: 100px; background:#f8f8f8; }
                .btn {
                    padding: 15px 40px;
                    border-radius: 8px;
                    background: #4CAF50;
                    color: white;
                    text-decoration: none;
                    font-size: 20px;
                }
            </style>
        </head>
        <body>
            <h1>🤖 ADK BigQuery Agent Service</h1>
            <a class="btn" href="/ask-form">질문하러 가기</a>
        </body>
    </html>
    """


###########################################################
# 2) 질문 입력 폼 페이지
###########################################################
@app.get("/ask-form", response_class=HTMLResponse)
def ask_form():
    return """
    <html>
        <head>
            <title>Ask Agent</title>
            <style>
                body { font-family: Arial; padding-top:50px; text-align:center; background:#fbfbfb; }
                textarea { width: 60%; height: 120px; padding:10px; font-size:16px; }
                button {
                    margin-top: 20px;
                    padding:12px 30px;
                    background: #1976D2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size:18px;
                }
            </style>
        </head>
        <body>
            <h2>🤖 AD문제주면: 답변</h2>
            <form action="/ask" method="post">
                <textarea name="question" placeholder="여기에 질문을 입력하세요"></textarea><br>
                <button type="submit">질문 보내기</button>
            </form>
        </body>
    </html>
    """


###########################################################
# 3) /ask - Form(HTML) + JSON API 둘 다 처리
###########################################################
@app.post("/ask")
async def ask(question: str = Form(None), request: Request = None):
    # JSON body로 들어온 경우 처리
    if question is None:
        try:
            body = await request.json()
            question = body.get("question")
        except:
            return JSONResponse({"error": "question field missing"}, status_code=400)

    # Agent 실행
    answer = await root_agent.run(question)

    # 요청이 HTML Form일 경우 응답도 HTML로
    if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
        return HTMLResponse(f"""
        <html>
            <head>
                <title>Agent Response</title>
                <style>
                    body {{ font-family: Arial; background:#f5f5f5; padding:40px; }}
                    .card {{
                        background:white; padding:30px; border-radius:10px; 
                        max-width:600px; margin:auto; box-shadow:0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .answer {{ white-space: pre-wrap; font-size:18px; }}
                    a {{ display:inline-block; margin-top:20px; text-decoration:none; color:#1976D2; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>🤖 Agent 답변</h2>
                    <div class="answer">{answer}</div>
                    <a href="/ask-form">← 다시 질문하기</a>
                </div>
            </body>
        </html>
        """)

    # JSON API 요청일 경우 JSON으로 응답
    return {"answer": answer}

