"""
Prompts package for podcast content generation
"""

from .intent_analysis import INTENT_ANALYSIS_PROMPT
from .research import RESEARCH_PROMPT
from .podcast_script import PODCAST_SCRIPT_PROMPT

__all__ = [
    'INTENT_ANALYSIS_PROMPT',
    'RESEARCH_PROMPT',
    'PODCAST_SCRIPT_PROMPT'
]