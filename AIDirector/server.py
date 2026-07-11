import json
from fastapi import FastAPI, WebSocket

app = FastAPI()

def make_decision(metrics):
    times_caught = metrics.get("timesCaught", 0)
    min_distance = metrics.get("minDistance", 999)
    chase_time = metrics.get("chaseTime", 0)
    session_duration = metrics.get("sessionDuration", 1)
    print(f"DEBUG: caught={times_caught}, dist={min_distance}")

    if times_caught >= 3 and min_distance < 1.5:
        return "Arena Expanded"  

    if times_caught >= 2 and min_distance < 2.0:
        return "Enemy Slowed"      

    if min_distance < 1.5:
        return "Enemy Slowed"

    chase_ratio = chase_time / session_duration
    if times_caught == 0 and chase_ratio < 0.3:
        return "Enemy Accelerated"
    
    return "Monitoring..."

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Unity connected!")

    try:
        while True:
            data = await websocket.receive_text()
            metrics = json.loads(data)
            print(f"Incoming data: {metrics}")

            command = make_decision(metrics)
            print(f"Decision: {command}")
            await websocket.send_text(command)

    except Exception as e:
        print(f"Connection closed: {e}")