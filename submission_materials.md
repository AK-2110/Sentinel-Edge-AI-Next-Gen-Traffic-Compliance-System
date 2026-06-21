# 🚀 Sentinel Pitch Deck & Submission Materials

## 1. Project Overview

**Project Name:** Sentinel (Next-Gen Traffic Compliance System)  
**Tagline:** "Immutable Edge AI for Smart City Traffic Compliance"  
**GitHub Repository:** [AK-2110/Sentinel-Edge-AI-Next-Gen-Traffic-Compliance-System](https://github.com/AK-2110/Sentinel-Edge-AI-Next-Gen-Traffic-Compliance-System)

**Description:**  
Sentinel is a high-performance, edge-deployed computer vision platform that automates traffic violation detection (triple-riding, speeding, illegal parking). By running YOLOv8 neural networks directly on camera nodes and hashing every piece of evidence, Sentinel guarantees zero-latency inference and 100% data non-repudiation for municipal authorities.

---

## 2. The Problem
Traffic authorities rely on manual monitoring or legacy systems that are slow, inaccurate, and susceptible to tampering or corruption. Issuing fines often results in disputes because the evidentiary chain of custody is weak.

## 3. The Solution (Sentinel)
1. **Edge AI:** Processes video streams instantly using YOLOv8 without relying on slow cloud uplinks.
2. **Instant OCR:** Extracts license plates dynamically with EasyOCR.
3. **Cryptographic Ledgers:** Immediately generates a SHA-256 hash for every piece of evidence upon capture, ensuring the data cannot be tampered with.

---

## 4. Technical Architecture & Stack

### Frontend (User Experience)
- **Framework:** React + Vite
- **Styling:** Tailwind CSS (Dark Mode, Glassmorphism, Neon Accents)
- **Motion:** Framer Motion (60fps hardware-accelerated animations)
- **Analytics:** Recharts (Interactive telemetry dashboards)
- **Persistence:** LocalStorage (Maintains offline evaluation history)

### Backend (Microservices)
- **Framework:** FastAPI (High-performance asynchronous Python backend)
- **AI Models:** YOLOv8 (Object tracking), EasyOCR (Text extraction)
- **Security:** Python `hashlib` for SHA-256 evidence hashing

---

## 5. Visual Assets for Slides

> [!TIP]
> Include the AI-generated concept art below in your presentation to illustrate the vision to the judges.

1. **Smart City Integration:** ![Smart City Overview](C:/Users/aksha/.gemini/antigravity-ide/brain/ceaae4dc-8d5c-401b-b14b-387ea392c43f/smart_city_traffic_1782051849699.png)
2. **Edge Hardware Interface:** ![Edge Camera AI](C:/Users/aksha/.gemini/antigravity-ide/brain/ceaae4dc-8d5c-401b-b14b-387ea392c43f/edge_camera_ai_1782051865253.png)
3. **LPR Evidence Scan:** ![License Plate Scan](C:/Users/aksha/.gemini/antigravity-ide/brain/ceaae4dc-8d5c-401b-b14b-387ea392c43f/license_plate_scan_1782051879068.png)

*(Note: Take screenshots of your new React dashboard (specifically the 'Overview', 'Live Inference', and 'Global Analytics' tabs) and add them to your slides!)*

---

## 6. How to Run for Judges

> [!IMPORTANT]
> If judges ask to test the prototype on their own machines, give them these instructions.

**Backend Setup:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
uvicorn backend_api:app --host 0.0.0.0 --port 8000
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```
*Open `http://localhost:5173` in a web browser.*
