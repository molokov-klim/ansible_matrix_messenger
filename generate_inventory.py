#!/usr/bin/env python3
"""
Script to generate inventory.ini from template and environment variables
"""

import os
from jinja2 import Template

def load_env_vars():
    """Load variables from environment variables"""
    return {
        'server_ip': os.environ.get('SERVER_IP'),
        'ansible_user': os.environ.get('ANSIBLE_USER')
    }

def generate_inventory():
    """Generate inventory.ini from template"""
    # Load environment variables
    env_vars = load_env_vars()
    
    # Check if required variables are set and not empty
    missing_vars = []
    for var_name, var_value in env_vars.items():
        if var_value is None or var_value.strip() == "":
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(f"The following environment variables are not set or are empty: {', '.join(missing_vars)}")
    
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