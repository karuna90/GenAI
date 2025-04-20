#!/usr/bin/env python3
import requests
import json
import sys

# Ollama API endpoint
ollama_url = "http://localhost:11434/api/generate"

# Check if Ollama server is running
try:
    # Simple connection check
    requests.get("http://localhost:11434/api/version")
except requests.exceptions.ConnectionError:
    print("Error: Cannot connect to Ollama server at http://localhost:11434")
    print("Please make sure Ollama is running. You can start it with 'ollama serve'")
    sys.exit(1)

# Get user preferences
print("\n===== BALI TWO-DAY ITINERARY GENERATOR =====")
print("Let's create your personalized Bali itinerary!")
print("\nPlease answer the following questions about your preferences:")

# Collect user preferences
travel_style = input("\nWhat's your travel style? (adventure, relaxation, cultural, mix): ")
interests = input("What are your main interests in Bali? (beaches, temples, food, shopping, nature, etc.): ")
accommodation = input("Where are you staying in Bali? (Ubud, Seminyak, Kuta, Canggu, etc.): ")
budget = input("What's your budget level? (budget, mid-range, luxury): ")
special_requests = input("Any special requests or dietary requirements?: ")

# Create the prompt for Ollama
prompt = f"""
Create a detailed two-day itinerary for Bali, Indonesia based on the following preferences:

- Travel Style: {travel_style}
- Main Interests: {interests}
- Accommodation Location: {accommodation}
- Budget Level: {budget}
- Special Requests: {special_requests}

Include specific recommendations for:
- Morning activities
- Lunch spots with cuisine style
- Afternoon activities
- Dinner restaurants
- Evening entertainment

For each recommendation, provide:
1. The name of the place/activity
2. A brief description
3. Approximate cost if relevant
4. Travel time from {accommodation} if applicable

Format the itinerary in a clear, organized way with DAY 1 and DAY 2 clearly labeled.
"""

# Prepare the request payload
model = input("\nWhich Ollama model would you like to use? (default: llama3.2:1b): ") or "llama3.2:1b"

payload = {
    "model": model,
    "prompt": prompt,
    "stream": False
}

print(f"\nGenerating your Bali itinerary using the {model} model...")
print("This may take a moment...\n")

# Make the API request to Ollama
try:
    response = requests.post(ollama_url, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    result = response.json()
    itinerary = result.get("response", "No response received")
    
    # Display the generated itinerary
    print("\n===== YOUR PERSONALIZED BALI ITINERARY =====\n")
    print(itinerary)
    
    # Offer to save the itinerary
    save_option = input("\nWould you like to save this itinerary to a file? (y/n): ")
    if save_option.lower() == 'y':
        filename = input("Enter filename (default: bali_itinerary.txt): ") or "bali_itinerary.txt"
        with open(filename, 'w') as file:
            file.write("===== YOUR PERSONALIZED BALI ITINERARY =====\n\n")
            file.write(f"Travel Style: {travel_style}\n")
            file.write(f"Main Interests: {interests}\n")
            file.write(f"Accommodation: {accommodation}\n")
            file.write(f"Budget Level: {budget}\n")
            file.write(f"Special Requests: {special_requests}\n\n")
            file.write(itinerary)
        print(f"Itinerary saved to {filename}")
        
except requests.exceptions.RequestException as e:
    print(f"Error communicating with Ollama: {e}")
    if hasattr(e, 'response') and e.response is not None:
        try:
            error_detail = e.response.json()
            print(f"Error details: {error_detail}")
        except:
            print(f"Status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")

print("\nThank you for using the Bali Itinerary Generator!")