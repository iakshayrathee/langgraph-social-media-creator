# 📱 AI-Powered Social Media Content Generator

A sophisticated LangGraph-based agent for generating comprehensive social media content plans. This tool helps content creators, marketers, and businesses by automatically generating engaging content calendars with topics, captions, and hashtags based on any theme.

🌐 **Live Demo**: [https://langgraph-social-media-creator.onrender.com/](https://langgraph-social-media-creator.onrender.com/)

## ✨ Features

### Core Features
- 📅 Generate customizable content plans (7-90 days, default 30)
- 🎯 Theme-based topic generation with 4 built-in categories (Fitness, Mental Health, Business, Technology)
- 💬 Engaging captions with emojis and varied templates
- 🏷️ Relevant hashtags optimized for social media engagement
- 📊 Multiple export formats (CSV/JSON) for easy integration
- 🔧 Built with LangGraph for modular workflow management

### Advanced Features
- 🤖 **LLM Integration**: Optional open-source LLM support for enhanced content generation
- 🌐 **Chat UI**: Beautiful, responsive web interface built with Gradio
- 📱 **Multiple Interfaces**: Command-line, Python API, and web UI
- 🚀 **Easy Deployment**: One-click sharing with Gradio's built-in hosting

## 🏗️ Project Structure

```
root/
├── content_creator/           # Core content generation logic
│   ├── __init__.py
│   ├── nodes.py              # LangGraph node definitions
│   └── workflow.py           # Main workflow implementation
├── .gradio/                  # Gradio UI configuration
├── cli.py                    # Command-line interface
├── enhanced_workflow.py      # LLM-enhanced workflow
├── llm_integration.py        # LLM model handling and generation
├── requirements.txt          # Python dependencies
├── simple_chat_ui.py         # Web interface
└── test_all_features.py      # Test suite
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
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

4. **For LLM support** (optional):
   ```bash
   # Install additional requirements for LLM support
   pip install llama-cpp-python
   # Download a model (e.g., TinyLLaMA)
   python -m llama_cpp.server --model models/tinyllama.gguf
   ```

## 💻 Usage

### 🌐 Web Interface (Recommended)

Launch the interactive web UI:

```bash
python simple_chat_ui.py
```

**Features**:
- 🎨 Intuitive, responsive design
- 🔄 Real-time content generation
- 📱 Mobile-friendly interface
- 💾 Save and export functionality

Access the UI at: `http://localhost:7860`

### 💻 Command Line Interface

#### Basic Generation
```bash
python cli.py "Fitness for Busy Professionals" --days 30 --output my_content_plan.csv
```

#### Enhanced Generation with LLM
```bash
python enhanced_workflow.py "Mental Health for Gen Z" --days 30 --use-llm --model ./models/tinyllama.gguf
```

**Arguments**:
- `theme`: The main theme for your content (required)
- `--days`: Number of days to generate content for (7-90, default: 30)
- `--output`: Output file path (default: content_calendar.csv)
- `--format`: Output format: csv or json (default: csv)
- `--use-llm`: Enable LLM enhancement (enhanced_workflow.py only)
- `--model`: Path to GGUF model file (for LLM mode)

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

#### Enhanced Usage with LLM
```python
from enhanced_workflow import generate_enhanced_content_plan

# Generate with LLM enhancement
result = generate_enhanced_content_plan(
    brand_theme="Mental Health for Gen Z",
    days=30,
    use_llm=True,
    model_path="./models/tinyllama.gguf"
)

# Access the generated content
for day_content in result["content_plan"]:
    print(f"Day {day_content['Day']}: {day_content['Topic']}")
    print(f"Caption: {day_content['Caption']}")
    print(f"Hashtags: {day_content['Hashtags']}")
    print()
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

## 🤖 LLM Integration (Optional)

For enhanced content generation, you can use local LLM models in GGUF format:

1. Download a compatible model (e.g., TinyLLaMA, LLaMA 2)
2. Place the model file in the `models/` directory
3. Use the `--use-llm` flag with the path to your model

## 🚀 Deployment

### Local Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Run the web UI: `python simple_chat_ui.py`
3. Access at: `http://localhost:7860`

### Cloud Deployment (Gradio)
1. Create a free Hugging Face account
2. Upload this repository
3. Set up a Space with Gradio
4. Configure the Space to run `simple_chat_ui.py`

## 🧪 Testing

Run the test suite to verify all features:

```bash
python test_all_features.py
```
