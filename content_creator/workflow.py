from typing import Dict, List, TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from .nodes import (
    ContentState,
    day_planner_node,
    content_generator_node,
    formatter_node,
    save_node
)
import pandas as pd

class ContentCreatorWorkflow:
    """Workflow for generating a social media content plan."""
    
    def __init__(self, brand_theme: str, days: int = 30):
        """Initialize the workflow with brand theme and number of days."""
        self.brand_theme = brand_theme
        self.days = days
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build and configure the LangGraph workflow."""
        # Create a new graph
        workflow = StateGraph(ContentState)
        
        # Define the nodes
        workflow.add_node("day_planner", day_planner_node)
        workflow.add_node("content_generator", content_generator_node)
        workflow.add_node("formatter", formatter_node)
        workflow.add_node("save", save_node)
        
        # Define the edges
        workflow.add_edge("day_planner", "content_generator")
        workflow.add_edge("content_generator", "formatter")
        workflow.add_edge("formatter", "save")
        workflow.add_edge("save", END)
        
        # Set the entry point
        workflow.set_entry_point("day_planner")
        
        # Compile the workflow
        return workflow.compile()
    
    def run(self) -> Dict:
        """Run the workflow and return the result."""
        # Initialize the state
        initial_state = {
            "brand_theme": self.brand_theme,
            "days": self.days,
            "topics": [],
            "content_plan": []
        }
        
        # Run the workflow
        result = self.workflow.invoke(initial_state)
        
        return result

def save_to_csv(content_plan: List[Dict[str, str]], filename: str = "content_calendar.csv") -> None:
    """Save the content plan to a CSV file."""
    if not content_plan:
        raise ValueError("Content plan is empty")
    
    # Convert to DataFrame
    df = pd.DataFrame(content_plan)
    
    # Reorder columns to match the required format
    df = df[['Day', 'Topic', 'Caption', 'Hashtags']]
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Content plan saved to {filename}")

def generate_content_plan(brand_theme: str, days: int = 30) -> Dict:
    """
    Generate a content plan for the given brand theme and number of days.
    
    Args:
        brand_theme: The main theme for the content (e.g., "Fitness for Busy Professionals")
        days: Number of days to generate content for (default: 30)
        
    Returns:
        Dict containing the generated content plan
    """
    # Initialize and run the workflow
    workflow = ContentCreatorWorkflow(brand_theme, days)
    result = workflow.run()
    
    # Save to CSV
    if result.get("content_plan"):
        save_to_csv(result["content_plan"])
    
    return result
