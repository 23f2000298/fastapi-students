from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    data = df
    if class_:
        data = df[df["class"].isin(class_)]
    return {"students": data.to_dict(orient="records")}

class SentimentRequest(BaseModel):
    sentences: List[str]

def get_sentiment(text: str) -> str:
    positive = ["love","great","excellent","amazing","good","happy","best","wonderful","fantastic","awesome"]
    negative = ["hate","terrible","awful","bad","worst","sad","horrible","poor","disappointing","ugly"]
    text_lower = text.lower()
    if any(w in text_lower for w in positive):
        return "happy"
    elif any(w in text_lower for w in negative):
        return "sad"
    return "neutral"

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    results = [{"sentence": s, "sentiment": get_sentiment(s)} for s in req.sentences]
    return {"results": results}

DATA = [
  {"region":"apac","latency_ms":190.43,"uptime_pct":99.376},
  {"region":"apac","latency_ms":196.34,"uptime_pct":97.62},
  {"region":"apac","latency_ms":209.22,"uptime_pct":98.894},
  {"region":"apac","latency_ms":201.7,"uptime_pct":98.168},
  {"region":"apac","latency_ms":111.06,"uptime_pct":97.949},
  {"region":"apac","latency_ms":183.08,"uptime_pct":98.379},
  {"region":"apac","latency_ms":227.78,"uptime_pct":99.465},
  {"region":"apac","latency_ms":217.51,"uptime_pct":98.201},
  {"region":"apac","latency_ms":174.97,"uptime_pct":98.903},
  {"region":"apac","latency_ms":116.21,"uptime_pct":97.18},
  {"region":"apac","latency_ms":150.37,"uptime_pct":99.467},
  {"region":"apac","latency_ms":114.92,"uptime_pct":99.211},
  {"region":"emea","latency_ms":123.01,"uptime_pct":99.347},
  {"region":"emea","latency_ms":192.74,"uptime_pct":98.735},
  {"region":"emea","latency_ms":233.02,"uptime_pct":97.964},
  {"region":"emea","latency_ms":107.27,"uptime_pct":98.974},
  {"region":"emea","latency_ms":116.31,"uptime_pct":99.1},
  {"region":"emea","latency_ms":152.3,"uptime_pct":97.839},
  {"region":"emea","latency_ms":198.34,"uptime_pct":98.74},
  {"region":"emea","latency_ms":157.06,"uptime_pct":98.405},
  {"region":"emea","latency_ms":204.57,"uptime_pct":97.126},
  {"region":"emea","latency_ms":224.28,"uptime_pct":97.961},
  {"region":"emea","latency_ms":146.31,"uptime_pct":98.891},
  {"region":"emea","latency_ms":151.56,"uptime_pct":99.092},
  {"region":"amer","latency_ms":226.58,"uptime_pct":99.238},
  {"region":"amer","latency_ms":129.22,"uptime_pct":98.802},
  {"region":"amer","latency_ms":114.74,"uptime_pct":98.876},
  {"region":"amer","latency_ms":150.26,"uptime_pct":97.226},
  {"region":"amer","latency_ms":124.88,"uptime_pct":98.518},
  {"region":"amer","latency_ms":222.45,"uptime_pct":99.5},
  {"region":"amer","latency_ms":149.16,"uptime_pct":99.437},
  {"region":"amer","latency_ms":157.35,"uptime_pct":98.325},
  {"region":"amer","latency_ms":134.84,"uptime_pct":99.035},
  {"region":"amer","latency_ms":146.25,"uptime_pct":97.299},
  {"region":"amer","latency_ms":105.19,"uptime_pct":97.178},
  {"region":"amer","latency_ms":182.0,"uptime_pct":98.808}
]

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/latency")
async def latency(req: LatencyRequest):
    result = {}
    for region in req.regions:
        records = [r for r in DATA if r["region"] == region]
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes), ), 4),
            "breaches": int(sum(1 for l in latencies if l > req.threshold_ms))
        }
    return result
