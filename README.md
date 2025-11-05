# CASS-Lite v2 🌱
## Carbon-Aware Serverless Scheduler

**Run cloud workloads in the greenest region, automatically.**

CASS-Lite v2 fetches real-time carbon intensity data from 6 global regions, intelligently picks the cleanest region, triggers serverless jobs there, and visualizes everything on a live dashboard.

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
py carbon_fetcher.py
```

### 4. Run the Scheduler
```bash
py main.py
```

The scheduler will automatically select the greenest region and prepare deployment instructions.

---

## 📁 Project Structure

```
cass-lite-v2/
├── scheduler/           # Core scheduling logic
│   ├── main.py         # ✅ Scheduler decision engine (DONE)
│   ├── carbon_fetcher.py   # ✅ Carbon API integration (DONE)
│   ├── job_runner.py   # Cloud Function trigger (TODO)
│   ├── firestore_logger.py # Database logging (TODO)
│   └── config.json     # ✅ Configuration (DONE)
│
├── cloud_functions/    # Serverless workers
│   ├── worker_job/     # (TODO)
│   └── scheduler_function/ # (TODO)
│
├── dashboard/          # Streamlit analytics
│   ├── app.py          # (TODO)
│   └── utils.py        # (TODO)
│
├── scripts/            # Deployment scripts
│   ├── deploy_scheduler.sh # (TODO)
│   └── deploy_worker.sh    # (TODO)
│
└── requirements.txt    # ✅ Dependencies (DONE)
```

---

## 🌍 Supported Regions (6 Active)

- 🇮🇳 **India (IN)** - ~508 gCO₂/kWh
- 🇫🇮 **Finland (FI)** - ~40 gCO₂/kWh ⭐ **Cleanest!**
- 🇩🇪 **Germany (DE)** - ~265 gCO₂/kWh
- �� **Japan (JP)** - ~502 gCO₂/kWh
- 🇦🇺 **New South Wales, Australia (AU-NSW)** - ~327 gCO₂/kWh
- 🇧🇷 **Central-South Brazil (BR-CS)** - ~161 gCO₂/kWh

**Live carbon intensity data updated every 5 minutes!**

---

## ✨ Key Features

### ✅ Phase 1: Carbon Data Fetching (COMPLETE)
- Real-time carbon intensity from ElectricityMap API
- Smart caching (5-minute TTL)
- Flag emojis + colorized console output
- Error handling for failed regions
- Regional ranking system

### ✅ Phase 2: Decision Engine (COMPLETE)
- Intelligent region selection (lowest carbon)
- Carbon savings calculation (up to 86.7%!)
- Decision logging with timestamps
- Job instruction preparation
- Complete scheduling cycle orchestration

### 🚧 Phase 3: Execution (IN PROGRESS)
- Cloud Function triggering
- Firestore logging
- Streamlit dashboard
- Automated deployment scripts

---

## � Sample Output

```
🎯 DEPLOYMENT RECOMMENDATION
✅ Recommended Region: 🇫🇮 Finland (FI)
🌱 Carbon Intensity: 40 gCO₂/kWh
💰 Savings vs Average: 260 gCO₂/kWh (86.7% reduction)
📊 Compared across 6 regions (avg: 300 gCO₂/kWh)
```

---

## �🛠️ Development Progress

### ✅ Completed
- [x] Carbon fetcher module with 6 regions
- [x] Configuration system (config.json)
- [x] Dependencies defined
- [x] Main scheduler decision engine
- [x] Console logging
- [x] Job instruction preparation

### 🚧 In Progress
- [ ] Job runner (Cloud Function trigger)
- [ ] Firestore logger (database persistence)
- [ ] Cloud Functions (worker jobs)
- [ ] Streamlit dashboard (visualization)
- [ ] Deployment scripts

---

## � How It Works

1. **Fetch** - Get live carbon intensity from 6 global regions
2. **Analyze** - Compare carbon footprints across regions
3. **Decide** - Select the greenest region (e.g., Finland @ 40 gCO₂/kWh)
4. **Execute** - Trigger Cloud Function in that region
5. **Log** - Save decision to Firestore
6. **Visualize** - Display analytics in Streamlit dashboard

**Result:** Up to 86.7% carbon reduction vs deploying to average region! 🌱

---

## 🔧 Configuration

Edit `scheduler/config.json` to:
- Add your ElectricityMap API key
- Configure region Cloud Function URLs
- Adjust cache TTL settings
- Set Firestore project details

---

## �📝 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ for a greener cloud.**  
**Making serverless computing carbon-aware, one deployment at a time.** 🌍
