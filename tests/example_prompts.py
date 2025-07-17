"""
Example prompts for testing the comedy cohost functionality.
These prompts cover different comedy styles and conversation scenarios.
"""

EXAMPLE_PROMPTS = [
    {
        "prompt": "Tell me about your worst day ever, but make it funny",
        "expected_style": "self-deprecating",
        "description": "Tests self-deprecating humor with personal storytelling"
    },
    
    {
        "prompt": "What's the deal with people who still use Internet Explorer?",
        "expected_style": "observational", 
        "description": "Tests observational comedy about everyday annoyances"
    },
    
    {
        "prompt": "I just got a promotion at work and I'm feeling pretty good about myself",
        "expected_style": "sarcastic",
        "description": "Tests sarcastic responses to positive news"
    },
    
    {
        "prompt": "Explain quantum physics like you're a stand-up comedian",
        "expected_style": "witty",
        "description": "Tests witty explanations of complex topics"
    },
    
    {
        "prompt": "My pet goldfish just learned how to drive",
        "expected_style": "absurd",
        "description": "Tests absurd humor with ridiculous scenarios"
    }
]

def get_test_prompts():
    """Return all example prompts for testing."""
    return EXAMPLE_PROMPTS

def get_prompt_by_style(style):
    """Get example prompts filtered by expected comedy style."""
    return [p for p in EXAMPLE_PROMPTS if p["expected_style"] == style]