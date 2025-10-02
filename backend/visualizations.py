import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any
import json

class VisualizationEngine:
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#ffbb78',
            'danger': '#d62728'
        }
    
    def generate_visualizations(self, resume_data: Dict, score_results: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Generate all visualizations for the resume analysis"""
        visualizations = {
            "skill_gap_chart": self._create_skill_gap_chart(resume_data, job_analysis),
            "score_breakdown_chart": self._create_score_breakdown_chart(score_results),
            "experience_skills_plot": self._create_experience_skills_plot(resume_data),
            "keyword_match_chart": self._create_keyword_match_chart(job_analysis)
        }
        
        return visualizations
    
    def _create_skill_gap_chart(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Create skill gap analysis chart"""
        resume_skills = set(resume_data.get('skills', []))
        
        # Extract JD skills from job analysis
        jd_skills = set()
        if 'gaps' in job_analysis:
            for gap in job_analysis['gaps']:
                if "Missing key skills" in gap:
                    # Extract skills from gap description
                    skills_text = gap.replace("Missing key skills: ", "")
                    jd_skills.update([s.strip() for s in skills_text.split(',')])
        
        # If no JD skills from gaps, use a sample set
        if not jd_skills:
            jd_skills = {'python', 'sql', 'aws', 'docker', 'machine learning', 'react'}
        
        present_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        
        # Create data for chart
        categories = list(jd_skills)
        present_data = [1 if skill in present_skills else 0 for skill in categories]
        required_data = [1 for _ in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Skills Present',
            y=categories,
            x=present_data,
            orientation='h',
            marker_color=self.color_scheme['success']
        ))
        
        fig.add_trace(go.Bar(
            name='Skills Required',
            y=categories,
            x=required_data,
            orientation='h',
            marker_color=self.color_scheme['warning'],
            opacity=0.3
        ))
        
        fig.update_layout(
            title="Skill Gap Analysis",
            xaxis_title="",
            yaxis_title="Skills",
            barmode='overlay',
            height=400,
            showlegend=True
        )
        
        return fig.to_json()
    
    def _create_score_breakdown_chart(self, score_results: Dict) -> Dict[str, Any]:
        """Create score breakdown radar chart"""
        categories = ['Skills', 'Experience', 'Education', 'Projects & Certifications']
        
        if 'category_scores' in score_results:
            scores = [
                score_results['category_scores']['skills'],
                score_results['category_scores']['experience'],
                score_results['category_scores']['education'],
                score_results['category_scores']['projects_certifications']
            ]
        else:
            # Fallback for general scoring
            scores = [75, 65, 80, 60]  # Example scores
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],  # Close the radar
            theta=categories + [categories[0]],
            fill='toself',
            name='Score Breakdown',
            line_color=self.color_scheme['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Score Breakdown",
            showlegend=False,
            height=400
        )
        
        return fig.to_json()
    
    def _create_experience_skills_plot(self, resume_data: Dict) -> Dict[str, Any]:
        """Create experience vs skills scatter plot"""
        experience = resume_data.get('experience_years', 0)
        skills_count = len(resume_data.get('skills', []))
        
        # Sample data for context (in real app, this would be from a database)
        sample_data = {
            'Experience': [1, 2, 3, 4, 5, 6, 7, 8, experience],
            'Skills': [8, 12, 15, 18, 20, 22, 25, 28, skills_count],
            'Role': ['Junior']*3 + ['Mid']*3 + ['Senior']*2 + ['You']
        }
        
        df = pd.DataFrame(sample_data)
        
        fig = px.scatter(
            df, x='Experience', y='Skills', 
            text='Role', color='Role',
            title="Experience vs Skills Comparison",
            size_max=20
        )
        
        fig.update_traces(
            textposition='top center',
            marker=dict(size=12)
        )
        
        fig.update_layout(height=400)
        
        return fig.to_json()
    
    def _create_keyword_match_chart(self, job_analysis: Dict) -> Dict[str, Any]:
        """Create keyword matching chart"""
        keyword_analysis = job_analysis.get('keyword_analysis', {})
        
        present_count = len(keyword_analysis.get('present_keywords', []))
        missing_count = len(keyword_analysis.get('missing_keywords', []))
        total_count = keyword_analysis.get('total_keywords', present_count + missing_count)
        
        labels = ['Keywords Present', 'Keywords Missing']
        values = [present_count, missing_count]
        colors = [self.color_scheme['success'], self.color_scheme['warning']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values,
            hole=.4,
            marker_colors=colors
        )])
        
        fig.update_layout(
            title=f"Keyword Match: {present_count}/{total_count}",
            height=400,
            showlegend=True
        )
        
        return fig.to_json()
    
    def create_skill_network_chart(self, network_data: Dict) -> Dict[str, Any]:
        """Create skill co-occurrence network chart"""
        nodes = network_data.get('nodes', [])
        links = network_data.get('links', [])
        
        if not nodes:
            return {"error": "No network data available"}
        
        # Create node positions (simplified)
        node_trace = go.Scatter(
            x=[], y=[],
            mode='markers+text',
            text=[],
            textposition="middle center",
            marker=dict(
                size=[],
                color=[],
                colorscale='Viridis'
            )
        )
        
        # Simplified network visualization
        # In a full implementation, you would use networkx for proper layout
        fig = go.Figure()
        
        # Add nodes
        node_sizes = [node['value'] for node in nodes]
        node_names = [node['name'] for node in nodes]
        
        # Simple circular layout
        import math
        num_nodes = len(nodes)
        radius = 10
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[node['name']],
                textposition="middle center",
                marker=dict(
                    size=min(50, 10 + node['value']),
                    color=node['value'],
                    colorscale='Viridis'
                ),
                name=node['name']
            ))
        
        # Add links (simplified)
        for link in links[:20]:  # Limit for clarity
            source_node = next((n for n in nodes if n['id'] == link['source']), None)
            target_node = next((n for n in nodes if n['id'] == link['target']), None)
            
            if source_node and target_node:
                # This is a simplified representation
                # Proper network visualization would require calculating node positions
                pass
        
        fig.update_layout(
            title="Skill Co-occurrence Network",
            showlegend=False,
            height=500,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        return fig.to_json()