"""Quick demo - Generate all visualizations with one command"""

from visualizer import TeacherAnalyticsVisualizer
from interactive_dashboard import InteractiveDashboard

print("\n" + "="*70)
print("  🎨 TEACHER ANALYTICS VISUALIZATION - QUICK DEMO")
print("="*70)



print("\n📊 Generating all visualizations...")
print("   This will create 10 different visualizations\n")

# Static visualizations
print("1️⃣  Performance Trends (Line Graph)...")
print("2️⃣  Correlation Heatmap...")
print("3️⃣  Weekly Performance Heatmap...")
print("4️⃣  Radar Chart (Current vs Target)...")
print("5️⃣  Improvement Curve...")
print("6️⃣  Comparison Bars (First vs Latest)...")
print("7️⃣  All Metrics Grid...")

viz = TeacherAnalyticsVisualizer()
viz.generate_all_visualizations("sample_data/teacher_data.csv")

# Interactive dashboards
print("\n8️⃣  Interactive Trends Dashboard...")
print("9️⃣  Animated Progress...")
print("🔟 Comprehensive Dashboard...")

dashboard = InteractiveDashboard()
dashboard.generate_all_interactive("sample_data/teacher_data.csv")

print("\n" + "="*70)
print("  ✅ ALL VISUALIZATIONS GENERATED!")
print("="*70)
print("\n📁 Check the 'outputs' folder:")
print("   • 7 PNG images (static graphs)")
print("   • 3 HTML files (interactive dashboards)")
print("\n💡 Open HTML files in your browser for interactive experience!")
print("\n" + "="*70)
