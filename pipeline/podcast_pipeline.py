"""
Complete Podcast Pipeline - Single Gradio Interface
Takes user input and generates podcast audio through all steps automatically
"""

import gradio as gr
import os
import json
import openai
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from prompts import INTENT_ANALYSIS_PROMPT, RESEARCH_PROMPT, PODCAST_SCRIPT_PROMPT
from audio_generator import generate_audio_from_script

# Load environment variables
load_dotenv()


def analyze_intent(query: str, user_profile: str = "") -> dict:
    """Step 1: Analyze user intent and extract structured data"""
    print(f"Step 1: Analyzing intent for: {query}")
    
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Format the prompt with current date and user input
        current_date = datetime.now().strftime("%Y-%m-%d")
        prompt = INTENT_ANALYSIS_PROMPT.format(current_date=current_date, user_query=query)
        
        if user_profile:
            prompt += f"\n\nUSER PROFILE: {user_profile}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            max_completion_tokens=800
        )
        
        response_text = response.choices[0].message.content.strip()
        print("Step 1 completed: Intent analysis generated")
        
        # Parse the response to extract structured data
        step1_data = {
            "query": query,
            "user_profile": user_profile,
            "raw_response": response_text,
            "primary_categories": "Unknown",
            "timeline": "Unknown", 
            "depth": "Unknown",
            "recency_level": "SHORT_TERM",
            "data_sources": "HISTORICAL",
            "search_strategy": "Unknown",
            "mood_tone": "CASUAL",
            "notes": "Analysis completed"
        }
        
        # Try to parse structured data from response
        try:
            lines = response_text.split('\n')
            for line in lines:
                if 'Primary Categories:' in line:
                    step1_data['primary_categories'] = line.split('Primary Categories:')[1].strip()
                elif 'Timeline:' in line:
                    step1_data['timeline'] = line.split('Timeline:')[1].strip()
                elif 'Depth:' in line:
                    step1_data['depth'] = line.split('Depth:')[1].strip()
                elif 'Recency Level:' in line:
                    step1_data['recency_level'] = line.split('Recency Level:')[1].strip()
                elif 'Data Sources:' in line:
                    step1_data['data_sources'] = line.split('Data Sources:')[1].strip()
                elif 'Search Strategy:' in line:
                    step1_data['search_strategy'] = line.split('Search Strategy:')[1].strip()
                elif 'Mood/Tone:' in line:
                    step1_data['mood_tone'] = line.split('Mood/Tone:')[1].strip()
                elif 'Notes:' in line:
                    step1_data['notes'] = line.split('Notes:')[1].strip()
        except:
            pass  # Use defaults if parsing fails
        
        return step1_data
        
    except Exception as e:
        print(f"Step 1 failed: {str(e)}")
        return {"error": f"Intent analysis failed: {str(e)}"}


def conduct_research(step1_data: dict) -> str:
    """Step 2: Conduct LLM-based research"""
    print("Step 2: Conducting research...")
    
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Format the research prompt with all Step 1 data
        research_prompt = RESEARCH_PROMPT.format(
            query=step1_data['query'],
            primary_categories=step1_data['primary_categories'],
            timeline=step1_data['timeline'],
            depth=step1_data['depth'],
            recency_level=step1_data['recency_level'],
            data_sources=step1_data['data_sources'],
            search_strategy=step1_data['search_strategy'],
            notes=step1_data['notes'],
            mood_tone=step1_data['mood_tone']
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": research_prompt}],
            max_completion_tokens=2000
        )
        
        research_result = response.choices[0].message.content.strip()
        print("Step 2 completed: Research conducted")
        
        return research_result
        
    except Exception as e:
        print(f"Step 2 failed: {str(e)}")
        return f"Research failed: {str(e)}"


def generate_podcast_script(step1_data: dict, research_result: str) -> str:
    """Step 3: Generate podcast script"""
    print("Step 3: Generating podcast script...")
    
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Format the script prompt with all context
        script_prompt = PODCAST_SCRIPT_PROMPT.format(
            query=step1_data['query'],
            primary_categories=step1_data['primary_categories'],
            timeline=step1_data['timeline'],
            mood_tone=step1_data['mood_tone'],
            research_content=research_result
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": script_prompt}],
            max_completion_tokens=15000,
            temperature=0.8
        )
        
        script = response.choices[0].message.content.strip()
        
        # Clean up script content
        script = clean_script_content(script)
        
        print(f"Step 3 completed: Script generated ({len(script)} characters)")
        
        return script
        
    except Exception as e:
        print(f"Step 3 failed: {str(e)}")
        return f"Script generation failed: {str(e)}"


def clean_script_content(script: str) -> str:
    """Clean up script content by replacing smart quotes and other Unicode characters"""
    script = script.replace('\u201c', '"')  # Left double quotation mark
    script = script.replace('\u201d', '"')  # Right double quotation mark
    script = script.replace('\u2018', "'")  # Left single quotation mark
    script = script.replace('\u2019', "'")  # Right single quotation mark
    script = script.replace('\u2013', '-')  # En dash
    script = script.replace('\u2014', '--')  # Em dash
    script = script.replace('\u2026', '...')  # Horizontal ellipsis
    return script


