# 📊 Teacher Analytics Visualization System

## Overview

Generate beautiful **graphs**, **heatmaps**, and **interactive dashboards** for teacher performance analysis.

## 🎨 Visualizations Included

### Static Graphs (PNG)
1. **Performance Trends** - Line graph showing all metrics over time
2. **Correlation Heatmap** - Shows relationships between metrics
3. **Weekly Heatmap** - Performance across weeks
4. **Radar Chart** - Current vs target performance
5. **Improvement Curve** - Overall improvement trajectory
6. **Comparison Bars** - First class vs latest class
7. **All Metrics Grid** - Small multiples of all metrics

### Interactive Dashboards (HTML)
1. **Interactive Trends** - Hover for details, zoom, pan
2. **Animated Progress** - Watch performance improve over time
3. **Comprehensive Dashboard** - Multi-panel overview

## 🚀 Quick Start

### Install Dependencies
```bash
cd "Teacher_Analytics_Visualization"
pip install -r requirements.txt
```

### Run Application
```bash
python main.py
```

### Generate All Visualizations
```bash
python visualizer.py
```

### Generate Interactive Dashboards
```bash
python interactive_dashboard.py
```

## 📁 File Structure

```
Teacher_Analytics_Visualization/
├── visualizer.py              # Static graphs generator
├── interactive_dashboard.py   # Interactive HTML dashboards
├── main.py                    # Main application with menu
├── requirements.txt           # Dependencies
├── sample_data/
│   └── teacher_data.csv      # Sample data
├── outputs/                   # Generated visualizations
│   ├── *.png                 # Static images
│   └── *.html                # Interactive dashboards
└── README.md
```

## 📊 Sample Data Format

Your CSV should have these columns:
```csv
date,engagement,attention,retention,curiosity,teacher_impact,wpm,questions,interaction_rate
2024-01-15,45,40,48,35,52,195,8,25
2024-01-16,48,43,50,38,54,190,9,28
...
```

## 💻 Usage Examples

### Generate All Static Graphs
```python
from visualizer import TeacherAnalyticsVisualizer

viz = TeacherAnalyticsVisualizer()
viz.generate_all_visualizations("sample_data/teacher_data.csv")
```

### Generate Specific Graph
```python
viz = TeacherAnalyticsVisualizer()
df = viz.load_data("sample_data/teacher_data.csv")
viz.plot_performance_trends(df)
viz.plot_metrics_heatmap(df)
```

### Generate Interactive Dashboard
```python
from interactive_dashboard import InteractiveDashboard

dashboard = InteractiveDashboard()
dashboard.generate_all_interactive("sample_data/teacher_data.csv")
```

## 🎯 Visualization Details

### 1. Performance Trends
- **Type**: Multi-line graph
- **Shows**: All 5 core metrics over time
- **Colors**: Distinct colors for each metric
- **Features**: Markers, grid, legend

### 2. Correlation Heatmap
- **Type**: Heatmap with annotations
- **Shows**: Correlation between all metrics
- **Colors**: Red-Yellow-Green scale
- **Range**: -1 to +1

### 3. Weekly Heatmap
- **Type**: Time-based heatmap
- **Shows**: Performance across weeks
- **Colors**: Yellow-Orange-Red scale
- **Useful for**: Identifying patterns

### 4. Radar Chart
- **Type**: Polar chart
- **Shows**: Current vs target performance
- **Metrics**: 5 core metrics
- **Useful for**: Quick overview

### 5. Improvement Curve
- **Type**: Dual chart (line + bar)
- **Shows**: Overall trend + session-to-session changes
- **Features**: Polynomial fit, color-coded bars

### 6. Comparison Bars
- **Type**: Grouped bar chart
- **Shows**: First class vs latest class
- **Features**: Improvement percentage labels

### 7. All Metrics Grid
- **Type**: Small multiples
- **Shows**: Individual trends for each metric
- **Layout**: 3x3 grid

### 8. Interactive Trends
- **Type**: Plotly line chart
- **Features**: Hover details, zoom, pan, download
- **Format**: HTML (open in browser)

### 9. Animated Progress
- **Type**: Animated bar chart
- **Features**: Play/pause controls
- **Shows**: Progress over time

### 10. Comprehensive Dashboard
- **Type**: Multi-panel dashboard
- **Panels**: Trends, distribution, improvement, gauge
- **Format**: Single HTML file

## 🎨 Customization

### Change Colors
Edit the color lists in `visualizer.py`:
```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
```

### Change Figure Size
```python
plt.rcParams['figure.figsize'] = (12, 8)  # Width, Height
```

### Change DPI (Resolution)
```python
plt.savefig('output.png', dpi=300)  # Higher = better quality
```

## 📈 Integration with Your System

### Use with RAG System
```python
from RAG_System.rag_integration import RAGIntegration
from Teacher_Analytics_Visualization.visualizer import TeacherAnalyticsVisualizer

# Get analysis
integration = RAGIntegration()
result = integration.analyze_with_rag()

# Create visualization data
# ... convert result to CSV ...

# Generate visualizations
viz = TeacherAnalyticsVisualizer()
viz.generate_all_visualizations("your_data.csv")
```

### Use with Existing Data
```python
import pandas as pd

# Load your existing CSV
df = pd.read_csv("path/to/your/data.csv")

# Generate visualizations
viz = TeacherAnalyticsVisualizer()
viz.plot_performance_trends(df)
```

## 🔧 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Data file not found"
- Ensure `sample_data/teacher_data.csv` exists
- Or provide your own CSV path

### Graphs not showing
- Check if `outputs/` folder exists
- Verify matplotlib backend: `plt.show()`

### Interactive dashboards not opening
- Open HTML files manually from `outputs/` folder
- Use any web browser

## 📊 Output Files

All visualizations are saved to `outputs/` folder:

**Static Images (PNG)**
- `performance_trends.png`
- `correlation_heatmap.png`
- `weekly_heatmap.png`
- `radar_chart.png`
- `improvement_curve.png`
- `comparison_bars.png`
- `all_metrics_grid.png`

**Interactive Dashboards (HTML)**
- `interactive_trends.html`
- `animated_progress.html`
- `comprehensive_dashboard.html`

## 🎯 Best Practices

1. **Use high DPI** for presentations (300 DPI)
2. **Interactive dashboards** for exploration
3. **Static images** for reports
4. **Regular updates** to track progress
5. **Compare periods** using date ranges

## 📞 Support

- Check sample data format
- Ensure all columns present
- Verify date format: YYYY-MM-DD
- Use numeric values for metrics

## 🚀 Next Steps

1. Run `python main.py`
2. Choose option 3 (Generate Everything)
3. Check `outputs/` folder
4. Open HTML files in browser
5. Use PNG files in reports

---

**Making teacher analytics beautiful and insightful!** 📊✨
