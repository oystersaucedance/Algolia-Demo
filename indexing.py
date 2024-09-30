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
    with open('data/products.json') as f:
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
    'ranking': [
        'typo',
        'geo',
        'words',
        'filters',
        'proximity',
        'attribute',
        'exact',
        'custom'
    ],
    'optionalWords': ['and', 'the'],
    'exactOnSingleWordQuery': 'word',
    'hitsPerPage': 20
}
# Define replica indices for sorting by price
replicas = [
    ('products_price_asc', {
        'ranking': [
            'asc(price)',  # Sort by price ascending
            'typo',
            'geo',
            'words',
            'filters',
            'proximity',
            'attribute',
            'exact',
            'custom'
        ]
    }),
    ('products_price_desc', {
        'ranking': [
            'desc(price)',  # Sort by price descending
            'typo',
            'geo',
            'words',
            'filters',
            'proximity',
            'attribute',
            'exact',
            'custom'
        ]
    }),
]

# Create replica indices
for replica_name, settings in replicas:
    try:
        replica = client.init_index(replica_name)
        replica.set_settings(settings)
        print(f"Replica index '{replica_name}' created with custom ranking.")
    except Exception as e:
        print(f"Error creating replica '{replica_name}': {e}")

print("Indexing script completed successfully.")