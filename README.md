# AI Consultant Portfolio

A professional, data-driven portfolio template designed for AI Consultants. Built with Python, Jinja2, and Tailwind CSS.

## Features

-   **Single Source of Truth**: All content is managed via a single `config.yaml` file.
-   **Automated Deployment**: GitHub Actions automatically rebuilds and deploys the site when you update the config.
-   **AI-Powered Updates**: Includes a Python script to update your portfolio using natural language prompts (e.g., "Add a new service for Generative AI Workshop").
-   **Professional Design**: Dark-themed, responsive, and high-tech aesthetic using Tailwind CSS.

## Setup Instructions

### 1. Fork this Repository
Click the "Fork" button at the top right of this page to create your own copy.

### 2. Enable GitHub Pages
1.  Go to **Settings** > **Pages**.
2.  Under **Build and deployment** > **Source**, select **Deploy from a branch**.
3.  Under **Branch**, select `gh-pages` / `/root` (Note: The `gh-pages` branch will be created automatically after the first successful action run).

### 3. Customize Content
Edit `config.yaml` directly in GitHub or locally. The site will automatically rebuild and deploy.

### 4. Local Development (Optional)
Prerequisites: Python 3.x installed.

1.  **Install Dependencies:**
    ```bash
    pip install pyyaml jinja2 requests
    ```

2.  **Build Site:**
    ```bash
    python build_site.py
    ```
    Open `index.html` in your browser to view the site.

## Using the AI Updater (`update_site.py`)

You can update your `config.yaml` using natural language commands.

1.  **Get an API Key:**
    Obtain an API key from OpenRouter (or modify the script for OpenAI/Gemini directly).

2.  **Set Environment Variable:**
    ```bash
    # Windows (PowerShell)
    $env:LLM_API_KEY = "your_api_key_here"
    
    # Mac/Linux
    export LLM_API_KEY="your_api_key_here"
    ```

3.  **Run the Updater:**
    ```bash
    python update_site.py "Change my bio to focus more on Agentic AI and increase my rate to $200/hr"
    ```
    The script will rewrite `config.yaml` intelligently while preserving the structure.

## Project Structure

-   `config.yaml`: The database for your site.
-   `templates/index.html`: The HTML template.
-   `build_site.py`: Generates the static HTML.
-   `update_site.py`: AI script for config updates.
-   `.github/workflows/deploy.yml`: CI/CD configuration.
