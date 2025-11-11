# CASS-Lite v2 
## Carbon-Aware Serverless Scheduler

**Run cloud workloads in the greenest region, automatically.**

CASS-Lite v2 fetches real-time carbon intensity data from 6 global regions, intelligently picks the cleanest region, triggers serverless jobs there, and visualizes everything on a live dashboard.

---
## 📁 Project Structure

```
cass-lite-v2/
├── scheduler/           # Core scheduling logic
│   ├── main.py         #  Scheduler decision engine 
│   ├── carbon_fetcher.py   #  Carbon API integration 
│   ├── job_runner.py   #  Cloud Function trigger 
│   ├── firestore_logger.py #  Database logging 
│   └── config.json     #  Configuration 
│
├── cloud_functions/    # Serverless workers
│   ├── worker_job/     #  Worker function 
│   └── scheduler_function/ # Scheduler function 
│
├── dashboard/          # Streamlit analytics
│   ├── app.py           
│   └── utils.py        
│
├── scripts/            # Deployment scripts
│   ├── deploy_scheduler.sh 
│   └── deploy_worker.sh   
│
└── requirements.txt    # Dependencies
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

## � Sample Output

```
🎯 DEPLOYMENT RECOMMENDATION
✅ Recommended Region: 🇫🇮 Finland (FI)
🌱 Carbon Intensity: 40 gCO₂/kWh
💰 Savings vs Average: 260 gCO₂/kWh (86.7% reduction)
📊 Compared across 6 regions (avg: 300 gCO₂/kWh)
```

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

**Built with ❤️ for a greener cloud.**  
**Making serverless computing carbon-aware, one deployment at a time.** 
