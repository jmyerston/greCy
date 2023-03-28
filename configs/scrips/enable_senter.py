import spacy
from spacy import util

# Load the configuration file
config_path = "/path/to/config.cfg"
config = spacy.util.load_config(config_path)

# Remove 'senter' from the disabled components
config['training']['disabled'] = [comp for comp in config['training']['disabled'] if comp != 'senter']

# Save the modified configuration to file
spacy.util.to_disk(config_path, config)
