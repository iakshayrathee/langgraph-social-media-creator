#!/usr/bin/env python3
"""
Enhanced workflow with optional LLM integration for better content generation.
"""
from typing import Dict, List, Optional
from content_creator.workflow import ContentCreatorWorkflow, save_to_csv
from llm_integration import LLMContentGenerator, create_llm_generator

class EnhancedContentCreatorWorkflow(ContentCreatorWorkflow):
    """Enhanced workflow with LLM integration capabilities."""
    
    def __init__(self, brand_theme: str, days: int = 30, model_path: Optional[str] = None, use_llm: bool = False):
        """
        Initialize enhanced workflow with optional LLM support.
        
        Args:
            brand_theme: The main theme for content generation
            days: Number of days to generate content for
            model_path: Path to GGUF model file for LLM integration
            use_llm: Whether to attempt using LLM for content generation
        """
        self.llm_generator = None
        if use_llm:
            print("🤖 Initializing LLM integration...")
            self.llm_generator = create_llm_generator(model_path)
        
        super().__init__(brand_theme, days)
    
    def generate_enhanced_content_plan(self) -> Dict:
        """Generate content plan with enhanced LLM capabilities."""
        print(f"🚀 Generating {self.days}-day content plan for: '{self.brand_theme}'")
        
        if self.llm_generator and self.llm_generator.use_llm:
            print("🤖 Using LLM-enhanced generation...")
            return self._generate_with_llm()
        else:
            print("📝 Using rule-based generation...")
            return self.run()
    
    def _generate_with_llm(self) -> Dict:
        """Generate content using LLM integration."""
        # Generate topics with LLM
        print("📋 Generating topics...")
        topics = self.llm_generator.generate_topics_with_llm(self.brand_theme, self.days)
        
        # Generate content for each topic
        print("💬 Generating captions and hashtags...")
        content_plan = []
        
        for i, topic in enumerate(topics, 1):
            print(f"  Processing day {i}: {topic}")
            
            # Generate caption and hashtags with LLM
            caption = self.llm_generator.generate_caption_with_llm(topic, self.brand_theme)
            hashtags = self.llm_generator.generate_hashtags_with_llm(topic, self.brand_theme)
            
            content_plan.append({
                "Day": i,
                "Topic": topic,
                "Caption": caption,
                "Hashtags": hashtags
            })
        
        return {
            "brand_theme": self.brand_theme,
            "days": self.days,
            "topics": topics,
            "content_plan": content_plan
        }

def generate_enhanced_content_plan(
    brand_theme: str, 
    days: int = 30, 
    model_path: Optional[str] = None, 
    use_llm: bool = False,
    output_file: str = "content_calendar.csv"
) -> Dict:
    """
    Generate an enhanced content plan with optional LLM integration.
    
    Args:
        brand_theme: The main theme for content generation
        days: Number of days to generate content for
        model_path: Path to GGUF model file for LLM integration
        use_llm: Whether to attempt using LLM for content generation
        output_file: Output CSV file name
        
    Returns:
        Dict containing the generated content plan
    """
    # Create enhanced workflow
    workflow = EnhancedContentCreatorWorkflow(
        brand_theme=brand_theme,
        days=days,
        model_path=model_path,
        use_llm=use_llm
    )
    
    # Generate content plan
    result = workflow.generate_enhanced_content_plan()
    
    # Save to CSV
    if result.get("content_plan"):
        save_to_csv(result["content_plan"], output_file)
        print(f"✅ Content plan saved to: {output_file}")
    
    return result

if __name__ == "__main__":
    # Demo with different modes
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Social Media Content Creator")
    parser.add_argument("theme", help="Brand theme for content generation")
    parser.add_argument("--days", type=int, default=30, help="Number of days")
    parser.add_argument("--model", help="Path to GGUF model file")
    parser.add_argument("--use-llm", action="store_true", help="Enable LLM integration")
    parser.add_argument("--output", default="content_calendar.csv", help="Output file")
    
    args = parser.parse_args()
    
    print("🎨 Enhanced Social Media Content Creator")
    print("=" * 50)
    
    # Generate content plan
    result = generate_enhanced_content_plan(
        brand_theme=args.theme,
        days=args.days,
        model_path=args.model,
        use_llm=args.use_llm,
        output_file=args.output
    )
    
    # Show summary
    if result.get("content_plan"):
        print(f"\n📊 Summary:")
        print(f"  Theme: {result['brand_theme']}")
        print(f"  Days: {result['days']}")
        print(f"  Topics generated: {len(result['content_plan'])}")
        print(f"  Output file: {args.output}")
        
        # Show preview
        print(f"\n📝 Preview (first 3 entries):")
        for entry in result["content_plan"][:3]:
            print(f"  Day {entry['Day']}: {entry['Topic']}")
            print(f"    Caption: {entry['Caption'][:60]}...")
            print(f"    Hashtags: {entry['Hashtags']}")
            print()
    else:
        print("❌ Failed to generate content plan")
