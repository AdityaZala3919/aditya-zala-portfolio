from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import threading

from app.schemas import (
    Project, ProjectCreate, ProjectUpdate, 
    Blog, BlogCreate, BlogUpdate
)
from app.auth import verify_master_token
from app.email_service import email_service
from app import db

app = FastAPI(
    title="Portfolio API",
    description="Protected API for managing portfolio projects and blogs",
    version="1.0.0",
)

# Define security scheme for Swagger UI
app.openapi_tags = [
    {
        "name": "projects",
        "description": "Project management endpoints",
    },
    {
        "name": "blogs",
        "description": "Blog management endpoints",
    },
    {
        "name": "contact",
        "description": "Contact form endpoint",
    },
]

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== PROJECTS ENDPOINTS ====================

@app.get("/api/projects", response_model=List[Project], tags=["projects"])
async def list_projects(token: str = Depends(verify_master_token)):
    """Get all projects (protected)."""
    return db.get_projects()


@app.get("/api/projects/{project_id}", response_model=Project, tags=["projects"])
async def read_project(project_id: int, token: str = Depends(verify_master_token)):
    """Get a specific project by ID (protected)."""
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@app.post("/api/projects", response_model=Project, status_code=status.HTTP_201_CREATED, tags=["projects"])
async def create_project(project: ProjectCreate, token: str = Depends(verify_master_token)):
    """Create a new project (protected)."""
    return db.create_project(project)


@app.put("/api/projects/{project_id}", response_model=Project, tags=["projects"])
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    token: str = Depends(verify_master_token),
):
    """Update an existing project (protected)."""
    updated = db.update_project(project_id, project)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return updated


@app.delete("/api/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
async def delete_project(project_id: int, token: str = Depends(verify_master_token)):
    """Delete a project (protected)."""
    if not db.delete_project(project_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


# ==================== BLOGS ENDPOINTS ====================

@app.get("/api/blogs", response_model=List[Blog], tags=["blogs"])
async def list_blogs(token: str = Depends(verify_master_token)):
    """Get all blogs (protected)."""
    return db.get_blogs()


@app.get("/api/blogs/{blog_id}", response_model=Blog, tags=["blogs"])
async def read_blog(blog_id: int, token: str = Depends(verify_master_token)):
    """Get a specific blog by ID (protected)."""
    blog = db.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@app.post("/api/blogs", response_model=Blog, status_code=status.HTTP_201_CREATED, tags=["blogs"])
async def create_blog(blog: BlogCreate, token: str = Depends(verify_master_token)):
    """Create a new blog (protected)."""
    return db.create_blog(blog)


@app.put("/api/blogs/{blog_id}", response_model=Blog, tags=["blogs"])
async def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    token: str = Depends(verify_master_token),
):
    """Update an existing blog (protected)."""
    updated = db.update_blog(blog_id, blog)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return updated


@app.delete("/api/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
async def delete_blog(blog_id: int, token: str = Depends(verify_master_token)):
    """Delete a blog (protected)."""
    if not db.delete_blog(blog_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")


# ==================== CONTACT FORM ENDPOINT ====================

@app.post("/api/contact", tags=["contact"], dependencies=[Depends(verify_master_token)])
async def send_contact_email(data: dict, token: str = Depends(verify_master_token)):
    """
    Send a contact form email (protected).
    Requires MASTER_TOKEN authentication.
    Email is sent in a background thread to prevent blocking.
    """
    try:
        name = data.get("name", "")
        email = data.get("email", "")
        subject = data.get("subject", "")
        message = data.get("message", "")
        
        # Send email in background thread to avoid blocking the response
        def send_email_bg():
            try:
                email_service.send_contact_email(
                    sender_name=name,
                    sender_email=email,
                    sender_subject=subject,
                    sender_message=message,
                )
            except Exception as e:
                print(f"Background email error: {str(e)}")
        
        thread = threading.Thread(target=send_email_bg, daemon=True)
        thread.start()
        
        # Return immediately while email sends in background
        return {
            "success": True,
            "message": "Email sent successfully"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required)."""
    return {"status": "ok"}

