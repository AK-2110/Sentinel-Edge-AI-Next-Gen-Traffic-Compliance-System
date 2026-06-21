# 🚀 How to Run Sentinel (Complete Instructions)

To run the full Sentinel Edge AI system locally, you need to start both the **FastAPI Backend** and the **React Frontend**. Follow these steps in **two separate terminal windows**.

---

## 🟢 Terminal 1: Start the AI Backend

The backend handles the YOLOv8 object detection, EasyOCR processing, and Cryptographic Hashing.

1. **Navigate to the project root directory:**
   ```bash
   cd Sentinel-Edge-AI-Next-Gen-Traffic-Compliance-System
   ```

2. **Create and activate a Python virtual environment (Windows):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install the required AI libraries:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start the FastAPI Server:**
   ```powershell
   uvicorn backend_api:app --host 0.0.0.0 --port 8000
   ```
   > [!TIP]
   > You should see `Application startup complete.` The backend is now successfully running on `http://localhost:8000`.

---

## 🔵 Terminal 2: Start the React Frontend

The frontend powers the beautiful UI, the live inference dashboards, and local storage history.

1. **Navigate to the `frontend` folder:**
   ```bash
   cd Sentinel-Edge-AI-Next-Gen-Traffic-Compliance-System/frontend
   ```

2. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```

3. **Start the Vite Development Server:**
   ```powershell
   npm run dev
   ```
   > [!TIP]
   > You should see `VITE ready in X ms`. The frontend is now successfully running.

---

## 🚦 Final Step: Test the Prototype

1. Open your web browser.
2. Navigate to **`http://localhost:5173`**.
3. You will see the **Overview** landing page.
4. Click **Start Evaluation**.
5. Upload a test image (like `sample_traffic.jpg` located in the project root).
6. Watch the system analyze the image, detect violations, and generate cryptographic evidence cards instantly!
