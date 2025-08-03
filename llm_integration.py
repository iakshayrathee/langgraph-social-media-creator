#!/usr/bin/env python3
"""
Open-source LLM integration for enhanced content generation.
Uses llama-cpp-python for local LLM inference.
"""
import os
import json
from typing import List, Dict, Optional
from llama_cpp import Llama

class LLMContentGenerator:
    """Enhanced content generator using open-source LLMs."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the LLM content generator.
        
        Args:
            model_path: Path to the GGUF model file. If None, will use rule-based fallback.
        """
        self.llm = None
        self.model_path = model_path
        self.use_llm = False
        
        if model_path and os.path.exists(model_path):
            try:
                print(f"🤖 Loading LLM model from: {model_path}")
                self.llm = Llama(
                    model_path=model_path,
                    n_ctx=2048,  # Context window
                    n_threads=4,  # CPU threads
                    verbose=False
                )
                self.use_llm = True
                print("✅ LLM model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Failed to load LLM model: {e}")
                print("🔄 Falling back to rule-based generation")
                self.use_llm = False
        else:
            print("📝 Using rule-based content generation (no LLM model specified)")
    
    def generate_topics_with_llm(self, theme: str, num_days: int = 30) -> List[str]:
        """Generate topics using LLM."""
        if not self.use_llm:
            return self._fallback_topics(theme, num_days)
        
        prompt = f"""Generate {num_days} unique and engaging social media content topics for the theme: "{theme}".

Requirements:
- Each topic should be specific and actionable
- Topics should be relevant to the target audience
- Vary the content types (tips, questions, behind-the-scenes, educational, etc.)
- Keep topics concise (2-6 words each)

Format your response as a JSON array of strings, like this:
["Topic 1", "Topic 2", "Topic 3", ...]

Topics for "{theme}":\n"""

        try:
            response = self.llm(
                prompt,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                stop=["</s>", "\n\n\n"]
            )
            
            # Extract and parse the response
            response_text = response['choices'][0]['text'].strip()
            
            # Try to extract JSON array from response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                topics_json = json_match.group()
                topics = json.loads(topics_json)
                
                # Validate and clean topics
                clean_topics = []
                for topic in topics[:num_days]:
                    if isinstance(topic, str) and len(topic.strip()) > 0:
                        clean_topics.append(topic.strip())
                
                if len(clean_topics) >= num_days // 2:  # At least half the topics
                    return clean_topics[:num_days]
            
        except Exception as e:
            print(f"⚠️ LLM topic generation failed: {e}")
        
        # Fallback to rule-based
        return self._fallback_topics(theme, num_days)
    
    def generate_caption_with_llm(self, topic: str, theme: str) -> str:
        """Generate caption using LLM."""
        if not self.use_llm:
            return self._fallback_caption(topic, theme)
        
        prompt = f"""Create an engaging social media caption for the topic "{topic}" within the theme "{theme}".

Requirements:
- 1-2 sentences maximum
- Include relevant emojis (2-4 emojis)
- Be conversational and engaging
- Encourage interaction
- Match the tone appropriate for the theme
- Don't include hashtags (they will be added separately)

Caption for "{topic}" ({theme}):\n"""

        try:
            response = self.llm(
                prompt,
                max_tokens=150,
                temperature=0.8,
                top_p=0.9,
                stop=["</s>", "\n\n", "Caption for"]
            )
            
            caption = response['choices'][0]['text'].strip()
            
            # Clean up the caption
            if caption and len(caption) > 10:
                # Remove any hashtags that might have been generated
                caption = ' '.join([word for word in caption.split() if not word.startswith('#')])
                return caption
            
        except Exception as e:
            print(f"⚠️ LLM caption generation failed: {e}")
        
        # Fallback to rule-based
        return self._fallback_caption(topic, theme)
    
    def generate_hashtags_with_llm(self, topic: str, theme: str) -> str:
        """Generate hashtags using LLM."""
        if not self.use_llm:
            return self._fallback_hashtags(topic, theme)
        
        prompt = f"""Generate 5 relevant hashtags for a social media post about "{topic}" in the "{theme}" niche.

Requirements:
- Exactly 5 hashtags
- Mix of broad and specific tags
- No spaces in hashtags
- Include the # symbol
- Separate with spaces

Hashtags for "{topic}" ({theme}):\n"""

        try:
            response = self.llm(
                prompt,
                max_tokens=100,
                temperature=0.6,
                top_p=0.8,
                stop=["</s>", "\n\n"]
            )
            
            hashtags = response['choices'][0]['text'].strip()
            
            # Validate and clean hashtags
            if hashtags:
                # Extract hashtags using regex
                import re
                hashtag_matches = re.findall(r'#\w+', hashtags)
                if len(hashtag_matches) >= 3:
                    return ' '.join(hashtag_matches[:5])
            
        except Exception as e:
            print(f"⚠️ LLM hashtag generation failed: {e}")
        
        # Fallback to rule-based
        return self._fallback_hashtags(topic, theme)
    
    def _fallback_topics(self, theme: str, num_days: int) -> List[str]:
        """Fallback rule-based topic generation."""
        from content_creator.nodes import generate_topic_ideas
        return generate_topic_ideas(theme, num_days)
    
    def _fallback_caption(self, topic: str, theme: str) -> str:
        """Fallback rule-based caption generation."""
        from content_creator.nodes import generate_caption
        return generate_caption(topic, theme)
    
    def _fallback_hashtags(self, topic: str, theme: str) -> str:
        """Fallback rule-based hashtag generation."""
        from content_creator.nodes import generate_hashtags
        return generate_hashtags(topic, theme)

def download_sample_model():
    """
    Download a small sample model for demonstration.
    This is optional and users can provide their own models.
    """
    import urllib.request
    import os
    
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    # Example: TinyLlama model (small for demonstration)
    model_url = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    model_path = os.path.join(model_dir, "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
    
    if not os.path.exists(model_path):
        print(f"📥 Downloading sample model to {model_path}")
        print("⏳ This may take a few minutes...")
        try:
            urllib.request.urlretrieve(model_url, model_path)
            print("✅ Model downloaded successfully!")
            return model_path
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return None
    else:
        print(f"✅ Model already exists at {model_path}")
        return model_path

def create_llm_generator(model_path: Optional[str] = None, auto_download: bool = False) -> LLMContentGenerator:
    """
    Create an LLM content generator.
    
    Args:
        model_path: Path to GGUF model file
        auto_download: Whether to auto-download a sample model if none provided
        
    Returns:
        LLMContentGenerator instance
    """
    if not model_path and auto_download:
        model_path = download_sample_model()
    
    return LLMContentGenerator(model_path)

if __name__ == "__main__":
    # Demo usage
    print("🤖 LLM Content Generator Demo")
    
    # Create generator (will fallback to rule-based if no model)
    generator = create_llm_generator(auto_download=False)
    
    # Test topic generation
    theme = "Fitness for Busy Professionals"
    topics = generator.generate_topics_with_llm(theme, 5)
    print(f"\n📝 Generated topics for '{theme}':")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    # Test caption and hashtag generation
    if topics:
        topic = topics[0]
        caption = generator.generate_caption_with_llm(topic, theme)
        hashtags = generator.generate_hashtags_with_llm(topic, theme)
        
        print(f"\n💬 Sample content for '{topic}':")
        print(f"Caption: {caption}")
        print(f"Hashtags: {hashtags}")