def generate_audio(script: str, query: str) -> str:
    """Step 4: Generate audio from script"""
    print("Step 4: Generating audio...")
    
    try:
        # Create safe filename
        safe_query = query.replace(' ', '_').replace('?', '').replace('!', '')[:30]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f"podcast_audio_{safe_query}_{timestamp}.wav"
        
        # Generate audio
        result = generate_audio_from_script(script, audio_filename)
        
        if result:
            print(f"Step 4 completed: Audio generated - {audio_filename}")
            return audio_filename
        else:
            print("Step 4 failed: Audio generation failed")
            return None
            
    except Exception as e:
        print(f"Step 4 failed: {str(e)}")
        return None


def run_complete_pipeline(query: str, user_profile: str = "", progress_callback=None) -> tuple:
    """Run the complete podcast generation pipeline with progress updates"""
    print(f"Starting Complete Podcast Pipeline")
    print(f"Query: {query}")
    print(f"User Profile: {user_profile}")
    print("=" * 80)
    
    status_updates = []
    current_status = "Starting pipeline..."
    
    def update_status(message):
        nonlocal current_status
        current_status = message
        status_updates.append(message)
        print(f"Status: {message}")
        if progress_callback:
            progress_callback(message)
    
    try:
        # Step 1: Intent Analysis
        update_status("Step 1/4: Analyzing user intent...")
        step1_data = analyze_intent(query, user_profile)
        if "error" in step1_data:
            return f"Pipeline failed at Step 1: {step1_data['error']}", current_status
        
        update_status("Step 1 completed: Intent analysis generated")
        
        # Step 2: Research
        update_status("Step 2/4: Conducting research...")
        research_result = conduct_research(step1_data)
        if research_result.startswith("Research failed"):
            return f"Pipeline failed at Step 2: {research_result}", current_status
        
        update_status("Step 2 completed: Research conducted")
        
        # Step 3: Script Generation
        update_status("Step 3/4: Generating podcast script...")
        script = generate_podcast_script(step1_data, research_result)
        if script.startswith("Script generation failed"):
            return f"Pipeline failed at Step 3: {script}", current_status
        
        update_status(f"Step 3 completed: Script generated ({len(script)} characters)")
        
        # Step 4: Audio Generation
        update_status("Step 4/4: Generating audio...")
        audio_filename = generate_audio(script, query)
        if not audio_filename:
            return f"Pipeline failed at Step 4: Audio generation failed", current_status
        
        update_status("Step 4 completed: Audio generated")
        
        # Success!
        update_status("Pipeline completed successfully!")
        print(f"Audio file: {audio_filename}")
        
        result = f"""## Podcast Generated Successfully!

**Query:** {query}
**Audio File:** `{audio_filename}`
**Script Length:** {len(script)} characters

### Generated Script:
{script}

---
*Audio file saved and ready to play!*
"""
        
        return result, "Pipeline completed successfully!"
        
    except Exception as e:
        error_msg = f"Pipeline failed: {str(e)}"
        print(error_msg)
        return error_msg, f"Pipeline failed: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="Podcast Pipeline") as demo:
    gr.Markdown("# Complete Podcast Pipeline")
    gr.Markdown("Generate podcast audio from your query through all steps automatically")
    
    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(
                label="What would you like to hear a podcast about?",
                placeholder="e.g., relatable girl talk, Manchester United gameweek review, AI in healthcare...",
                lines=2
            )
            
            user_profile_input = gr.Textbox(
                label="Your Profile (Optional)",
                placeholder="e.g., 23 year old software engineer interested in sports, movies, entertainment...",
                lines=2
            )
            
            generate_btn = gr.Button("Generate Podcast", variant="primary", size="lg")
        
        with gr.Column():
            status_display = gr.Markdown("### Pipeline Status\nReady to generate your podcast!")
            progress_bar = gr.Progress()
    
    with gr.Row():
        output_display = gr.Markdown()
    
    # Event handler with real-time updates
    def generate_podcast(query, user_profile, progress=gr.Progress()):
        if not query.strip():
            return "Please enter a query for your podcast.", "### Pipeline Status\nNo query provided"
        
        progress(0, desc="Starting pipeline...")
        
        # Run the complete pipeline with progress updates
        result, final_status = run_complete_pipeline(query, user_profile)
        
        return result, f"### Pipeline Status\n{final_status}"
    
    generate_btn.click(
        generate_podcast,
        inputs=[query_input, user_profile_input],
        outputs=[output_display, status_display]
    )


if __name__ == "__main__":
    print("Starting Complete Podcast Pipeline...")
    print("Make sure you have OPENAI_API_KEY and HUME_API_KEY in your .env file")
    demo.launch(server_name="0.0.0.0", server_port=7860)