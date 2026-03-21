from pydantic import BaseModel
from typing import Optional, List


class ProjectBase(BaseModel):
    title: str
    description: str
    image: str
    technologies: List[str]
    githubUrl: Optional[str] = None
    liveUrl: Optional[str] = None
    isPinned: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    technologies: Optional[List[str]] = None
    githubUrl: Optional[str] = None
    liveUrl: Optional[str] = None
    isPinned: Optional[bool] = None


class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class BlogBase(BaseModel):
    title: str
    excerpt: str
    date: str
    readTime: str
    tags: List[str]
    isPinned: bool = False


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    date: Optional[str] = None
    readTime: Optional[str] = None
    tags: Optional[List[str]] = None
    isPinned: Optional[bool] = None


class Blog(BlogBase):
    id: int

    class Config:
        from_attributes = True


# ==================== CONTACT FORM SCHEMAS ====================

class ContactFormRequest(BaseModel):
    """Schema for contact form submissions."""
    name: str
    email: str
    subject: str
    message: str


class ContactFormResponse(BaseModel):
    """Response schema for contact form submission."""
    success: bool
    message: str
