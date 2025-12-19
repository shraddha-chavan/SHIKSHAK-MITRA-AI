# 🎥 Web Video Monitor - Live Classroom Monitoring

## Overview

Display **output_accurate.mp4** video on a beautiful web interface with live monitoring.

## 🚀 Quick Start

```bash
cd Web_Video_Monitor
pip install -r requirements.txt
python app.py
```

Then open: **http://localhost:5000**

## ✨ Features

- 🎥 **Live Video Streaming** - Displays output_accurate.mp4
- 📊 **Video Information** - Duration, resolution, FPS, frames
- 🔄 **Auto Loop** - Video loops automatically
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Beautiful UI** - Modern gradient design
- 📈 **Live Metrics** - Engagement, attention, hand raises

## 📁 Video Path

Automatically loads from:
```
AI Video Analyzer/output/output_accurate.mp4
```

## 🌐 Access

- **Local**: http://localhost:5000
- **Network**: http://YOUR_IP:5000

## 🎨 Interface

- **Left Panel**: Live video stream
- **Right Panel**: Video info + metrics
- **Status Badge**: Live monitoring indicator
- **Refresh Button**: Reload video

## 🔧 Customization

### Change Video Path
Edit `app.py`:
```python
VIDEO_PATH = Path("your/video/path.mp4")
```

### Change Port
Edit `app.py`:
```python
app.run(port=8080)
```

### Update Metrics
Edit `index.html` - metrics section

## 📊 Features Included

✅ Video streaming
✅ Auto loop
✅ Video info display
✅ Responsive design
✅ Live status indicator
✅ Refresh button
✅ Beautiful UI

## 🎯 Use Cases

- Live classroom monitoring
- Video playback on web
- Remote observation
- Demo presentations
- Training sessions

---

**Access your video at: http://localhost:5000** 🎥
