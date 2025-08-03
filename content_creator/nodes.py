from typing import Dict, List, TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph
import random

class ContentState(TypedDict):
    """State for the content creation workflow."""
    brand_theme: str
    days: int
    topics: List[str]
    content_plan: List[Dict[str, str]]

def generate_topic_ideas(theme: str, num_days: int = 30) -> List[str]:
    """Generate topic ideas based on the brand theme."""
    # Comprehensive theme-based topic generation
    themes = {
        "Fitness": [
            "Morning Workout Routines", "Healthy Breakfast Ideas", "Office Stretches",
            "Quick Lunch Workouts", "Evening Relaxation Techniques", "Weekend Fitness Challenges",
            "Desk Yoga Poses", "Healthy Snack Ideas", "Posture Correction Exercises",
            "Lunch Break Walks", "Stair Workout Ideas", "Healthy Meal Prep Tips",
            "Standing Desk Exercises", "Mindfulness Practices", "Hydration Tips",
            "Quick Stretches for Back Pain", "Healthy Takeout Options", "Sleep Improvement Tips",
            "Stress Relief Exercises", "Healthy Dessert Recipes", "Commute Workout Ideas",
            "Healthy Grocery List", "Quick Workout for Busy Days", "Healthy Meal Swaps",
            "Deskercise Routines", "Healthy Office Snacks", "Lunch Break Meditation",
            "Healthy Drink Recipes", "Weekend Fitness Goals", "Recovery Techniques"
        ],
        "Mental": [
            "Daily Mindfulness Practices", "Stress Management Techniques", "Anxiety Coping Strategies",
            "Self-Care Sunday Ideas", "Meditation for Beginners", "Journaling Prompts",
            "Breathing Exercises", "Digital Detox Tips", "Positive Affirmations",
            "Sleep Hygiene Habits", "Gratitude Practice", "Boundary Setting",
            "Emotional Regulation", "Mindful Eating", "Nature Therapy Benefits",
            "Social Connection Tips", "Creative Expression", "Time Management",
            "Perfectionism Recovery", "Self-Compassion Exercises", "Mindful Communication",
            "Workplace Wellness", "Seasonal Affective Disorder", "Therapy Benefits",
            "Mental Health Myths", "Crisis Resources", "Support System Building",
            "Mindful Movement", "Cognitive Behavioral Techniques", "Mental Health First Aid"
        ],
        "Business": [
            "Morning Productivity Routines", "Time Management Hacks", "Networking Strategies",
            "Leadership Development", "Team Building Activities", "Goal Setting Frameworks",
            "Communication Skills", "Presentation Tips", "Email Etiquette",
            "Remote Work Best Practices", "Meeting Efficiency", "Delegation Techniques",
            "Conflict Resolution", "Innovation Strategies", "Customer Service Excellence",
            "Brand Building Tips", "Social Media Marketing", "Content Creation Ideas",
            "Financial Planning", "Investment Basics", "Entrepreneurship Mindset",
            "Work-Life Balance", "Professional Development", "Industry Trends",
            "Negotiation Skills", "Project Management", "Digital Marketing",
            "Sales Techniques", "Client Relationship Management", "Strategic Planning"
        ],
        "Technology": [
            "AI Tools for Productivity", "Cybersecurity Best Practices", "Cloud Computing Benefits",
            "Mobile App Development", "Web Design Trends", "Data Privacy Tips",
            "Social Media Security", "Digital Minimalism", "Tech for Seniors",
            "Automation Tools", "Programming Languages", "Tech Career Paths",
            "Gadget Reviews", "Software Recommendations", "Tech News Updates",
            "Digital Wellness", "Online Learning Platforms", "Tech Troubleshooting",
            "Future Tech Predictions", "Startup Tech Stack", "Open Source Tools",
            "Tech Accessibility", "Green Technology", "Blockchain Basics",
            "IoT Applications", "Virtual Reality Uses", "Machine Learning Intro",
            "Tech Ethics", "Digital Transformation", "Tech Community Building"
        ]
    }
    
    # Extract main theme keyword
    theme_lower = theme.lower()
    theme_key = None
    
    # Find matching theme
    for key in themes.keys():
        if key.lower() in theme_lower:
            theme_key = key
            break
    
    if theme_key and theme_key in themes:
        topics = themes[theme_key][:num_days]
        # If we need more topics than available, cycle through them
        while len(topics) < num_days:
            remaining = num_days - len(topics)
            topics.extend(themes[theme_key][:remaining])
        return topics[:num_days]
    
    # Enhanced fallback for unknown themes
    base_topics = [
        "Getting Started Guide", "Common Mistakes to Avoid", "Expert Tips",
        "Best Practices", "Tools and Resources", "Success Stories",
        "Troubleshooting Guide", "Advanced Techniques", "Industry Insights",
        "Trends and Updates", "Community Spotlight", "Q&A Session",
        "Behind the Scenes", "Case Study", "Tutorial Tuesday",
        "Myth Busting", "Quick Tips", "Deep Dive Analysis",
        "Beginner's Guide", "Pro Tips", "Weekly Roundup",
        "How-To Guide", "Comparison Review", "Future Predictions",
        "Personal Experience", "Lessons Learned", "Resource Recommendations",
        "Community Discussion", "Expert Interview", "Reflection Friday"
    ]
    
    topics = []
    for i in range(num_days):
        base_topic = base_topics[i % len(base_topics)]
        topics.append(f"{theme}: {base_topic}")
    
    return topics

