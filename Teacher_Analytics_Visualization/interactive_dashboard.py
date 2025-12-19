import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path

class InteractiveDashboard:
    """Create interactive HTML dashboards with Plotly"""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def load_data(self, csv_path):
        df = pd.read_csv(csv_path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    
    def create_interactive_trends(self, df):
        """Interactive line chart with hover details"""
        fig = go.Figure()
        
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 'teacher_impact']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for metric, color in zip(metrics, colors):
            if metric in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[metric],
                    mode='lines+markers',
                    name=metric.replace('_', ' ').title(),
                    line=dict(color=color, width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{fullData.name}</b><br>Session: %{x}<br>Score: %{y:.1f}%<extra></extra>'
                ))
        
        fig.update_layout(
            title='Interactive Performance Trends',
            xaxis_title='Class Session',
            yaxis_title='Score (%)',
            hovermode='x unified',
            template='plotly_white',
            height=600
        )
        
        fig.write_html(self.output_dir / 'interactive_trends.html')
        return fig
    
    def create_3d_surface(self, df):
        """3D surface plot showing metric relationships"""
        if 'engagement' in df.columns and 'attention' in df.columns and 'retention' in df.columns:
            fig = go.Figure(data=[go.Surface(
                x=df.index,
                y=df['engagement'],
                z=df['attention'].values.reshape(-1, 1) @ df['retention'].values.reshape(1, -1),
                colorscale='Viridis'
            )])
            
            fig.update_layout(
                title='3D Performance Surface',
                scene=dict(
                    xaxis_title='Session',
                    yaxis_title='Engagement',
                    zaxis_title='Combined Score'
                ),
                height=700
            )
            
            fig.write_html(self.output_dir / '3d_surface.html')
            return fig
    
    def create_animated_progress(self, df):
        """Animated bar chart showing progress over time"""
        metrics = ['engagement', 'attention', 'retention', 'curiosity', 'teacher_impact']
        
        frames = []
        for i in range(len(df)):
            frame_data = []
            for metric in metrics:
                if metric in df.columns:
                    frame_data.append(go.Bar(
                        x=[metric.replace('_', ' ').title()],
                        y=[df[metric].iloc[i]],
                        name=metric
                    ))
            frames.append(go.Frame(data=frame_data, name=str(i)))
        
        fig = go.Figure(
            data=[go.Bar(x=[m.replace('_', ' ').title() for m in metrics], 
                        y=[df[m].iloc[0] if m in df.columns else 0 for m in metrics])],
            frames=frames
        )
        
        fig.update_layout(
            title='Animated Performance Progress',
            yaxis=dict(range=[0, 100], title='Score (%)'),
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=500))]),
                    dict(label='Pause', method='animate', args=[[None], dict(frame=dict(duration=0), mode='immediate')])
                ]
            )],
            height=600
        )
        
        fig.write_html(self.output_dir / 'animated_progress.html')
        return fig
    
    def create_comprehensive_dashboard(self, df):
        """Multi-panel interactive dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Performance Trends', 'Metrics Distribution', 
                          'Improvement Rate', 'Current Status'),
            specs=[[{'type': 'scatter'}, {'type': 'bar'}],
                   [{'type': 'scatter'}, {'type': 'indicator'}]]
        )
        
        # Trends
        for metric in ['engagement', 'attention', 'retention']:
            if metric in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df[metric], name=metric, mode='lines+markers'), row=1, col=1)
        
        # Distribution
        metrics = ['engagement', 'attention', 'retention', 'curiosity']
        latest = [df[m].iloc[-1] if m in df.columns else 0 for m in metrics]
        fig.add_trace(go.Bar(x=metrics, y=latest, marker_color='lightblue'), row=1, col=2)
        
        # Improvement rate
        if 'teacher_impact' in df.columns:
            improvement = df['teacher_impact'].diff().fillna(0)
            colors = ['green' if x >= 0 else 'red' for x in improvement]
            fig.add_trace(go.Bar(x=df.index, y=improvement, marker_color=colors), row=2, col=1)
        
        # Current status indicator
        if 'teacher_impact' in df.columns:
            current_score = df['teacher_impact'].iloc[-1]
            fig.add_trace(go.Indicator(
                mode='gauge+number+delta',
                value=current_score,
                delta={'reference': df['teacher_impact'].iloc[0]},
                gauge={'axis': {'range': [0, 100]},
                      'bar': {'color': 'darkblue'},
                      'steps': [
                          {'range': [0, 50], 'color': 'lightgray'},
                          {'range': [50, 75], 'color': 'gray'},
                          {'range': [75, 100], 'color': 'lightgreen'}
                      ]},
                title={'text': 'Teacher Impact'}
            ), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True, title_text='Comprehensive Teacher Analytics Dashboard')
        fig.write_html(self.output_dir / 'comprehensive_dashboard.html')
        return fig
    
    def generate_all_interactive(self, csv_path):
        """Generate all interactive visualizations"""
        print("📊 Loading data...")
        df = self.load_data(csv_path)
        
        print("📈 Creating interactive trends...")
        self.create_interactive_trends(df)
        
        print("🎬 Creating animated progress...")
        self.create_animated_progress(df)
        
        print("📊 Creating comprehensive dashboard...")
        self.create_comprehensive_dashboard(df)
        
        print(f"\n✅ Interactive dashboards saved to: {self.output_dir.absolute()}")
        print("   Open the HTML files in your browser!")


if __name__ == "__main__":
    dashboard = InteractiveDashboard()
    dashboard.generate_all_interactive("sample_data/teacher_data.csv")
