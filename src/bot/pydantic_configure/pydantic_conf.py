from pydantic import BaseModel, HttpUrl
from typing import List, Optional

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
    url: List[HttpUrl]  # Comment can include multiple urls
    attachments: List[AttachmentSerialized]

class ThreadSerialized(BaseModel):
    thread_id: int
    owner_id: int       # tracks the author of the thread
    topic: str
    comments: List[CommentSerialized]



    