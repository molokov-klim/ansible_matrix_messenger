#!/usr/bin/env python3
"""
Script to generate inventory.ini from template and .env.yml variables
"""

import yaml
import os
from jinja2 import Template

def load_env_vars():
    """Load variables from .env.yml file"""
    with open('.env.yml', 'r') as f:
        return yaml.safe_load(f)

def generate_inventory():
    """Generate inventory.ini from template"""
    # Load environment variables
    env_vars = load_env_vars()
    
    # Read the template
    with open('inventory.ini.j2', 'r') as f:
        template_str = f.read()
    
    # Render the template with environment variables
    template = Template(template_str)
    rendered_inventory = template.render(**env_vars)
    
    # Write the rendered inventory to file
    with open('inventory.ini', 'w') as f:
        f.write(rendered_inventory)
    
    print("Inventory file generated successfully!")

if __name__ == "__main__":
    generate_inventory()