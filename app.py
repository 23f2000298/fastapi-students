from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    data = df
    if class_:
        data = df[df["class"].isin(class_)]
    return {"students": data.to_dict(orient="records")}
