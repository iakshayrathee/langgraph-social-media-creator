# 📱 AI-Powered Social Media Content Generator

A LangGraph-based application for generating comprehensive social media content plans. This tool helps content creators, marketers, and businesses by automatically generating engaging content calendars with topics, captions, and hashtags based on any theme.

## ✨ Features

- 📅 Generate customizable content plans (7-90 days, default 30)
- 🎯 Theme-based topic generation with built-in content categories
- 💬 Engaging captions with emojis
- 🏷️ Relevant hashtags for social media engagement
- 📊 CSV export for easy integration with other tools
- 🔧 Built with LangGraph for modular workflow management

## 🏗️ Project Structure

```
.
├── content_creator/           # Core content generation logic
│   ├── __init__.py
│   ├── nodes.py              # LangGraph node definitions
│   └── workflow.py           # Main workflow implementation
├── chat_ui.py               # Gradio web interface
├── cli.py                   # Command-line interface
├── enhanced_workflow.py     # Extended workflow implementation
├── llm_integration.py       # LLM model handling
├── requirements.txt         # Project dependencies
└── test_all_features.py     # Test cases
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already cloned):
   ```bash
   git clone https://github.com/iakshayrathee/langgraph-social-media-creator.git
   cd langgraph-social-media-creator
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### 🌐 Web Interface

Launch the interactive web UI:

```bash
python chat_ui.py
```

Access the UI at: `http://localhost:7860`

### 💻 Command Line Interface

#### Basic Generation
```bash
python cli.py "Fitness for Busy Professionals" --days 30 --output my_content_plan.csv
```

**Arguments**:
- `theme`: The main theme for your content (required)
- `--days`: Number of days to generate content for (7-90, default: 30)
- `--output`: Output file path (default: content_calendar.csv)

### 🐍 Python API

#### Basic Usage
```python
from content_creator.workflow import generate_content_plan

# Generate 30-day content plan
result = generate_content_plan("Fitness for Busy Professionals", days=30)
print(f"Generated {len(result['content_plan'])} days of content!")

# Save to CSV
import pandas as pd
pd.DataFrame(result["content_plan"]).to_csv("my_content_plan.csv", index=False)
```

## Project Structure

- `content_creator/`: Main package
  - `nodes.py`: Contains the LangGraph nodes for content generation
  - `workflow.py`: Defines the LangGraph workflow
  - `__init__.py`: Package initialization
- `cli.py`: Command-line interface

Example entry:
```csv
Day,Topic,Caption,Hashtags
1,AI Job Market Trends 2025,The AI job market is evolving rapidly! 🚀 Here are the top trends to watch in 2025... #AITrends #FutureOfWork #AIJobs #CareerGrowth #TechCareers
```

## 🚀 Running the Application

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run the web UI: `python chat_ui.py`
3. Access at: `http://localhost:7860`

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_all_features.py
```

