import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from typing import Dict, List, Any
import json

class AssociationMiner:
    def __init__(self, dataset_path: str = "data/resume_dataset.csv"):
        self.dataset_path = dataset_path
        self.frequent_itemsets = None
        self.rules = None
        
        # Load or generate sample dataset
        self._initialize_dataset()
        self._mine_association_rules()
    
    def _initialize_dataset(self):
        """Initialize sample resume dataset for association rule mining"""
        try:
            self.dataset = pd.read_csv(self.dataset_path)
        except:
            # Generate synthetic dataset
            self._generate_sample_dataset()
    
    def _generate_sample_dataset(self):
        """Generate synthetic resume dataset with skill combinations"""
        np.random.seed(42)
        
        # Common skill combinations by role
        role_skills = {
            'data_scientist': ['python', 'sql', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'machine learning'],
            'web_developer': ['javascript', 'html', 'css', 'react', 'node.js', 'python', 'sql'],
            'devops_engineer': ['aws', 'docker', 'kubernetes', 'jenkins', 'python', 'linux', 'terraform'],
            'mobile_developer': ['java', 'kotlin', 'swift', 'react native', 'javascript', 'python'],
            'data_analyst': ['sql', 'python', 'excel', 'tableau', 'power bi', 'pandas', 'statistics']
        }
        
        data = []
        for role, skills in role_skills.items():
            for _ in range(50):  # 50 resumes per role
                # Select 4-7 skills from role skills plus some random ones
                num_skills = np.random.randint(4, 8)
                selected_skills = np.random.choice(skills, num_skills, replace=False)
                
                # Add some common additional skills
                common_skills = ['git', 'agile', 'problem solving', 'communication']
                additional = np.random.choice(common_skills, 2, replace=False)
                
                all_skills = list(selected_skills) + list(additional)
                data.append({
                    'role': role,
                    'skills': ','.join(all_skills)
                })
        
        self.dataset = pd.DataFrame(data)
        
        # Save dataset
        import os
        os.makedirs('data', exist_ok=True)
        self.dataset.to_csv(self.dataset_path, index=False)
    
    def _mine_association_rules(self):
        """Mine association rules from the resume dataset"""
        # Prepare transaction data
        transactions = []
        for skills_str in self.dataset['skills']:
            transactions.append(skills_str.split(','))
        
        # Transform transactions
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        # Find frequent itemsets
        self.frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        
        # Generate association rules
        if not self.frequent_itemsets.empty:
            self.rules = association_rules(
                self.frequent_itemsets, 
                metric="confidence", 
                min_threshold=0.6
            )
    
    def get_recommendations(self, current_skills: List[str], experience: List[Dict] = None) -> Dict[str, Any]:
        """Get skill recommendations based on association rules"""
        if self.rules is None or self.rules.empty:
            return {"error": "No association rules available"}
        
        recommendations = {
            "frequent_combinations": [],
            "suggested_skills": [],
            "role_based_suggestions": []
        }
        
        # Find rules where antecedents match current skills
        current_skills_set = set(current_skills)
        
        for _, rule in self.rules.iterrows():
            antecedents = set(rule['antecedents'])
            consequents = set(rule['consequents'])
            
            # Check if some antecedents are in current skills
            if antecedents.intersection(current_skills_set):
                # Get new skills to recommend
                new_skills = consequents - current_skills_set
                
                if new_skills:
                    recommendations["suggested_skills"].append({
                        "based_on": list(antecedents.intersection(current_skills_set)),
                        "recommend": list(new_skills),
                        "confidence": round(rule['confidence'], 3),
                        "support": round(rule['support'], 3)
                    })
        
        # Get frequent combinations
        self._add_frequent_combinations(recommendations, current_skills)
        
        # Get role-based suggestions
        self._add_role_based_suggestions(recommendations, current_skills, experience)
        
        # Sort and limit recommendations
        recommendations["suggested_skills"].sort(key=lambda x: x['confidence'], reverse=True)
        recommendations["suggested_skills"] = recommendations["suggested_skills"][:5]
        
        return recommendations
    
    def _add_frequent_combinations(self, recommendations: Dict, current_skills: List[str]):
        """Add frequently co-occurring skill combinations"""
        if self.frequent_itemsets is None:
            return
        
        for _, itemset in self.frequent_itemsets.nlargest(5, 'support').iterrows():
            items = list(itemset['itemsets'])
            if len(items) >= 2:
                recommendations["frequent_combinations"].append({
                    "skills": items,
                    "frequency": round(itemset['support'], 3)
                })
    
    def _add_role_based_suggestions(self, recommendations: Dict, current_skills: List[str], experience: List[Dict] = None):
        """Add role-based skill suggestions"""
        # Analyze current skills to infer role
        role_indicators = {
            'data_scientist': ['python', 'machine learning', 'pandas', 'tensorflow'],
            'web_developer': ['javascript', 'react', 'html', 'css'],
            'devops_engineer': ['docker', 'kubernetes', 'aws', 'terraform'],
            'data_analyst': ['sql', 'excel', 'tableau', 'power bi']
        }
        
        role_scores = {}
        for role, indicators in role_indicators.items():
            score = len(set(indicators).intersection(set(current_skills)))
            role_scores[role] = score
        
        # Get top inferred role
        if role_scores:
            inferred_role = max(role_scores, key=role_scores.get)
            if role_scores[inferred_role] > 0:
                
                # Get skills commonly associated with this role but missing
                role_skills = set()
                for _, row in self.dataset[self.dataset['role'] == inferred_role].iterrows():
                    role_skills.update(row['skills'].split(','))
                
                missing_skills = role_skills - set(current_skills)
                
                recommendations["role_based_suggestions"] = {
                    "inferred_role": inferred_role,
                    "commonly_missing": list(missing_skills)[:5]
                }
    
    def get_skill_network_data(self) -> Dict[str, Any]:
        """Get data for skill co-occurrence network visualization"""
        if self.frequent_itemsets is None:
            return {"nodes": [], "links": []}
        
        # Create nodes and links for network visualization
        nodes = []
        links = []
        
        # Get all unique skills
        all_skills = set()
        for itemset in self.frequent_itemsets['itemsets']:
            all_skills.update(itemset)
        
        # Create nodes
        for skill in all_skills:
            # Calculate node size based on frequency
            skill_frequency = len(self.dataset[self.dataset['skills'].str.contains(skill)])
            nodes.append({
                "id": skill,
                "name": skill,
                "value": skill_frequency
            })
        
        # Create links from association rules
        if self.rules is not None:
            for _, rule in self.rules.iterrows():
                antecedents = list(rule['antecedents'])
                consequents = list(rule['consequents'])
                
                for ant in antecedents:
                    for cons in consequents:
                        if ant != cons:
                            links.append({
                                "source": ant,
                                "target": cons,
                                "value": round(rule['confidence'], 3)
                            })
        
        return {
            "nodes": nodes,
            "links": links
        }