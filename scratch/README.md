# Qdrant Vector Database Example

This example demonstrates how to use Qdrant, a vector similarity search engine, to store and query vector embeddings.

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Setup

1. Install the required packages:
```bash
pip install qdrant-client python-dotenv
```

2. Create a `.env` file in the same directory with your Qdrant credentials:
```bash
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

You can get these credentials by:
- Using a local Qdrant instance (URL would be something like `http://localhost:6333`)
- Using Qdrant Cloud (URL would be something like `https://your-cluster.cloud.qdrant.io`)

## Running the Example

Simply run the script:
```bash
python ex_qdrant_flow.py
```

## What the Script Does ([from the Qdrant docs](https://qdrant.tech/documentation/quickstart/#create-a-collection))

1. Creates a new collection called "test_collection886" with 4-dimensional vectors
2. Inserts 6 sample points with city names as payload
3. Performs a similarity search using New York's vector as the query
4. Prints the search results and lists all collections

## Expected Output

The script will output:
- Search results showing the most similar vectors to the query vector
- A list of all collections in your Qdrant instance

## Notes

- The example uses 4-dimensional vectors for simplicity
- The distance metric used is DOT (dot product)
- The script includes error handling for collection creation
- Each point has a unique ID and a payload containing a city name
