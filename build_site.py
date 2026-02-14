import yaml
from jinja2 import Environment, FileSystemLoader
import os

def build_site():
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')

    # Render template with config data
    output = template.render(**config)

    # Write output to index.html in the root directory
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output)

    print("Site built successfully! Output saved to index.html")

if __name__ == "__main__":
    build_site()
