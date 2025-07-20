from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv


# Initialize the encoder and client
encoder = SentenceTransformer("all-MiniLM-L6-v2")
load_dotenv()
client = QdrantClient(url=os.environ['QDRANT_URL'], api_key=os.environ['QDRANT_API_KEY'])  # Adjust URL and API KEY as needed
collection_name = "cool_papers"

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

def add_paper_to_collection(thread_data):
    """
    Add a research paper to the Qdrant collection
    
    Args:
        thread_data: Dictionary containing paper information
            - thread_id: Discord thread ID
            - title: Paper title
            - content: Paper content/description
            - urls: List of URLs (paper links)
            - poster_id: Discord user ID who posted
            - messages: List of all messages in thread
            - summary: Summary if available (first message if tagged as summarized)
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
        text_for_embedding = thread_data.get('content', '')

    # Generate embedding
    embedding = encoder.encode(text_for_embedding)

    # Prepare payload
    payload = {
        "thread_id": thread_data['thread_id'],
        "title": thread_data.get('title', ''),
        "content": thread_data.get('content', ''),
        "urls": thread_data.get('urls', []),
        "poster_id": thread_data['poster_id'],
        "messages": thread_data.get('messages', []),
        "summary": thread_data.get('summary', ''),
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
        existing = client.retrieve_points(
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
    # New threads are already confirmed to have Summarized tag
    
    '''
    summary = first comment in the thread
    NOTE: The thread will ALWAYS contain at least a starting message - checks are redundant
    - The summary will need to be changed to properly log the summary since it isn't guaranteed to be the first message, 
      I will figure out how to scrape from discord and include it as an attribute in the pydantic model
    '''
    summary = thread.comments[0].comment

    # Prepare thread data
    # NOTE: removed embeds, redundant. Use Urls instead.
    thread_data = {
        'thread_id': thread.id,
        'title': thread.topic,
        'content': thread.comments[0], # removed checks: the thread cannot be posted without a message
        'urls': [comment.url for comment in thread.comments],
        'poster_id': thread.owner_id,
        'messages': [comment for comment in thread.comments if comment.url], # CommentSerialized objs
        'summary': summary,
        'tags': thread.tags,
        'timestamp': thread.created_at.isoformat(),
        'attachments': [comment.attachments for comment in thread.comments]
    }
    # Add to Qdrant
    add_paper_to_collection(thread_data)

    ''' 
    NOTE: removed add_log_tag in method:
    It is already being checked within the bot logic
    '''


async def process_thread_update(thread_id, message):
    """
    Process a thread update and update the paper in Qdrant
    This integrates with your existing updateThreadData logic
    """
    # Retrieve existing paper data
    try:
        existing = client.retrieve_points(
            collection_name=collection_name,
            ids=[thread_id]
        )
        if not existing:
            print(f"Paper {thread_id} not found for update")
            return
        
        existing_data = existing[0].payload
        
        # Update with new information
        # NOTE: removed embed parameter
        updated_data = existing_data.copy()
        updated_data['messages'].append(message.comment)
        updated_data['urls'].extend(message.url)
        updated_data['attachments'].extend(message.attachments)
        
        # Track all participants
        if 'participants' not in updated_data:
            updated_data['participants'] = []
        if message.author_id and message.author_id not in updated_data['participants']:
            updated_data['participants'].append(message.author_id)
        
        # Re-generate embedding if needed (e.g., if summary was updated)
        if updated_data.get('summary'):
            text_for_embedding = updated_data['summary']
        else:
            text_for_embedding = updated_data.get('title', '')
        
        embedding = encoder.encode(text_for_embedding)
        
        # Update in Qdrant
        client.upsert_points(
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
        print(f"Error updating paper {thread_id}: {e}")

async def upload_success(thread):
    point_id = thread.id
    points = client.retrieve(
        collection_name='cool_papers', 
        ids=[point_id]
        )

    return True if points else False
   
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