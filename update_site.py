import os
import yaml
import requests
import argparse

# Configuration
API_KEY = os.getenv("LLM_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions" # Example using OpenRouter
MODEL = "google/gemini-2.0-flash-001" 

def update_config(user_prompt):
    if not API_KEY:
        print("Error: LLM_API_KEY environment variable not set.")
        return

    # Load current config
    try:
        with open('config.yaml', 'r') as f:
            current_config = f.read()
    except FileNotFoundError:
        print("Error: config.yaml not found.")
        return

    # Construct system prompt
    system_prompt = f"""
    You remain a helpful assistant that updates a YAML configuration file for a portfolio website based on user requests.
    
    Current YAML content:
    ```yaml
    {current_config}
    ```
    
    Instructions:
    1. Read the user's request.
    2. detailed Modify the YAML content to reflect the user's request.
    3. Return ONLY the valid YAML code. Do not include markdown code blocks (```yaml ... ```) or any other text.
    4. Ensure the structure (keys) remains consistent unless explicitly asked to change.
    """

    # Call LLM API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
         "HTTP-Referer": "http://localhost:3000", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Consultant Portfolio Updater", # Optional. Shows in rankings on openrouter.ai.
    }
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        new_yaml_content = result['choices'][0]['message']['content'].strip()
        
        # Simple cleanup if the LLM still wraps in code blocks despite instructions
        if new_yaml_content.startswith("```yaml"):
            new_yaml_content = new_yaml_content[7:]
        if new_yaml_content.startswith("```"):
             new_yaml_content = new_yaml_content[3:]
        if new_yaml_content.endswith("```"):
            new_yaml_content = new_yaml_content[:-3]
            
        new_yaml_content = new_yaml_content.strip()

        # Validate YAML
        yaml.safe_load(new_yaml_content)

        # Write updates
        with open('config.yaml', 'w') as f:
            f.write(new_yaml_content)
        
        print("Successfully updated config.yaml based on your request.")
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if response:
             print(f"Response text: {response.text}")
    except yaml.YAMLError as e:
        print(f"Error: Generated content was not valid YAML. {e}")
        print("Generated content was:")
        print(new_yaml_content)
    except Exception as e:
         print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update portfolio config via AI")
    parser.add_argument("prompt", help="Natural language instruction for the update")
    args = parser.parse_args()
    
    update_config(args.prompt)
