# Duck

An AI-powered podcast generation system that creates complete podcast episodes from user queries.

**Inspired by NotebookLM** - designed for minimal prompts on any topic possible.

## Overview

This project contains two main components:

### 🎙️ Pipeline (`pipeline/`)
Complete automated podcast generation pipeline with Gradio interface.

**Features:**
- Intent analysis and research
- Script generation 
- Audio generation with Hume AI
- Single interface for end-to-end podcast creation

### 🔍 Web Research (`duckduckgo_crawl/`)
Web scraping components for augmenting LLM responses with real-time data.

**Status:** Work in progress - future enhancement for beyond knowledge cutoff information.

## Quick Start

1. **Main Pipeline:**
```bash
cd pipeline/
pip install -r requirements.txt
gradio podcast_pipeline.py
```

2. **Environment Setup:**
Create a `.env` file with two required API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
HUME_API_KEY=your_hume_api_key_here
```

### TTS Alternatives
These alternatives were considered and experimented with:

- **DIA TTS**: Good for shorter dialogues (under 20 seconds) with hyperrealistic voices
- **Parler TTS**: Excellent for short content with high-quality output
- **ElevenLabs**: Best quality but expensive - premium option
- **Hume AI**: Chosen for best quality and pricing balance

You can incorporate whatever TTS service you prefer by modifying the audio generator.

### LLM Model Options
OpenAI LLMs and Hume are used. Other LLMs were experimented with but decided to go with these.

### Web Research Enhancement
The `duckduckgo_crawl/` components can be integrated to augment LLM responses with real-time data beyond knowledge cutoff (WIP).

## Usage
Free to use and modify in any way deemed fit.
