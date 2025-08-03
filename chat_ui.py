#!/usr/bin/env python3
"""
Simple Gradio Chat UI using the existing LangGraph workflow.
No LLM dependencies required - uses rule-based generation.
"""
import gradio as gr
import pandas as pd
import os
from typing import Tuple
from content_creator.workflow import generate_content_plan

def create_content_plan_interface(brand_theme: str, days: int = 30) -> Tuple[str, str]:
    """Generate content plan using the existing LangGraph workflow."""
    try:
        if not brand_theme.strip():
            return "❌ Please enter a brand theme!", ""
        
        result = generate_content_plan(brand_theme.strip(), days)
        
        if not result.get("content_plan"):
            return "❌ Failed to generate content plan. Please try again.", ""
        
        df = pd.DataFrame(result["content_plan"])
        
        # Show first 5 rows as preview
        preview_df = df.head(5)
        preview_text = preview_df.to_string(index=False)
        
        success_msg = f"""✅ **Successfully generated {days}-day content plan for "{brand_theme}"!**

🔧 **Generation Method:** 📝 Rule-Based (LangGraph Workflow)
📊 **Preview (First 5 days):**
```
{preview_text}
```

📁 **Full plan saved to:** `content_calendar.csv`
📈 **Total entries:** {len(result["content_plan"])} days
🎯 **Theme:** {brand_theme}

You can download the complete CSV file below!"""
        
        return success_msg, df.to_csv(index=False)
        
    except Exception as e:
        error_msg = f"❌ **Error generating content plan:** {str(e)}"
        return error_msg, ""

def create_simple_gradio_interface():
    """Create and configure the simple Gradio interface."""
    
    css = """
    /* Fix full-screen layout issues */
    body {
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }
    
    .gradio-container {
        max-width: 100vw !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Remove Gradio's default container margins */
    .gradio-container > .contain {
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .gradio-container .block {
        margin: 0 !important;
        border-radius: 0 !important;
    }
    
    .gradio-container .gap {
        gap: 0 !important;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white;
        padding: 2rem;
        border-radius: 0;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        position: relative;
        overflow: hidden;
        margin: 0;
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .header h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header p {
        font-size: 1rem;
        color: white !important;
        opacity: 0.95;
        margin: 0.3rem 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .header p:last-child {
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.8rem;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.15);
        border-radius: 20px;
        display: inline-block;
        backdrop-filter: blur(10px);
    }
    
    /* Main content styling - work with Gradio's default layout */
    .main-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        min-height: calc(100vh - 200px) !important;
        height: 100% !important;
        align-items: stretch !important;
    }
    
    .input-card, .output-card {
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 2rem !important;
    }
    
    .input-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-right: 2px solid #e2e8f0;
    }
    
    .output-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    .output-content {
        flex-grow: 1;
        overflow-y: auto;
        margin-bottom: 1rem !important;
    }
    
    /* Enhanced input styling - preserve functionality */
    .gradio-textbox textarea,
    .gradio-textbox input {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .gradio-textbox textarea:focus,
    .gradio-textbox input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    /* Enhanced button styling */
    button.primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    button.primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Slider enhancement */
    input[type="range"] {
        accent-color: #6366f1;
    }
    
    /* Info cards */
    .info-card {
        background: white;
        padding: 1.5rem !important;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef);
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .info-card h4 {
        color: #1e293b !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin: 0 0 1rem 0 !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-card p {
        color: #475569 !important;
        line-height: 1.6 !important;
        margin: 0.5rem 0 !important;
        font-size: 0.9rem !important;
    }
    
    .info-card p strong {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Output area styling */
    .output-content {
        background: white;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 2rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        min-height: 300px;
        position: relative;
        overflow: hidden;
    }
    
    .output-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #3b82f6, #6366f1);
    }
    
    /* File download styling */
    .gradio-file {
        border-radius: 12px !important;
        border: 2px dashed #6366f1 !important;
        background: rgba(99, 102, 241, 0.05) !important;
        padding: 1rem !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white !important;
        padding: 2rem !important;
        border-radius: 0;
        position: relative;
        overflow: hidden;
        flex-shrink: 0;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.05) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .footer h4 {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin: 0 0 0.5rem 0 !important;
        color: white !important;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .footer p {
        font-size: 0.95rem !important;
        color: white !important;
        opacity: 0.95;
        margin: 0.5rem 0 !important;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .footer p:last-child {
        margin-top: 1rem !important;
        font-size: 1rem !important;
        font-weight: 500;
    }
    
    /* Enhanced section headers */
    h3 {
        color: #1e293b;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #6366f1;
        position: relative;
    }
    
    h3::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, #d946ef);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .input-card,
        .output-card {
            padding: 1rem;
        }
        
        .header h1 {
            font-size: 1.5rem;
        }
        
        .header p {
            font-size: 0.9rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
    }
    """
    
    with gr.Blocks(css=css, title="Content Creator") as interface:
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🚀 Social Media Content Creator</h1>
            <p>Generate professional content plans with AI-powered LangGraph workflow</p>
            <p>📝 Rule-Based Generation • 🤖 No API Keys Required • 📊 CSV Export</p>
        </div>
        """)
        
        # Main content grid - full height columns
        with gr.Row(elem_classes=["main-grid"]):
            with gr.Column(scale=1, elem_classes=["input-card"]):
                gr.Markdown("### 🎯 Content Configuration")
                
                brand_theme = gr.Textbox(
                    label="🎯 Brand Theme & Focus Area",
                    placeholder="Enter your specific brand theme or niche (e.g., 'Fitness for Busy Professionals', 'AI Tools for Small Business', 'Mental Health for Students')",
                    lines=3,
                    info="Be specific about your target audience and content focus for better results"
                )
                
                days = gr.Slider(
                    minimum=7,
                    maximum=90,
                    value=30,
                    step=1,
                    label="📅 Content Calendar Duration",
                    info="Choose how many days of content you want to generate (7-90 days)"
                )
                
                generate_btn = gr.Button(
                    "🚀 Generate Content Plan",
                    variant="primary",
                    size="lg"
                )
                
                # Enhanced info sections
                gr.HTML("""
                <div class="info-card">
                    <h4>💡 Popular Theme Examples</h4>
                    <p><strong>🏋️ Fitness & Health:</strong> "Home Workout Tips", "Nutrition for Athletes", "Mental Wellness"</p>
                    <p><strong>💼 Business & Leadership:</strong> "Startup Growth Hacks", "Remote Team Management", "Sales Strategies"</p>
                    <p><strong>💻 Technology & AI:</strong> "AI Tools for Business", "Coding Best Practices", "Tech Trends 2024"</p>
                    <p><strong>🎨 Creative & Lifestyle:</strong> "Digital Art Tips", "Photography Basics", "Travel Hacking"</p>
                </div>
                """)
                
            
            with gr.Column(scale=1, elem_classes=["output-card"]):
                gr.Markdown("### 📊 Generated Content Plan")
                
                output_message = gr.Markdown(
                    """### 🎯 Ready to Generate Your Content Calendar!
                    
