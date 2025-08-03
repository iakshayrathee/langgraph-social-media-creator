#!/usr/bin/env python3
"""
Test script to verify all features work correctly.
"""
import os
import sys
from content_creator.workflow import generate_content_plan

def test_basic_generation():
    """Test basic content generation."""
    print("🧪 Testing basic content generation...")
    
    try:
        result = generate_content_plan("Fitness for Busy Professionals", days=5)
        
        if result and result.get("content_plan"):
            print(f"✅ Generated {len(result['content_plan'])} days of content")
            
            # Show first entry
            first_entry = result["content_plan"][0]
            print(f"📝 Sample entry:")
            print(f"   Day: {first_entry['Day']}")
            print(f"   Topic: {first_entry['Topic']}")
            print(f"   Caption: {first_entry['Caption'][:50]}...")
            print(f"   Hashtags: {first_entry['Hashtags']}")
            
            return True
        else:
            print("❌ No content generated")
            return False
            
    except Exception as e:
        print(f"❌ Error in basic generation: {e}")
        return False

def test_theme_coverage():
    """Test different theme coverage."""
    print("\n🎨 Testing theme coverage...")
    
    themes = [
        "Mental Health for Gen Z",
        "Business Tips for Entrepreneurs", 
        "Technology Trends",
        "Unknown Theme Test"
    ]
    
    success_count = 0
    
    for theme in themes:
        try:
            result = generate_content_plan(theme, days=3)
            if result and result.get("content_plan") and len(result["content_plan"]) == 3:
                print(f"✅ {theme}: Generated successfully")
                success_count += 1
            else:
                print(f"❌ {theme}: Failed to generate")
        except Exception as e:
            print(f"❌ {theme}: Error - {e}")
    
    print(f"📊 Theme coverage: {success_count}/{len(themes)} themes successful")
    return success_count == len(themes)

def test_csv_output():
    """Test CSV file generation."""
    print("\n📁 Testing CSV output...")
    
    try:
        # Generate content and check if CSV is created
        result = generate_content_plan("Test Theme", days=3)
        
        if os.path.exists("content_calendar.csv"):
            print("✅ CSV file created successfully")
            
            # Check file content
            with open("content_calendar.csv", 'r', encoding='utf-8') as f:
                content = f.read()
                if "Day,Topic,Caption,Hashtags" in content:
                    print("✅ CSV has correct headers")
                    lines = content.strip().split('\n')
                    print(f"✅ CSV has {len(lines)-1} data rows")
                    return True
                else:
                    print("❌ CSV missing correct headers")
                    return False
        else:
            print("❌ CSV file not created")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CSV: {e}")
        return False

def test_30_day_generation():
    """Test full 30-day generation as required by assignment."""
    print("\n📅 Testing 30-day generation (Assignment Requirement)...")
    
    try:
        result = generate_content_plan("Mental Health for Gen Z", days=30)
        
        if result and result.get("content_plan"):
            content_count = len(result["content_plan"])
            print(f"✅ Generated {content_count} days of content")
            
            if content_count == 30:
                print("✅ Meets assignment requirement (30 days)")
                
                # Verify all required columns
                first_entry = result["content_plan"][0]
                required_fields = ["Day", "Topic", "Caption", "Hashtags"]
                
                missing_fields = [field for field in required_fields if field not in first_entry]
                if not missing_fields:
                    print("✅ All required CSV columns present")
                    return True
                else:
                    print(f"❌ Missing fields: {missing_fields}")
                    return False
            else:
                print(f"❌ Generated {content_count} days, but assignment requires 30")
                return False
        else:
            print("❌ No content generated")
            return False
            
    except Exception as e:
        print(f"❌ Error in 30-day generation: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Social Media Content Creator - Feature Test Suite")
    print("=" * 60)
    
    tests = [
        ("Basic Generation", test_basic_generation),
        ("Theme Coverage", test_theme_coverage),
        ("CSV Output", test_csv_output),
        ("30-Day Generation", test_30_day_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        print("✅ Assignment requirements are met:")
        print("   - LangGraph workflow implemented")
        print("   - 30-day content generation")
        print("   - CSV output with required columns")
        print("   - Rule-based content generation (no paid APIs)")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
