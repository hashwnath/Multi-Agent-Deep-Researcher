# Multi-Agent-Deep-Researcher
<img width="2515" height="1200" alt="architecture diagram" src="https://github.com/user-attachments/assets/4fc74b61-9faf-4f63-979f-e8ce3869adaf" />

A sophisticated multi-type research and analysis system that combines web content extraction, PDF processing, and specialized domain research to provide comprehensive insights across various research domains.

## 🚀 Features

### **Multi-Domain Research Capabilities**
- **Developer Tools Research**: Analyze development tools, APIs, and technologies
- **Product Research**: Compare products, features, and alternatives
- **Educational Research**: Evaluate institutions, programs, and courses
- **Financial Research**: Analyze stocks, companies, and market trends
- **Technical Documentation**: Review APIs, SDKs, and technical specifications
- **Industry Research**: Study market trends, competitors, and industry analysis
- **General Research**: Fallback for uncategorized queries

### **Intelligent Content Processing**
- **Web Content Extraction**: Advanced web scraping and content analysis
- **PDF Document Processing**: Intelligent PDF analysis with relevance scoring
- **Entity Extraction**: Automated identification of companies, products, and technologies
- **Context-Aware Analysis**: Domain-specific insights and recommendations

### **Flexible PDF Integration**
- **PDF Selection Options**:
  - Auto-select relevant PDFs
  - Manual PDF selection
  - Relevance-based PDF ranking
- **S3 Integration**: Secure PDF storage and retrieval
- **Relevance Scoring**: Intelligent PDF filtering based on query context

### **Specialized Output Formatting**
Each research type provides tailored output with domain-specific metrics and insights.

## 🏗️ Architecture

The system uses a multi-agent architecture with specialized nodes for different research types:

- **Intent Detection Agent**: Classifies research queries
- **Content Extraction Agent**: Processes web content
- **PDF Processing Agent**: Analyzes PDF documents
- **Specialized Research Agents**: Domain-specific analysis
- **Analysis & Synthesis Agent**: Combines insights and generates recommendations

## 📋 Prerequisites

- Python 3.8+
- AWS S3 access (for PDF storage)
- Required API keys (configured via environment variables)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Advanced-Research-Agent
   ```

2. **Install dependencies**
   ```bash
   cd advanced-agent
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
# API Keys
ANTHROPIC_API_KEY=your_anthropic_key
FIRECRAWL_API_KEY=your_firecrawl_key

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-2
S3_BUCKET_NAME=your_bucket_name

# Application Settings
MAX_ENTITIES=10
MAX_PDFS=5
```

## 🎯 Usage

### **Basic Research**
```bash
python main.py
```

### **Research Options**
1. **Regular Research**: Auto-selects relevant PDFs
2. **Select Specific PDFs**: Choose specific PDFs for analysis
3. **Find Relevant PDFs**: Rank PDFs by relevance to query

### **Example Queries**
- "Best tools to build AI agents"
- "Compare Python web frameworks"
- "Top universities for computer science"
- "Stock analysis for tech companies"
- "API documentation for payment processing"

## 📊 Output Examples

### **Developer Tools Research**
```
1. 🏢 LangChain
   🌐 Website: https://langchain.com
   💰 Pricing: Freemium
   📖 Open Source: Yes
   🛠️ Tech Stack: Python, JavaScript, TypeScript
   💻 Language Support: Python, JavaScript, TypeScript
   🔌 API: ✅ Available
   🔗 Integrations: OpenAI, Anthropic, Pinecone
```

### **Product Research**
```
1. 📱 ChatGPT
   🏷️ Category: AI Assistant
   🌐 Website: https://chat.openai.com
   💰 Price: Free + Premium
   ⭐ Rating: 4.8/5
   ✨ Features: Natural language processing, Code generation
   🎯 Target: Developers, Content creators
```

## 🔒 Security

- Environment variables for sensitive configuration
- AWS IAM roles for S3 access
- Secure API key management
- No hardcoded credentials in source code

## 📁 Project Structure

```
Advanced-Research-Agent/
├── advanced-agent/
│   ├── main.py                 # Main application entry point
│   ├── src/
│   │   ├── workflow.py         # Workflow orchestration
│   │   ├── models.py           # Data models
│   │   ├── prompts.py          # LLM prompts
│   │   ├── firecrawl.py        # Web content extraction
│   │   ├── pdf_notetaker.py    # PDF processing
│   │   └── s3_pdf_service.py   # S3 PDF management
│   ├── pyproject.toml          # Project configuration
│   └── README.md               # Agent-specific documentation
├── simple-agent/               # Simplified version
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) for LLM orchestration
- Uses [Anthropic Claude](https://www.anthropic.com/) for AI analysis
- Powered by [Firecrawl](https://firecrawl.dev/) for web content extraction
- PDF processing with [pdfplumber](https://github.com/jsvine/pdfplumber) and [PyPDF2](https://pypdf2.readthedocs.io/)

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

**Note**: This is a research and development tool. Please ensure compliance with relevant terms of service and data privacy regulations when using third-party APIs and services. 
