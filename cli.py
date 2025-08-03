#!/usr/bin/env python3
"""
Command-line interface for the Social Media Content Creator Agent.
"""
import argparse
import sys
from content_creator.workflow import generate_content_plan

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a social media content plan based on a theme."
    )
    
    parser.add_argument(
        "theme",
        type=str,
        help="The main theme for the content (e.g., 'Fitness for Busy Professionals')"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to generate content for (default: 30)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="content_calendar.csv",
        help="Output CSV file path (default: content_calendar.csv)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    
    print(f"Generating {args.days}-day content plan for theme: {args.theme}")
    print("This may take a moment...\n")
    
    try:
        # Generate the content plan
        result = generate_content_plan(args.theme, args.days)
        
        # Print a preview of the generated content
        if result.get("content_plan"):
            print("\nSuccessfully generated content plan!")
            print(f"Preview of the first 3 days:")
            print("-" * 50)
            
            for day in result["content_plan"][:3]:
                print(f"Day {day['Day']}: {day['Topic']}")
                print(f"Caption: {day['Caption']}")
                print(f"Hashtags: {day['Hashtags']}")
                print("-" * 50)
            
            print(f"\nFull content plan has been saved to {args.output}")
        else:
            print("No content plan was generated. Please check the input parameters.")
            sys.exit(1)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
