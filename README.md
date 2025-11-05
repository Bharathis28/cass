# CASS-Lite v2 🌱
## Carbon-Aware Serverless Scheduler

**Run cloud workloads in the greenest region, automatically.**

CASS-Lite v2 fetches real-time carbon intensity data, picks the cleanest region, triggers serverless jobs there, and visualizes everything on a live dashboard.

---

## 🚀 Quick Start

### 1. Get Your API Key
Sign up at [ElectricityMap API Portal](https://api-portal.electricitymap.org/) and get your free API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test the Carbon Fetcher
```bash
cd scheduler
python carbon_fetcher.py
```

Replace `YOUR_API_KEY_HERE` in the file with your actual API key.

---

## 📁 Project Structure

```
cass-lite-v2/
├── scheduler/           # Core scheduling logic
│   ├── main.py         # Scheduler entry point
│   ├── carbon_fetcher.py   # ✅ Carbon API integration (DONE)
│   ├── job_runner.py   # Cloud Function trigger
│   ├── firestore_logger.py # Database logging
│   └── config.json     # ✅ Configuration (DONE)
│
├── cloud_functions/    # Serverless workers
│   ├── worker_job/
│   └── scheduler_function/
│
├── dashboard/          # Streamlit analytics
│   ├── app.py
│   └── utils.py
│
├── scripts/            # Deployment scripts
│   ├── deploy_scheduler.sh
│   └── deploy_worker.sh
│
└── requirements.txt    # ✅ Dependencies (DONE)
```

---

## 🌍 Supported Regions

- 🇮🇳 **India (IN)**
- 🇫🇮 **Finland (FI)**
- 🇺🇸 **California (US-CA)**

More regions coming soon!

---

## 🛠️ Development Progress

- [x] Carbon fetcher module
- [x] Configuration setup
- [x] Dependencies defined
- [ ] Scheduler logic
- [ ] Cloud Functions
- [ ] Firestore logger
- [ ] Streamlit dashboard
- [ ] Deployment scripts

---

## 📝 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ for a greener cloud.**
