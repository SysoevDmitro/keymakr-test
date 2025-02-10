import os
import json
import re
from typing import List, Optional
from .celery_app import celery_app
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from celery.result import AsyncResult

from .tasks import process_weather_task

app = FastAPI(title="Weather API")


class Weather(BaseModel):
    cities: List[str] = Field(..., description="List of city names")

    @validator("cities", each_item=True)
    def city_names(cls, v):
        pattern = re.compile(r'^[A-Za-zА-Яа-яЁё\s-]+$')
        if not pattern.match(v):
            raise ValueError("Invalid city name")
        return v


@app.post("/weather")
async def weather(request: Weather):
    task = process_weather_task.delay(request.cities)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
async def task_status(task_id: str):
    result = AsyncResult(task_id)
    status = result.status

    if status == "SUCCESS":
        return {
            "status": "completed",
            "results": result.get()  # Получаем JSON с погодой
        }
    elif status == "FAILURE":
        return {
            "status": "failed",
            "error_message": str(result.result),  # Подробности ошибки
            "traceback": result.traceback
        }
    else:
        return {"status": status}


@app.get("/results/{region}")
async def result(region: str, task_id: Optional[str] = None):
    if task_id:
        file_path = os.path.join("weather_data", region, f"task_{task_id}.json")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Result file not found")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        results_dir = os.path.join("weather_data", region)
        if not os.path.exists(results_dir):
            raise HTTPException(status_code=404, detail="Region not found")
        aggregated = []
        for file_name in os.listdir(results_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(results_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    aggregated.extend(data)
        return aggregated
