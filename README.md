# 🚀 ResumeVision AI - Smart Resume Analyzer

<div align="center">

![ResumeVision AI](https://img.shields.io/badge/ResumeVision-AI--Powered-blue?style=for-the-badge&logo=ai)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=for-the-badge&logo=streamlit)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green?style=for-the-badge&logo=flask)

**Next-Generation Resume Analysis Powered by Advanced AI & RAG Technology**

[![Demo](https://img.shields.io/badge/🎯-Live_Demo-orange?style=for-the-badge)](https://your-demo-link.streamlit.app)
[![Documentation](https://img.shields.io/badge/📚-Documentation-blue?style=for-the-badge)](docs/)
[![Issues](https://img.shields.io/badge/🐛-Issues-red?style=for-the-badge)](https://github.com/your-username/resume-vision-ai/issues)
[![License](https://img.shields.io/badge/📄-License_MIT-green?style=for-the-badge)](LICENSE)

</div>

## ✨ Overview

ResumeVision AI is a cutting-edge resume analysis platform that leverages **Artificial Intelligence**, **RAG (Retrieval-Augmented Generation)**, and **Association Rule Mining** to provide comprehensive resume insights, smart recommendations, and candidate comparisons.

### 🎯 Key Features

| Feature | Description | Emoji |
|---------|-------------|--------|
| **AI-Powered Analysis** | Deep resume parsing with intelligent scoring | 🤖 |
| **Smart Skill Extraction** | Automatic skill detection and categorization | 🛠️ |
| **RAG Technology** | Context-aware suggestions using knowledge base | 🔮 |
| **Multi-Resume Comparison** | Compare and rank multiple candidates | ⚖️ |
| **Visual Analytics** | Interactive charts and insights | 📊 |
| **Skill Gap Analysis** | Identify missing skills and improvements | 📈 |
| **Real-time Processing** | Instant analysis with progress tracking | ⚡ |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AdithyaTB/ResumeAnalyzer-RAG.git
cd ResumeAnalyzer-RAG.git
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
python run_stable.py
```

3. **Set up the frontend** (in a new terminal)
```bash
pip install streamlit requests plotly pandas
streamlit run main.py
```

4. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:5000

## 🏗️ Project Structure

```
resume-vision-ai/
├── 📁 backend/
│   ├── app.py                 # Flask API server
│   ├── run_stable.py          # Stable server runner
│   ├── requirements.txt       # Backend dependencies
│   ├── 📁 knowledge_base/     # RAG knowledge base
│   └── 📁 uploads/           # File storage
├── 📁 frontend/
│   ├── main.py               # Streamlit application
│   └── requirements.txt      # Frontend dependencies
├── 📁 data/
│   ├── sample_resumes/       # Sample data
│   ├── job_descriptions/     # JD examples
│   └── resume_dataset.csv    # Association rule data
├── 📁 docs/                  # Documentation
├── LICENSE
└── README.md
```

## 🎨 Features Deep Dive

### 1. 🤖 Intelligent Resume Analysis
- **Text Extraction**: PDF, DOCX, and TXT file support
- **Skill Detection**: 1000+ technical and soft skills
- **Experience Parsing**: Automatic years of experience calculation
- **Personal Info**: Name, email, phone extraction
- **Education Detection**: Degree and institution recognition

### 2. 🔮 RAG-Powered Insights
- **Knowledge Base**: Best practices and industry standards
- **Contextual Suggestions**: Role-specific recommendations
- **Writing Improvements**: AI-powered content enhancement
- **Skill Recommendations**: Missing skills based on job descriptions

### 3. 📊 Advanced Scoring System
```python
Scoring Weights:
- Skills Match: 50%
- Experience Relevance: 20%
- Education Alignment: 15%
- Projects & Certifications: 15%
```

### 4. ⚖️ Smart Comparison Engine
- **Multi-candidate Ranking**: AI-powered scoring and ranking
- **Skill Comparison**: Side-by-side competency analysis
- **Gap Identification**: Missing requirements highlighting
- **Visual Rankings**: Interactive comparison charts

## 🛠️ Technology Stack

### Backend
- **Flask**: REST API framework
- **SpaCy**: NLP and entity recognition
- **scikit-learn**: Machine learning algorithms
- **FAISS**: Vector similarity search
- **MLxtend**: Association rule mining

### Frontend
- **Streamlit**: Interactive web application
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Requests**: API communication

### AI/ML Components
- **RAG Architecture**: Retrieval-Augmented Generation
- **Association Rule Mining**: Frequent pattern discovery
- **TF-IDF Vectorization**: Text similarity analysis
- **Cosine Similarity**: Document matching

## 📈 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server health check |
| `/analyze` | POST | Single resume analysis |
| `/compare` | POST | Multiple resume comparison |
| `/test` | GET | Test endpoint with sample data |

### Example API Usage

```python
import requests

# Analyze a resume
files = {'resume': open('resume.pdf', 'rb')}
data = {'job_description': 'Python developer with AWS experience'}
response = requests.post('http://localhost:5000/analyze', files=files, data=data)
```

## 🎯 Usage Examples

### Single Resume Analysis
1. Upload your resume (PDF/DOCX/TXT)
2. Optional: Add job description for targeted analysis
3. Get instant AI-powered insights including:
   - Overall score and breakdown
   - Skill gap analysis
   - Improvement suggestions
   - Visual analytics

### Multiple Resume Comparison
1. Upload 2+ resumes
2. Set comparison criteria (optional job description)
3. View ranked candidates with:
   - Comparative scoring
   - Skill match percentages
   - Detailed analysis per candidate

## 📊 Sample Output

### Analysis Results
```json
{
  "score": {
    "overall_score": 87,
    "category_scores": {
      "skills": 92,
      "experience": 85,
      "education": 78,
      "projects_certifications": 82
    }
  },
  "suggestions": {
    "rag": {
      "text_improvements": ["Add quantifiable achievements"],
      "missing_skills": ["kubernetes", "terraform"]
    }
  }
}
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
FLASK_ENV=production
UPLOAD_FOLDER=../frontend/uploads
MAX_FILE_SIZE=16777216
```

### Customization Options
- Modify skill database in `skill_extractor.py`
- Adjust scoring weights in `scoring_engine.py`
- Extend knowledge base in `rag_engine.py`
- Customize visualizations in `visualizations.py`

## 🚀 Deployment

### Local Deployment
```bash
# Backend (Terminal 1)
cd backend && python run_stable.py

# Frontend (Terminal 2)
streamlit run main.py
```

### Docker Deployment
```dockerfile
# Coming soon - Docker support
```

### Cloud Deployment
- **Streamlit Cloud**: Deploy frontend with one click
- **Heroku/Railway**: Backend deployment
- **AWS/GCP**: Production scaling

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```
3. **Commit your changes**
```bash
git commit -m 'Add amazing feature'
```
4. **Push to the branch**
```bash
git push origin feature/amazing-feature
```
5. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black .
flake8
```

## 📋 Roadmap

- [ ] **v1.1**: Enhanced NLP models
- [ ] **v1.2**: Real-time collaboration
- [ ] **v1.3**: Advanced ATS optimization
- [ ] **v2.0**: Multi-language support
- [ ] **v2.1**: Interview question generator
- [ ] **v2.2**: Career path recommendations

## 🐛 Troubleshooting

### Common Issues

1. **Server not connecting**
   - Check if backend is running on port 5000
   - Verify all dependencies are installed

2. **File upload issues**
   - Ensure file size < 16MB
   - Check file format (PDF/DOCX/TXT)

3. **Analysis errors**
   - Verify resume text is extractable
   - Check backend logs for details

### Debug Mode
```bash
# Backend with debug info
cd backend && python app.py

# Frontend with debug
streamlit run main.py --logger.level=debug
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SpaCy** for excellent NLP capabilities
- **Streamlit** for amazing rapid prototyping
- **Plotly** for beautiful visualizations
- **OpenAI** for inspiration in AI applications

## 📞 Support

- **Documentation**: [Docs](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/resume-vision-ai/issues)
- **Email**: adithya.tb.24@gmail.com
- **Portfilio**: [Know about me](https://adithya-portfilo.vercel.app/)

## 🏆 Contributors

<a href="https://github.com/AdithyaTB/ResumeAnalyzer-RAG/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ResumeAnalyzer-RAG.git/ResumeAnalyzer-RAG.git" />
</a>

---

<div align="center">

**Made with ❤️ by the ResumeVision AI Team**

[![Star History Chart](https://api.star-history.com/svg?repos=AdithyaTB/resume-vision-ai&type=Date)](https://star-history.com/#your-username/resume-vision-ai&Date)

*If this project helps you, please give it a ⭐!*

</div>

