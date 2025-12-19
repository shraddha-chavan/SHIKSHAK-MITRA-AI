import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

class TeacherAnalyticsVisualizer:
    """Generate graphs, heatmaps, and line charts for teacher analytics"""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def load_data(self, csv_path):
        """Load teacher data from CSV"""
        df = pd.read_csv(csv_path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    
    def plot_performance_trends(self, df, save=True):
        """Line graph showing performance trends over time"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 'teacher_impact']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for metric, color in zip(metrics, colors):
            if metric in df.columns:
                ax.plot(df.index, df[metric], marker='o', linewidth=2.5, 
                       label=metric.replace('_', ' ').title(), color=color, markersize=6)
        
        ax.set_xlabel('Class Session', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
        ax.set_title('Teacher Performance Trends Over Time', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        
        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'performance_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_metrics_heatmap(self, df, save=True):
        """Heatmap showing correlation between metrics"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 
                  'teacher_impact', 'wpm', 'questions', 'interaction_rate']
        
        available_metrics = [m for m in metrics if m in df.columns]
        corr_matrix = df[available_metrics].corr()
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax, vmin=-1, vmax=1)
        
        ax.set_title('Metrics Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_weekly_heatmap(self, df, save=True):
        """Heatmap showing performance across weeks"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'date' in df.columns:
            df['week'] = df['date'].dt.isocalendar().week
            df['day'] = df['date'].dt.day_name()
        else:
            df['week'] = (df.index // 5) + 1
            df['day'] = df.index % 5
        
        metrics = ['engagement', 'attention', 'retention', 'curiosity']
        pivot_data = df.groupby('week')[metrics].mean()
        
        sns.heatmap(pivot_data.T, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Score (%)'}, linewidths=0.5, ax=ax)
        
        ax.set_title('Weekly Performance Heatmap', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Week Number', fontsize=12, fontweight='bold')
        ax.set_ylabel('Metrics', fontsize=12, fontweight='bold')
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'weekly_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_radar_chart(self, df, save=True):
        """Radar chart showing current vs target performance"""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        metrics = ['Engagement', 'Attention', 'Retention', 'Curiosity', 'Teacher Impact']
        current_values = [
            df['engagement'].iloc[-1] if 'engagement' in df.columns else 0,
            df['attention'].iloc[-1] if 'attention' in df.columns else 0,
            df['retention'].iloc[-1] if 'retention' in df.columns else 0,
            df['curiosity'].iloc[-1] if 'curiosity' in df.columns else 0,
            df['teacher_impact'].iloc[-1] if 'teacher_impact' in df.columns else 0
        ]
        target_values = [85, 85, 85, 80, 85]
        
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        current_values += current_values[:1]
        target_values += target_values[:1]
        angles += angles[:1]
        
        ax.plot(angles, current_values, 'o-', linewidth=2, label='Current', color='#FF6B6B')
        ax.fill(angles, current_values, alpha=0.25, color='#FF6B6B')
        ax.plot(angles, target_values, 'o-', linewidth=2, label='Target', color='#4ECDC4')
        ax.fill(angles, target_values, alpha=0.25, color='#4ECDC4')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=11)
        ax.set_ylim(0, 100)
        ax.set_title('Current vs Target Performance', fontsize=16, fontweight='bold', pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'radar_chart.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_improvement_curve(self, df, save=True):
        """Curve showing improvement trajectory"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Left: Overall improvement
        if 'teacher_impact' in df.columns:
            x = df.index
            y = df['teacher_impact']
            
            ax1.plot(x, y, 'o-', linewidth=2.5, color='#4ECDC4', markersize=8, label='Actual')
            
            # Fit polynomial curve
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            ax1.plot(x, p(x), '--', linewidth=2, color='#FF6B6B', label='Trend')
            
            ax1.fill_between(x, y, alpha=0.3, color='#4ECDC4')
            ax1.set_xlabel('Class Session', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Teacher Impact Score', fontsize=12, fontweight='bold')
            ax1.set_title('Overall Improvement Curve', fontsize=14, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # Right: Rate of improvement
        if 'teacher_impact' in df.columns:
            improvement_rate = df['teacher_impact'].diff().fillna(0)
            colors = ['green' if x >= 0 else 'red' for x in improvement_rate]
            
            ax2.bar(df.index, improvement_rate, color=colors, alpha=0.7)
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax2.set_xlabel('Class Session', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Improvement Rate', fontsize=12, fontweight='bold')
            ax2.set_title('Session-to-Session Improvement', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'improvement_curve.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_comparison_bars(self, df, save=True):
        """Bar chart comparing first vs latest performance"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 'teacher_impact']
        first_values = [df[m].iloc[0] if m in df.columns else 0 for m in metrics]
        latest_values = [df[m].iloc[-1] if m in df.columns else 0 for m in metrics]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, first_values, width, label='First Class', color='#FFB6C1', alpha=0.8)
        bars2 = ax.bar(x + width/2, latest_values, width, label='Latest Class', color='#90EE90', alpha=0.8)
        
        ax.set_xlabel('Metrics', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
        ax.set_title('Performance Comparison: First vs Latest', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics], rotation=15)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add improvement percentage on bars
        for i, (first, latest) in enumerate(zip(first_values, latest_values)):
            if first > 0:
                improvement = ((latest - first) / first) * 100
                ax.text(i, max(first, latest) + 2, f'+{improvement:.0f}%', 
                       ha='center', fontsize=9, fontweight='bold', color='green')
        
        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'comparison_bars.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_all_metrics_grid(self, df, save=True):
        """Grid of small line charts for all metrics"""
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 
                  'teacher_impact', 'wpm', 'questions', 'interaction_rate']
        available = [m for m in metrics if m in df.columns]
        
        n_metrics = len(available)
        n_cols = 3
        n_rows = (n_metrics + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 3))
        axes = axes.flatten() if n_metrics > 1 else [axes]
        
        colors = plt.cm.Set3(np.linspace(0, 1, n_metrics))
        
        for idx, (metric, color) in enumerate(zip(available, colors)):
            ax = axes[idx]
            ax.plot(df.index, df[metric], marker='o', linewidth=2, color=color, markersize=5)
            ax.fill_between(df.index, df[metric], alpha=0.3, color=color)
            ax.set_title(metric.replace('_', ' ').title(), fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Session', fontsize=9)
            ax.set_ylabel('Score', fontsize=9)
        
        # Hide extra subplots
        for idx in range(n_metrics, len(axes)):
            axes[idx].axis('off')
        
        fig.suptitle('All Metrics Overview', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'all_metrics_grid.png', dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def generate_all_visualizations(self, csv_path):
        """Generate all visualizations at once"""
        print("📊 Loading data...")
        df = self.load_data(csv_path)
        
        print("📈 Generating performance trends...")
        self.plot_performance_trends(df)
        
        print("🔥 Generating correlation heatmap...")
        self.plot_metrics_heatmap(df)
        
        print("📅 Generating weekly heatmap...")
        self.plot_weekly_heatmap(df)
        
        print("🎯 Generating radar chart...")
        self.plot_radar_chart(df)
        
        print("📉 Generating improvement curve...")
        self.plot_improvement_curve(df)
        
        print("📊 Generating comparison bars...")
        self.plot_comparison_bars(df)
        
        print("🔲 Generating metrics grid...")
        self.plot_all_metrics_grid(df)
        
        print(f"\n✅ All visualizations saved to: {self.output_dir.absolute()}")


if __name__ == "__main__":
    viz = TeacherAnalyticsVisualizer()
    viz.generate_all_visualizations("sample_data/teacher_data.csv")