def day_planner_node(state: ContentState) -> Dict[str, List[str]]:
    """Node to generate topic ideas for the content plan."""
    theme = state["brand_theme"]
    num_days = state.get("days", 30)
    
    topics = generate_topic_ideas(theme, num_days)
    return {"topics": topics}

def generate_caption(topic: str, theme: str) -> str:
    """Generate a caption for a given topic and theme."""
    theme_lower = theme.lower()
    
    # More diverse and engaging caption templates
    templates = [
        f"💡 {topic}: Your {theme_lower} game-changer! Ready to level up? Let's dive in! 🚀",
        f"🌟 Today's spotlight: {topic}. Small steps, big results in your {theme_lower} journey! ✨",
        f"🔥 {topic} - the secret sauce to crushing your {theme_lower} goals! Who's ready to try this? 💪",
        f"✨ Transform your routine with {topic}! Your future self will thank you 🙏 #{theme.replace(' ', '')}",
        f"🎯 Focus Friday: {topic}. Because consistency in {theme_lower} creates magic! ✨",
        f"💪 {topic} isn't just a tip - it's your pathway to {theme_lower} success! Let's go! 🚀",
        f"🌱 Growing stronger every day with {topic}. Your {theme_lower} journey matters! 💚",
        f"⚡ Power up your {theme_lower} with {topic}! Simple changes, powerful results 🔥",
        f"🎉 Celebrating progress with {topic}! Every step counts in your {theme_lower} story 📈",
        f"🧠 Smart strategy: {topic}. Work smarter, not harder in your {theme_lower} journey! 💡",
        f"🌈 Brighten your day with {topic}! Making {theme_lower} fun and sustainable 😊",
        f"⭐ Pro tip: {topic} is your secret weapon for {theme_lower} success! Ready to shine? ✨"
    ]
    
    caption = random.choice(templates)
    return caption

def generate_hashtags(topic: str, theme: str) -> str:
    """Generate relevant hashtags for a topic."""
    # Theme-specific hashtag pools
    theme_hashtags = {
        "fitness": ["FitnessMotivation", "HealthyLifestyle", "WorkoutTips", "FitLife", "HealthyHabits", "WellnessJourney"],
        "mental": ["MentalHealthMatters", "SelfCare", "Mindfulness", "WellnessWednesday", "MentalWellness", "SelfLove"],
        "business": ["BusinessTips", "Entrepreneurship", "Leadership", "ProductivityHacks", "BusinessGrowth", "Success"],
        "technology": ["TechTips", "Innovation", "DigitalLife", "TechTrends", "FutureTech", "TechCommunity"]
    }
    
    # General hashtags that work for any theme
    general_hashtags = ["Motivation", "Tips", "Growth", "Success", "Community", "Inspiration", "Goals", "Progress"]
    
    # Create base hashtags
    hashtags = []
    
    # Add theme-specific hashtag
    hashtags.append(theme.replace(" ", ""))
    
    # Add topic hashtag (cleaned)
    topic_clean = "".join(word.capitalize() for word in topic.replace("-", " ").split())
    if len(topic_clean) <= 20:  # Avoid overly long hashtags
        hashtags.append(topic_clean)
    
    # Add theme-specific hashtags
    theme_lower = theme.lower()
    for theme_key, theme_tags in theme_hashtags.items():
        if theme_key in theme_lower:
            hashtags.extend(random.sample(theme_tags, min(2, len(theme_tags))))
            break
    
    # Add general hashtags
    hashtags.extend(random.sample(general_hashtags, 2))
    
    # Remove duplicates and format
    unique_hashtags = list(dict.fromkeys([f"#{tag}" for tag in hashtags if tag and len(tag) > 2]))
    
    # Limit to 5 hashtags for optimal engagement
    return " ".join(unique_hashtags[:5])

def content_generator_node(state: ContentState) -> Dict[str, List[Dict[str, str]]]:
    """Node to generate captions and hashtags for each topic."""
    topics = state["topics"]
    theme = state["brand_theme"]
    
    content_plan = []
    for i, topic in enumerate(topics, 1):
        caption = generate_caption(topic, theme)
        hashtags = generate_hashtags(topic, theme)
        
        content_plan.append({
            "Day": i,
            "Topic": topic,
            "Caption": caption,
            "Hashtags": hashtags
        })
    
    return {"content_plan": content_plan}

def formatter_node(state: ContentState) -> Dict:
    """Node to format the content plan (placeholder for now)."""
    # This node is a pass-through in this implementation
    # but could be expanded for additional formatting
    return state

def save_node(state: ContentState) -> Dict:
    """Node to save the content plan to a CSV file."""
    # The actual saving will be handled in the workflow
    # This node just returns the state for now
    return state
