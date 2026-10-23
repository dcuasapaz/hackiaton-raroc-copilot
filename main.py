from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.copilot_agent import run_raroc_analysis

app = FastAPI(title="SmartRAROC API", version="1.0")

class ClientRequest(BaseModel):
    cif: int

@app.post("/api/v1/analyze")
def analyze_client(req: ClientRequest):
    metrics, analysis = run_raroc_analysis(req.cif)
    if "error" in metrics:
        raise HTTPException(status_code=404, detail=metrics["error"])
    return {
        "status": "success",
        "metrics": metrics,
        "ai_analysis": analysis
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)