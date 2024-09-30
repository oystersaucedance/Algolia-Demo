import os
from algoliasearch.search_client import SearchClient  # Updated import statement
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
print("Loaded environment variables.")

ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = os.getenv('ALGOLIA_API_KEY')
INDEX_NAME = "products"

# Check if environment variables are loaded
if not ALGOLIA_APP_ID or not ALGOLIA_API_KEY:
    print("Error: Algolia credentials not found. Please check your .env file.")
    exit(1)

# Initialize the Algolia client
try:
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    print("Algolia client created successfully.")
except Exception as e:
    print(f"Error creating Algolia client: {e}")
    exit(1)

# Initialize the index
index = client.init_index(INDEX_NAME)
print(f"Initialized index: {INDEX_NAME}")

# Load data from products.json
try:
    with open('products.json') as f:
        products = json.load(f)
        print(f"Loaded {len(products)} products from JSON file.")
except Exception as e:
    print(f"Error loading products: {e}")
    exit(1)

# Index the data
try:
    response = index.save_objects(products, {'autoGenerateObjectIDIfNotExist': True})
    print(f"Successfully indexed {len(products)} products.")
except Exception as e:
    print(f"Error indexing products: {e}")

# Index settings configuration
index_settings = {
    'searchableAttributes': [
        'name',
        'description',
        'category',
        'brand'
    ],
    'attributesToRetrieve': [
        'name',
        'description',
        'price',
        'category',
        'brand',
        'thumbnail'
    ],
    'disableTypoToleranceOnAttributes': [
        'brand'
    ],
    'attributesForFaceting': [
        'filterOnly(price)',
        'category',
        'brand'
    ],
    'customRanking': [
        'desc(popularity)',
        'asc(price)'
    ],
    'optionalWords': ['and', 'the'],
    'exactOnSingleWordQuery': 'word',
    'hitsPerPage': 20
}

# Set the main index settings
try:
    index.set_settings(index_settings)
    print("Index settings applied successfully.")
except Exception as e:
    print(f"Error setting index settings: {e}")

# Define settings for replicas (excluding forbidden settings)
replica_settings = {
    'customRanking': index_settings['customRanking'],  # Keep only customRanking for sorting
}

# Create replica indices without ranking
replicas = ['products_price_asc', 'products_price_desc']

for replica_name in replicas:
    try:
        # Create the replica index and set its settings
        replica_index = client.init_index(replica_name)
        # Set only the allowed settings for replicas
        replica_index.set_settings(replica_settings)
        
        print(f"Replica index '{replica_name}' created successfully.")
    except Exception as e:
        print(f"Error creating replica '{replica_name}': {e}")

print("Indexing script completed successfully.")
