# Spencer and Williams - Algolia Search Demo

## Overview

This repository contains a demo showcasing an Algolia-powered search interface for Spencer and Williams products. The demo allows users to search, filter, and sort products using Algolia's InstantSearch.js library. It includes a price range slider, brand filter, and sorting functionality (by relevance and price).

You can view the live demo here: [Algolia Search Demo](https://oystersaucedance.github.io/Algolia-Demo/)

## Requirements

Before running the indexing script, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (version 12.x or later)
- [npm](https://www.npmjs.com/) (usually comes with Node.js)
- An Algolia account and an application ID/API keys. 

## Running the Indexing Script

To index products into Algolia, follow these steps:

### 1. Clone the Repository

Run this in your terminal on visual studio
git clone https://github.com/oystersaucedance/Algolia-Demo.git
cd Algolia-Demo


### 2. Install Dependencies

Run the following command to install all required Node.js packages:

npm install

Install dotenv module, which is used to load environment variables from a .env file. Run the following command in your terminal:

pip install python-dotenv

### 3. Setup Algolia Credentials

You need to provide your Algolia Application ID, Admin API Key, and the index name. Here's how:

1. Create a `.env` file in the root of the project.
2. Add the following lines to the `.env` file, replacing the placeholders with your Algolia credentials:

ALGOLIA_APP_ID=YourAlgoliaAppID
ALGOLIA_ADMIN_API_KEY=YourAdminAPIKey
ALGOLIA_INDEX_NAME=products

### 4. Add Data to Algolia

The demo includes a sample dataset in a `products.json` file. You can run the provided indexing script to push this data to your Algolia index:

node indexData.js


### 5. Verify Indexing

Once the script completes, log in to your Algolia dashboard to verify that the data has been successfully indexed.

---

## How It Works

### `indexData.js`

This script reads from the `products.json` file and pushes the product data to the specified Algolia index.

Key steps in the script:

- **Algolia Client Initialization**: It uses the `algoliasearch` package to interact with the Algolia API using the credentials provided in the `.env` file.
- **Batch Data Upload**: It reads the product data and sends it to the specified index in batches to avoid hitting any API limits.

### Example Code Snippet:

```javascript
require('dotenv').config();
const algoliasearch = require('algoliasearch');
const products = require('./products.json');

// Initialize Algolia Client
const client = algoliasearch(process.env.ALGOLIA_APP_ID, process.env.ALGOLIA_ADMIN_API_KEY);
const index = client.initIndex(process.env.ALGOLIA_INDEX_NAME);

// Push Data to Algolia
(async function () {
  try {
    const { objectIDs } = await index.saveObjects(products, {
      autoGenerateObjectIDIfNotExist: true,
    });
    console.log('Products indexed:', objectIDs);
  } catch (error) {
    console.error('Error indexing products:', error);
  }
})();
```

### JSON Data Format

The `products.json` file should be structured like this:

```json
[
  {
    "name": "Product 1",
    "price": 25.99,
    "brand": "Brand A",
    "image": "https://example.com/product1.jpg",
    "description": "A short product description."
  },
  {
    "name": "Product 2",
    "price": 45.50,
    "brand": "Brand B",
    "image": "https://example.com/product2.jpg",
    "description": "Another product description."
  }
]
```

---

## Frontend Search Demo

Once the data is indexed, you can view the search demo on [GitHub Pages](https://oystersaucedance.github.io/Algolia-Demo/). 
The frontend uses Algolia's InstantSearch.js library to display results with a responsive design.

### Key Features:

- **Search Box**: Type to search for products by name.
- **Filters**: Use brand and price filters to narrow down results.
- **Sorting**: Sort results by relevance, price (low to high), or price (high to low).
- **Price Range**: Move the slider to select a price range for the products in your search.

---

## Challenges and Reasoning

The main challenge was ensuring proper integration between Algolia's InstantSearch.js on the frontend and the data indexing on the backend. 
Managing the product filters dynamically, especially the price range, required some adjustments to ensure accuracy. 
Additionally, styling the interface to give it a professional look involved optimizing the CSS to be modern and responsive.

## Approximate Time Taken

The project took approximately **5-7 hours**, including:
- Answering the questions.
- Setting up Algolia search.
- Creating and styling the frontend demo.
- Writing the indexing script and testing data indexing.
- Debugging and fixing issues related to filters, sorting, and styling.

---

## Feedback on the Assignment

The assignment was challenging but enjoyable, providing an opportunity to learn and explore Algolia's powerful search features in-depth. 
One suggestion would be to provide a bit more guidance on expected frontend styling or specific requirements for filter behavior to better align expectations.

---

This README should help explain how to get the project running, and you can make any tweaks to match your exact setup. Let me know if you have further questions!
