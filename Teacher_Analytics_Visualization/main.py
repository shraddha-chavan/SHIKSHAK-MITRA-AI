"""
Teacher Analytics Visualization System
Generate graphs, heatmaps, and interactive dashboards
"""

from visualizer import TeacherAnalyticsVisualizer
from interactive_dashboard import InteractiveDashboard
from pathlib import Path

def print_menu():
    print("\n" + "="*70)
    print("  TEACHER ANALYTICS VISUALIZATION SYSTEM")
    print("="*70)
    print("\n📊 Choose visualization type:")
    print("  1. Generate All Static Graphs (PNG)")
    print("  2. Generate Interactive Dashboards (HTML)")
    print("  3. Generate Everything")
    print("  4. Individual Visualizations")
    print("  5. Exit")
    print()

def individual_menu():
    print("\n📈 Individual Visualizations:")
    print("  1. Performance Trends (Line Graph)")
    print("  2. Correlation Heatmap")
    print("  3. Weekly Performance Heatmap")
    print("  4. Radar Chart (Current vs Target)")
    print("  5. Improvement Curve")
    print("  6. Comparison Bars (First vs Latest)")
    print("  7. All Metrics Grid")
    print("  8. Back to Main Menu")
    print()

def main():
    data_path = "sample_data/teacher_data.csv"
    
    # Check if data exists
    if not Path(data_path).exists():
        print(f"❌ Data file not found: {data_path}")
        print("   Please ensure sample_data/teacher_data.csv exists")
        return
    
    viz = TeacherAnalyticsVisualizer()
    dashboard = InteractiveDashboard()
    
    while True:
        print_menu()
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            print("\n🎨 Generating all static visualizations...")
            viz.generate_all_visualizations(data_path)
            print("\n✅ Done! Check the 'outputs' folder for PNG files.")
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            print("\n🌐 Generating interactive dashboards...")
            dashboard.generate_all_interactive(data_path)
            print("\n✅ Done! Open HTML files in 'outputs' folder with your browser.")
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            print("\n🎨 Generating ALL visualizations...")
            print("\n📊 Static graphs...")
            viz.generate_all_visualizations(data_path)
            print("\n🌐 Interactive dashboards...")
            dashboard.generate_all_interactive(data_path)
            print("\n✅ All visualizations complete!")
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            df = viz.load_data(data_path)
            while True:
                individual_menu()
                sub_choice = input("Select option (1-8): ").strip()
                
                if sub_choice == '1':
                    viz.plot_performance_trends(df)
                elif sub_choice == '2':
                    viz.plot_metrics_heatmap(df)
                elif sub_choice == '3':
                    viz.plot_weekly_heatmap(df)
                elif sub_choice == '4':
                    viz.plot_radar_chart(df)
                elif sub_choice == '5':
                    viz.plot_improvement_curve(df)
                elif sub_choice == '6':
                    viz.plot_comparison_bars(df)
                elif sub_choice == '7':
                    viz.plot_all_metrics_grid(df)
                elif sub_choice == '8':
                    break
                else:
                    print("❌ Invalid option")
                
                if sub_choice in ['1','2','3','4','5','6','7']:
                    input("\nPress Enter to continue...")
        
        elif choice == '5':
            print("\n👋 Thank you for using Teacher Analytics Visualization!")
            break
        
        else:
            print("\n❌ Invalid option. Please select 1-5.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🎓 SHIKSHAK MITRA AI - TEACHER ANALYTICS VISUALIZATION")
    print("="*70)
    print("\n  Generate beautiful graphs, heatmaps, and interactive dashboards")
    print("  for teacher performance analysis")
    print("\n" + "="*70)
    
    main()
