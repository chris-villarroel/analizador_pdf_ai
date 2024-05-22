import re
import os

def clean_filename(filename):
    # Separate the base name and extension
    base_name, extension = os.path.splitext(filename)
    
    # Remove any non-word characters (anything other than letters, digits, and underscores)
    clean_name = re.sub(r'[^\w\s]', '', base_name)
    
    # Replace any whitespace with a single underscore
    clean_name = re.sub(r'\s+', '_', clean_name)
    
    # Concatenate the cleaned base name and the original extension
    return clean_name + extension

import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

import os

def ensure_directories_exist(directories):
    """
    Ensure that the specified directories exist, creating them if necessary.

    Parameters:
    - directories (list of str): A list of directory paths to check/create.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


 
def validate_and_shorten_name(name, max_length=14):
    """Validate and possibly shorten the name according to specified rules."""

    # Step 1: Truncate to max_length if necessary
    if len(name) > max_length:
        name = name[:max_length]

    # Step 2: Ensure the name ends and starts with an alphanumeric character
    name = re.sub(r'^[^a-zA-Z0-9]*|[^a-zA-Z0-9]*$', '', name)

    # Step 3: Replace invalid characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)

    # Step 4: Shorten again if previous steps made it too long
    if len(name) > max_length:
        name = name[:max_length]

    # Step 5: Ensure it does not start or end with a hyphen or underscore
    name = re.sub(r'^[_-]+|[_-]+$', '', name)

    # Step 6: Ensure length is at least 3 characters
    while len(name) < 3:
        name += '_'

    return name
       
def count_characters_in_list(text_objects):
    """
    Count all characters from a list of objects with a 'text' attribute.

    Parameters:
    text_objects (list): A list of objects, each having a 'text' attribute containing a string.

    Returns:
    int: Total count of characters in all text attributes of the list elements.
    """
    total_characters = 0
    for obj in text_objects:
        total_characters += len(obj.text)  # Sum up the length of the string in the 'text' attribute
    
    return total_characters
      