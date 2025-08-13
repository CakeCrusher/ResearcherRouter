from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import traceback
import json

"""TODO: CREATE NEW COLLECTION 'IEEE SPS' """
# Initialize the encoder and client
encoder = SentenceTransformer("all-MiniLM-L6-v2")
load_dotenv()
client = QdrantClient(url=os.environ['QDRANT_URL'], api_key=os.environ['QDRANT_API_KEY'])  # Adjust URL and API KEY as needed
# testing: collection_name = "cool_papers"
collection_name = "IEEE SPS"

def create_collection():
    """Create the Qdrant collection for research papers"""
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=384,  # Size for all-MiniLM-L6-v2
                distance=models.Distance.COSINE
            )
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection {collection_name} already exists")

def delete_collection():
    collection_name = 'cool-papers'
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name="{collection_name}")

def add_paper_to_collection(thread_data):
    """
    Add a research paper to the Qdrant collection
    
    Args:
        thread_data: Dictionary containing paper information
            - thread_id: Discord thread ID
            - title: Paper title
            - starter_msg: The first message in the post
            - content: Paper content/description
            - urls: List of URLs (paper links)
            - poster_id: Discord user ID who posted
            - participants: List of users participating in discussion
            - messages: List of all messages in thread
            - summary: Summary if available
            - tags: List of tags
            - timestamp: When thread was created
    """
    # Prepare text for embedding
    text_for_embedding = ""
    if thread_data.get('summary'):
        text_for_embedding = thread_data['summary']
    elif thread_data.get('title'):
        text_for_embedding = thread_data['title']
    else:
        text_for_embedding = thread_data.get('starter_msg', '')

    # Generate embedding
    embedding = encoder.encode(text_for_embedding)

    # Prepare payload
    payload = {
        "thread_id": thread_data['thread_id'],
        "title": thread_data.get('title', ''),
        "starter_msg": thread_data.get('starter_msg', ''),
        "urls": thread_data.get('urls', []),
        "poster_id": thread_data['poster_id'],
        'participants': thread_data['participants'],
        "summary": thread_data.get('summary', ''),
        "messages": thread_data.get('messages', []),
        "tags": thread_data.get('tags', []),
        "timestamp": thread_data.get('timestamp', datetime.now().isoformat()),
        "embedding_text": text_for_embedding  # Store what was used for embedding
    }
    # Upload to Qdrant
    client.upload_points(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=thread_data['thread_id'],
                vector=embedding.tolist(),
                payload=payload
            )
        ]
    )
    print(f"Added paper {thread_data['thread_id']} to collection")

def search_papers(query, limit=5):
    """
    Search for papers using semantic similarity
    
    Args:
        query: Search query string
        limit: Number of results to return
    
    Returns:
        List of search results
    """
    # Generate embedding for the query
    query_embedding = encoder.encode(query)
    
    # Search in Qdrant
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding.tolist(),
        limit=limit
    )

    results = [item for item in results if item.score > 1/3]
    
    return results

def get_participants_from_results(results):
    """
    Extract all unique participants from search results
    
    Args:
        results: Search results from Qdrant
    
    Returns:
        Set of participant user IDs
    """
    participants = set()
    
    for result in results:
        payload = result.payload
        
        # Add original poster
        poster_id = payload.get('poster_id')
        if poster_id:
            participants.add(poster_id)
        
        # Add all participants from discussions
        thread_participants = payload.get('participants', [])
        participants.update(thread_participants)
    
    return participants

def update_paper_in_collection(thread_id, new_data):
    """
    Update an existing paper in the collection
    
    Args:
        thread_id: Discord thread ID
        new_data: Dictionary with updated information
    """
    # Check if paper exists
    try:
        existing = client.retrieve(
            collection_name=collection_name,
            ids=[thread_id]
        )
        if not existing:
            print(f"Paper {thread_id} not found in collection")
            return
    except:
        print(f"Paper {thread_id} not found in collection")
        return
    
    # Update the paper
    add_paper_to_collection(new_data)
    print(f"Updated paper {thread_id} in collection")

# Integration functions for your existing Discord parsing logic

async def process_new_thread(thread):
    """
    Process a new Discord thread and add it to Qdrant
    This integrates with existing add_thread logic
    """
    summary = thread.summary

    # Prepare thread data
    thread_data = {
        'thread_id': thread.id,
        'title': thread.topic,
        'starter_msg': thread.comments[0], # removed checks: the thread cannot be posted without a message
        'urls': thread.urls,
        'poster_id': thread.owner_id,
        'participants': thread.participants,
        'summary': summary,
        'messages': thread.comments, # CommentSerialized objs
        'tags': thread.tags,
        'timestamp': thread.created_at.isoformat(),
    }
    # Add to Qdrant
    add_paper_to_collection(thread_data)


async def process_thread_update(thread_id, message, summary=None):
    """
    Process a thread update and update the paper in Qdrant
    This integrates with your existing updateThreadData logic
    """
    # Retrieve existing paper data
    try:
        existing = client.retrieve(
            collection_name=collection_name,
            ids=[thread_id]
        )
        if not existing:
            print(f"Paper {thread_id} not found for update")
            return
        
        existing_data = existing[0].payload
        # Update with new information
        updated_data = existing_data.copy()
        updated_data['messages'].append(message)
        updated_data['urls'].extend(message.url)
        updated_data['summary'] = summary if summary else existing_data['summary']
        
        # Track all participants
        if 'participants' not in updated_data:
            updated_data['participants'] = []
        if message.author_id and message.author_id not in updated_data['participants']:
            updated_data['participants'].append(message.author_id)
        
        # Re-generate embedding if needed (e.g., if summary was updated)
        text_for_embedding = updated_data['summary'] if updated_data['summary'] else updated_data['title']
        embedding = encoder.encode(text_for_embedding)
        
        # Update in Qdrant
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=thread_id,
                    vector=embedding.tolist(),
                    payload=updated_data
                )
            ]
        )
        print(f"Updated paper {thread_id} in collection")

    except Exception as e:
        print(f"Error updating paper {thread_id}: {e.__class__.__name__}: {e}")
        traceback.print_exc()

async def thread_exists(thread):
    point_id = thread.id
    points = client.retrieve(
        collection_name=collection_name, 
        ids=[point_id]
        )
    return True if points else False

'''Removes irrelevant points from the database using thread identifiers'''
async def delete_thread(thread):
    response = client.delete(
        collection_name=collection_name,
        points_selector=models.PointIdsList(

        points=[thread.id],

        ),
    )
    return response

def delete_thread_id(id):
    response = client.delete(
        collection_name=collection_name,
        points_selector=models.PointIdsList(
            points = [id]
        )
    )
    return response
   
# Example usage functions

def example_search():
    """Example of how to search for papers"""
    results = search_papers("machine learning", limit=3)
    for result in results:
        print(f"Score: {result.score}")
        print(f"Title: {result.payload.get('title', 'No title')}")
        print(f"Summary: {result.payload.get('summary', 'No summary')[:100]}...")
        print(f"URLs: {result.payload.get('urls', [])}")
        print("---")

if __name__ == "__main__":
    # Create the collection
    create_collection()
    
    # Example search
    print("Example search results:")
    example_search()