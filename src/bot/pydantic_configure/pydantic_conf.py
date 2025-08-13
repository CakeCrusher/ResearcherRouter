from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

'''
Serialize Attachments, Messages, and Thread discord objects
Removed Embedded objects and replaced with CommentSerialized.url
The url can be extracted and used to gather needed information on the papers for comparison
'''
class AttachmentSerialized(BaseModel):
    filename: str
    attachment_id: int
    url: HttpUrl # url to download attachment file
    byte_size: int
    media_type: Optional[str] = None # may be None
  
class CommentSerialized(BaseModel):
    author_id: int      # tracks the author of the comment/message
    comment: str
    url: List[HttpUrl] = [] # Comment can include multiple urls
    attachments: List[AttachmentSerialized] = []
    reactions: List[str] = []
    created_at: datetime

class ThreadSerialized(BaseModel):
    id: int
    owner_id: int       # tracks the author of the thread
    participants: List[int]
    topic: str
    tags: List[int]
    urls: List[HttpUrl] = []
    summary: Optional[str] = None
    comments: List[CommentSerialized]
    created_at: datetime



    