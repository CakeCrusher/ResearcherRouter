from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class AttachmentSerialized(BaseModel):
    filename: str
    attachment_id: int
    url: HttpUrl # url to download attachment file
    byte_size: int
    media_type: Optional[str] = None # may be None
  
class CommentSerialized(BaseModel):
    author_id: int      # tracks the author of the comment/message
    comment: str
    url: List[HttpUrl]  # Comment can include multiple urls
    attachments: List[AttachmentSerialized]

class ThreadSerialized(BaseModel):
    thread_id: int
    owner_id: int       # tracks the author of the thread
    topic: str
    comments: List[CommentSerialized]



    