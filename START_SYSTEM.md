# 🚀 Shikshak Mitra AI - Complete System Startup Guide

## System Components

1. **Main Web Application** (React + Vite)
2. **Feedback Server** (Express.js)
3. **Video Monitor** (Flask + OpenCV)

---

## 📋 Prerequisites

- Node.js (v16 or higher)
- Python 3.8+
- npm or yarn

---

## 🔧 Installation

### 1. Install Main Application Dependencies
```bash
npm install
```

### 2. Install Feedback Server Dependencies
```bash
cd server
npm install
cd ..
```

### 3. Install Video Monitor Dependencies
```bash
cd Web_Video_Monitor
pip install -r requirements.txt
cd ..
```

---

## ▶️ Starting the System

### Option 1: Start All Components (Recommended)

**Terminal 1 - Main Application:**
```bash
npm run dev
```
Access at: http://localhost:5173

**Terminal 2 - Feedback Server:**
```bash
cd server
npm start
```
Running at: http://localhost:3001

**Terminal 3 - Video Monitor:**
```bash
cd Web_Video_Monitor
python app.py
```
Access at: http://localhost:5000

---

## 🌐 Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Main Website | http://localhost:5173 | Teacher & Admin Dashboard |
| Feedback API | http://localhost:3001 | Feedback collection backend |
| Video Monitor | http://localhost:5000 | Live classroom video analysis |

---

## 📊 Features Available

### Teacher Mode
- ✅ Dashboard with real-time metrics
- ✅ Analytics and performance tracking
- ✅ **Scoring System** - Mathematical score calculations
- ✅ **Feedback Form** - Submit teacher feedback
- ✅ Exam performance integration (55 students, 4 subjects)

### Admin Mode
- ✅ Management Dashboard
- ✅ Teacher Comparison
- ✅ Industry Alignment
- ✅ Live Monitoring
- ✅ Reports

---

## 📁 Data Locations

- **Exam Scores**: `Scoring_System/Sample_Data/Exam_Scores/exam_scores.csv`
- **Feedback Data**: `server/data/feedback.csv`
- **Video Files**: `AI Video Analyzer/output/output_accurate.mp4`

---

## 🎯 Key Metrics Calculated

1. **Attention Score** - Student focus tracking
2. **Emotion Score** - Emotional engagement level
3. **Participation Score** - Active class participation
4. **Overall Engagement** - Combined engagement metrics
5. **Comprehension Score** - Understanding level
6. **Teacher Effectiveness** - Overall teaching quality
7. **WPM Score** - Speaking pace analysis

---

## 🔄 Switching Modes

Click the **"Switch to Admin"** or **"Switch to Teacher"** button in the navbar to toggle between modes.

---

## 📝 Submitting Feedback

1. Navigate to **Feedback** in Teacher mode
2. Fill in the form with your details
3. Submit - Data saved to `server/data/feedback.csv`

---

## 🎥 Video Demo

Click **"View Demo"** on homepage to open the live video monitor at http://localhost:5000

---

## 🛠️ Troubleshooting

**Port Already in Use:**
```bash
# Kill process on port 5173
npx kill-port 5173

# Kill process on port 3001
npx kill-port 3001

# Kill process on port 5000
npx kill-port 5000
```

**Missing Dependencies:**
```bash
npm install
cd server && npm install
cd ../Web_Video_Monitor && pip install -r requirements.txt
```

---

## 📦 Project Structure

```
shikshak-mitra-ai-main/
├── src/                          # React application
│   ├── pages/
│   │   ├── TeacherScoring.tsx   # Scoring dashboard
│   │   ├── TeacherFeedback.tsx  # Feedback form
│   │   └── ...
│   └── components/
├── server/                       # Feedback server
│   ├── feedback_server.js
│   └── data/feedback.csv
├── Web_Video_Monitor/           # Video analysis
│   ├── app.py
│   └── templates/index.html
├── Scoring_System/              # Scoring logic
│   ├── mathematical_calculator.py
│   └── Sample_Data/
│       └── Exam_Scores/
└── AI Video Analyzer/           # Video processing
```

---

## ✅ System Status Check

After starting all components, verify:

- [ ] Main app loads at http://localhost:5173
- [ ] Can switch between Teacher/Admin modes
- [ ] Scoring page shows metrics
- [ ] Feedback form submits successfully
- [ ] Video monitor displays video feed
- [ ] Exam data displays in scoring dashboard

---

## 🎓 Ready to Use!

Your Shikshak Mitra AI system is now fully operational with:
- Real-time scoring calculations
- Live feedback collection
- Video monitoring integration
- Academic performance tracking
- Professional teacher dashboard

**Start teaching smarter with AI! 🚀**
