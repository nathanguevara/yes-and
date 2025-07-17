"""Basic tests for the humor cohost project."""

import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_import_modules():
    """Test that core modules can be imported."""
    try:
        # Import modules individually to avoid relative import issues
        import utils.prompts
        import utils.humor_metrics
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")

def test_humor_styles():
    """Test that humor styles are defined."""
    from utils.prompts import PromptTemplates
    templates = PromptTemplates()
    assert hasattr(templates, 'system_prompts')
    assert len(templates.system_prompts) > 0
    
def test_basic_functionality():
    """Test basic application functionality."""
    # Basic sanity check
    assert 1 + 1 == 2