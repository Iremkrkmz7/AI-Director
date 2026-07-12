# 🧠 AI Director — Dynamic Difficulty System for Unity
 
A technical prototype that demonstrates a **real-time AI Director system** built on top of an existing Unity game. The AI Director runs on a Python backend, analyzes player performance metrics every 2 seconds, and sends commands back to Unity to dynamically adjust game difficulty.
 
> Inspired by Left 4 Dead's AI Director system.
 
---
 
## 🎮 Demo
 
<img width="1018" height="683" alt="Animation" src="https://github.com/user-attachments/assets/689fae37-0fb6-4bf9-a06a-55799d006e98" />
---
 
## 🏗️ Architecture
 
```
Unity (C#)                        Python (FastAPI + WebSocket)
──────────────────                ────────────────────────────
DirectorMetrics.cs   ──────────▶  Receive player snapshot (JSON)
  │ Collects:                            │
  │ - Times caught by enemy              ▼
  │ - Time spent in chase          make_decision()
  │ - Min distance to enemy              │
  │ - Coins collected                    ▼
  │ - Session duration        ◀──  Send command back
  │
  ▼
DirectorClient.cs (WebSocket)
  │
  ▼
DirectorCommandHandler.cs
  │
  ├── "Enemy Slowed"    → NPC.agent.speed *= 0.5
  ├── "Enemy Accelerated" → NPC.agent.speed *= 1.5
  └── "Arena Expanded"  → next level planeSize += 5f
```
 
---
 
## ⚙️ How It Works
 
Every 2 seconds, Unity sends a JSON snapshot of the player's current performance to the Python server:
 
```json
{
  "timesCaught": 3,
  "chaseTime": 48.3,
  "minDistance": 1.18,
  "coins": 6,
  "sessionDuration": 24.0
}
```
 
The Python server runs a decision function and returns one of three commands:
 
| Condition | Command | Effect |
|---|---|---|
| Caught ≥ 3 times & distance < 1.5 | `Arena Expanded` | Next level size +5 units |
| Caught ≥ 2 times & distance < 2.0 | `Enemy Slowed` | Enemy speed × 0.5 |
| Never caught & chase ratio < 0.3 | `Enemy Accelerated` | Enemy speed × 1.5 |
 
The decision and its effect are displayed in real-time on the game UI.
 
---
 
## 🛠️ Technical Stack
 
**Unity (C#)**
- `DirectorMetrics.cs` — Singleton that collects and stores player performance data
- `DirectorClient.cs` — WebSocket client, sends JSON snapshots every 2 seconds
- `DirectorCommandHandler.cs` — Receives commands and applies them to game systems
- `NPC.cs` — FSM-based enemy AI (Idle → Chase → Attack) using NavMesh
**Python**
- `FastAPI` + `WebSocket` for real-time bidirectional communication
- `director_logic` (inside `server.py`) — Rule-based decision engine
---
 
## 🚀 How to Run
 
### 1. Start the Python Server
 
```bash
cd AIDirector
pip install fastapi uvicorn websockets
uvicorn server:app --host 0.0.0.0 --port 8000
```
 
Or simply double-click `start_server.bat`
 
### 2. Open Unity Project
 
Open `Enemy_AI_Project` in Unity, press **Play**.
 
The AI Director will automatically connect to the Python server and start monitoring.
 
---
 
## 📁 Project Structure
 
```
Enemy_AI_Project/
├── Assets/
│   └── Scripts/
│       ├── DirectorMetrics.cs
│       ├── DirectorClient.cs
│       ├── DirectorCommandHandler.cs
│       ├── NPC.cs
│       ├── FSMGameManager.cs
│       └── LevelGenerator.cs
└── AIDirector/
    ├── server.py
    └── start_server.bat
```
 
---
 
## 💡 Design Decisions
 
**Why Python for the director instead of C#?**
Keeping the decision logic in Python separates concerns cleanly — the game engine handles rendering and physics, while the director runs as an independent service. This also makes it easy to swap the rule-based system for an ML model in the future without touching Unity code.
 
**Why WebSocket instead of HTTP?**
The director needs to send commands back to Unity in real-time without Unity polling. WebSocket provides persistent, bidirectional communication ideal for this use case.
 
**Why rule-based decisions instead of ML?**
For a prototype, rule-based logic is transparent and debuggable. Every decision can be traced to an exact condition. An ML model would be a natural next step for a production system.
 
---
 
## 🔮 Future Improvements
 
- Replace rule-based logic with a trained ML model (e.g. reinforcement learning)
- Add more director commands: spawn additional enemies, change arena shrink speed
- Session history to make decisions based on long-term player patterns
- Multiplayer support: separate director decisions per player
---
 
*Built with Unity 2022 · Python 3.9 · FastAPI*
