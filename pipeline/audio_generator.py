"""
Audio Generator - Generates audio from podcast script using Hume AI TTS
Handles long scripts by splitting into chunks and stitching them together
"""

import asyncio
import base64
import os
import json
import time
from hume import HumeClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_env():
    """Load environment variables from .env file"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value


def split_text_into_chunks(text: str, max_length: int = 2000):
    """Split text into chunks at sentence boundaries"""
    chunks = []
    current_chunk = ""
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed the limit
        if len(current_chunk) + len(paragraph) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                # If single paragraph is too long, split by sentences
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 2 > max_length:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = sentence
                        else:
                            # If single sentence is too long, force split
                            chunks.append(sentence[:max_length])
                            current_chunk = sentence[max_length:]
                    else:
                        current_chunk += sentence + ". "
        else:
            current_chunk += paragraph + "\n\n"
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def generate_audio_from_script(script_text: str, output_filename: str = "podcast_audio.wav"):
    """Generate audio from script text using Hume AI TTS"""
    
    # Load API key
    load_env()
    api_key = os.getenv("HUME_API_KEY")
    if not api_key:
        print("Error: HUME_API_KEY not found in environment variables")
        return None
    
    if not script_text.strip():
        print("Error: No script text provided")
        return None
    
    print(f"Processing script: {len(script_text)} characters")
    
    # Create Hume client
    try:
        hume = HumeClient(api_key=api_key)
        print("Hume client initialized successfully")
    except Exception as e:
        print(f"Error initializing Hume client: {e}")
        return None
    
    # Test API connectivity with small text
    print("Testing Hume API connectivity...")
    test_text = "Hello, this is a test."
    
    try:
        test_response = hume.tts.synthesize_json(
            utterances=[
                {
                    "voice": {
                        "id": "YOUR_VOICE_ID_HERE",
                        "provider": "HUME_AI"
                    },
                    "text": test_text
                }
            ],
            num_generations=1
        )
        print("API connectivity test successful")
    except Exception as e:
        print(f"API connectivity test failed: {e}")
        print("Check your HUME_API_KEY and network connection")
        return None
    
    # Check if script needs chunking (Hume API limit: 5000 characters)
    MAX_CHARS = 2000  # Smaller chunks for faster processing
    
    if len(script_text) > MAX_CHARS:
        print(f"Script is too long ({len(script_text)} chars). Splitting into chunks...")
        chunks = split_text_into_chunks(script_text, MAX_CHARS)
        print(f"Split into {len(chunks)} chunks")
        
        # Generate audio for each chunk
        all_audio_data = []
        successful_chunks = 0
        
        for i, chunk in enumerate(chunks):
            try:
                print(f"Processing chunk {i + 1}/{len(chunks)} ({len(chunk)} characters)...")
                
                start_time = time.time()
                
                response = hume.tts.synthesize_json(
                    utterances=[
                        {
                            "voice": {
                                "id": "YOUR_VOICE_ID_HERE",
                                "provider": "HUME_AI"
                            },
                            "text": chunk
                        }
                    ],
                    num_generations=1
                )
                
                elapsed_time = time.time() - start_time
                print(f"Chunk {i + 1} processed in {elapsed_time:.2f} seconds")
                
                # Get the audio data
                audio = response.generations[0].audio
                audio_data = base64.b64decode(audio)
                all_audio_data.append(audio_data)
                successful_chunks += 1
                print(f"Chunk {i + 1} completed successfully")
                
                # Add delay between chunks to avoid rate limiting
                if i < len(chunks) - 1:
                    print("Waiting 3 seconds before next chunk...")
                    time.sleep(3)
                    
            except Exception as e:
                print(f"Failed to process chunk {i + 1}: {e}")
                print("Skipping this chunk and continuing...")
                continue
        
        if not all_audio_data:
            print("No audio chunks were successfully generated")
            return None
        
        # Combine all audio chunks
        print("Combining audio chunks...")
        combined_audio = b''.join(all_audio_data)
        
        # Save combined audio to WAV file
        with open(output_filename, "wb") as f:
            f.write(combined_audio)
        
        print(f"Audio saved as '{output_filename}'")
        print(f"Generated from {successful_chunks} successful chunks out of {len(chunks)} total")
        
        return output_filename
        
    else:
        # Script is short enough for single API call
        print(f"Script is short enough ({len(script_text)} chars). Generating audio in one call...")
        
        try:
            response = hume.tts.synthesize_json(
                utterances=[
                    {
                        "voice": {
                            "id": "YOUR_VOICE_ID_HERE",
                            "provider": "HUME_AI"
                        },
                        "text": script_text
                    }
                ],
                num_generations=1
            )
            
            # Get the audio data
            audio = response.generations[0].audio
            audio_data = base64.b64decode(audio)
            
            # Save audio to WAV file
            with open(output_filename, "wb") as f:
                f.write(audio_data)
            
            print(f"Audio saved as '{output_filename}'")
            
            return output_filename
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None