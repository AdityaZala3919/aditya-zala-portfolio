import json
import os
from typing import List, Optional
from app.schemas import Project, ProjectCreate, ProjectUpdate, Blog, BlogCreate, BlogUpdate

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
BLOGS_FILE = os.path.join(DATA_DIR, "blogs.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> List[dict]:
    """Load data from JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_json(filepath: str, data: List[dict]) -> None:
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==================== PROJECTS ====================

def get_projects() -> List[Project]:
    """Get all projects."""
    data = _load_json(PROJECTS_FILE)
    return [Project(**item) for item in data]


def get_project(project_id: int) -> Optional[Project]:
    """Get a specific project by ID."""
    projects = _load_json(PROJECTS_FILE)
    for p in projects:
        if p["id"] == project_id:
            return Project(**p)
    return None


def create_project(project: ProjectCreate) -> Project:
    """Create a new project."""
    projects = _load_json(PROJECTS_FILE)
    new_id = max([p["id"] for p in projects], default=0) + 1
    project_dict = project.model_dump()
    project_dict["id"] = new_id
    projects.append(project_dict)
    _save_json(PROJECTS_FILE, projects)
    return Project(**project_dict)


def update_project(project_id: int, project: ProjectUpdate) -> Optional[Project]:
    """Update an existing project."""
    projects = _load_json(PROJECTS_FILE)
    for i, p in enumerate(projects):
        if p["id"] == project_id:
            update_data = project.model_dump(exclude_unset=True)
            projects[i].update(update_data)
            _save_json(PROJECTS_FILE, projects)
            return Project(**projects[i])
    return None


def delete_project(project_id: int) -> bool:
    """Delete a project."""
    projects = _load_json(PROJECTS_FILE)
    for i, p in enumerate(projects):
        if p["id"] == project_id:
            projects.pop(i)
            _save_json(PROJECTS_FILE, projects)
            return True
    return False


# ==================== BLOGS ====================

def get_blogs() -> List[Blog]:
    """Get all blogs."""
    data = _load_json(BLOGS_FILE)
    return [Blog(**item) for item in data]


def get_blog(blog_id: int) -> Optional[Blog]:
    """Get a specific blog by ID."""
    blogs = _load_json(BLOGS_FILE)
    for b in blogs:
        if b["id"] == blog_id:
            return Blog(**b)
    return None


def create_blog(blog: BlogCreate) -> Blog:
    """Create a new blog."""
    blogs = _load_json(BLOGS_FILE)
    new_id = max([b["id"] for b in blogs], default=0) + 1
    blog_dict = blog.model_dump()
    blog_dict["id"] = new_id
    blogs.append(blog_dict)
    _save_json(BLOGS_FILE, blogs)
    return Blog(**blog_dict)


def update_blog(blog_id: int, blog: BlogUpdate) -> Optional[Blog]:
    """Update an existing blog."""
    blogs = _load_json(BLOGS_FILE)
    for i, b in enumerate(blogs):
        if b["id"] == blog_id:
            update_data = blog.model_dump(exclude_unset=True)
            blogs[i].update(update_data)
            _save_json(BLOGS_FILE, blogs)
            return Blog(**blogs[i])
    return None


def delete_blog(blog_id: int) -> bool:
    """Delete a blog."""
    blogs = _load_json(BLOGS_FILE)
    for i, b in enumerate(blogs):
        if b["id"] == blog_id:
            blogs.pop(i)
            _save_json(BLOGS_FILE, blogs)
            return True
    return False
