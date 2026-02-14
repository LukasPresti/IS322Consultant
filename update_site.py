import os
import yaml
import requests
import argparse
import json

# Configuration
API_KEY = os.getenv("LLM_API_KEY")

def update_config(user_prompt):
    if not API_KEY:
        print("Error: LLM_API_KEY environment variable not set.")
        return

    # Determine provider based on key format
    is_gemini = False
    if API_KEY.startswith("AIza"):
        is_gemini = True
        print("Detected Google Gemini API Key.")
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    else:
        print("Using OpenRouter/OpenAI API.")
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        model = "google/gemini-2.0-flash-001"

    # Load current config
    try:
        with open('config.yaml', 'r') as f:
            current_config = f.read()
    except FileNotFoundError:
        print("Error: config.yaml not found.")
        return

    # Construct prompts
    system_instruction = f"""
    You remain a helpful assistant that updates a YAML configuration file for a portfolio website based on user requests.
    
    Current YAML content:
    ```yaml
    {current_config}
    ```
    
    Instructions:
    1. Read the user's request.
    2. Modify the YAML content to reflect the user's request.
    3. Return ONLY the valid YAML code. Do not include markdown code blocks (```yaml ... ```) or any other text.
    4. Ensure the structure (keys) remains consistent unless explicitly asked to change.
    5. IMPORTANT: When updating theme colors, ALWAYS use valid CSS hex codes (e.g., '#00ff00' instead of 'neon green') or standard CSS color names.
    6. DESIGN CONTROL: You can now control the design via these keys in 'theme':
       - `primary_color`: Hex code.
       - `background`: Hex code.
       - `font`: 'sans' (default), 'serif', or 'mono'.
       - `alignment`: 'center' (default), 'left', or 'right'.
    """

    # Prepare Request
    headers = {
        "Content-Type": "application/json"
    }

    if is_gemini:
        # Google Gemini API Payload
        data = {
            "contents": [{
                "parts": [{"text": system_instruction + "\n\nUser Request: " + user_prompt}]
            }]
        }
    else:
        # OpenRouter/OpenAI API Payload
        headers["Authorization"] = f"Bearer {API_KEY}"
        headers["HTTP-Referer"] = "http://localhost:3000"
        headers["X-Title"] = "Consultant Portfolio Updater"
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Parse Response
        if is_gemini:
            new_yaml_content = result['candidates'][0]['content']['parts'][0]['text']
        else:
            new_yaml_content = result['choices'][0]['message']['content']
            
        # Clean up Markdown
        new_yaml_content = new_yaml_content.strip()
        if new_yaml_content.startswith("```yaml"):
            new_yaml_content = new_yaml_content[7:]
        elif new_yaml_content.startswith("```"):
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
        if 'response' in locals() and response:
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