**What you'll get:**
- 📝 Daily content topics tailored to your theme
- 💬 Professional captions with engaging copy
- 🏷️ Optimized hashtags for better reach
- 📊 Structured CSV format for easy planning

**Instructions:**
1. Enter your specific brand theme in the left panel
2. Choose your desired content duration (7-90 days)
3. Click the generate button to create your plan
4. Download the CSV file for your content calendar

*Your generated content will appear here once ready!*""",
                    container=False
                )
                
                csv_output = gr.File(
                    label="📁 Download CSV",
                    visible=False
                )
                
                # Enhanced technical and feature details
                gr.HTML("""
                <div class="info-card">
                    <h4>🔧 Advanced Features</h4>
                    <p><strong>🤖 AI Workflow:</strong> LangGraph with 4 specialized nodes (Planner → Generator → Formatter → Saver)</p>
                    <p><strong>📊 Output Format:</strong> Professional CSV with Day, Topic, Caption, and Hashtags columns</p>
                    <p><strong>🎯 Smart Categories:</strong> 4 main themes + intelligent fallback for custom topics</p>
                    <p><strong>⚡ Performance:</strong> Generates 30-day plans in under 10 seconds</p>
                </div>
                """)
        
        # Event handlers
        def generate_and_save(theme: str, num_days: int):
            """Generate content plan and prepare file for download."""
            message, csv_content = create_content_plan_interface(theme, num_days)
            
            if csv_content:
                # Sanitize the theme for filename - remove invalid characters
                import re
                sanitized_theme = re.sub(r'[^\w\s-]', '', theme.strip())  # Remove special chars
                sanitized_theme = re.sub(r'[\s\n\r\t]+', '_', sanitized_theme)  # Replace whitespace/newlines with underscore
                sanitized_theme = sanitized_theme.lower()[:50]  # Limit length and convert to lowercase
                
                temp_filename = f"content_plan_{sanitized_theme}_{num_days}days.csv"
                temp_path = os.path.join(os.getcwd(), temp_filename)
                
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)
                
                return message, gr.File(value=temp_path, visible=True)
            else:
                return message, gr.File(visible=False)
        
        generate_btn.click(
            fn=generate_and_save,
            inputs=[brand_theme, days],
            outputs=[output_message, csv_output]
        )
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <h4>🏆 Enterprise-Grade Content Creation</h4>
            <p>🔧 LangGraph Workflow • 🤖 AI-Powered • 📊 Professional Output • 🚀 Zero Setup</p>
            <p>Transform your content strategy with intelligent automation. Generate months of content in minutes.</p>
        </div>
        """)
    
    return interface

def main():
    """Launch the simple Gradio chat interface."""
    print("🚀 Starting Social Media Content Creator Chat UI...")
    print("📝 Using rule-based generation with LangGraph workflow")
    print("📱 This will open in your default web browser")
    print("🌐 Local access: http://localhost:7860")
    
    interface = create_simple_gradio_interface()
    
    interface.launch(
        server_name="127.0.0.1",  # Use localhost for proper URL display
        server_port=7860,         # Standard Gradio port
        share=True,               # Create public link for sharing
        show_error=True,          # Show detailed errors
        quiet=False,              # Show startup logs
        inbrowser=True            # Auto-open in browser
    )

if __name__ == "__main__":
    main()