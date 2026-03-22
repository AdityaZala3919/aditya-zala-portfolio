import json
import os
from http import HTTPStatus
from typing import Any, Callable, Dict, Optional
from urllib.parse import parse_qs


# Lazy import of backend modules - import only when needed
def _get_db():
    from backend.app import db
    return db

def _get_schemas():
    from backend.app.schemas import (
        Blog,
        BlogCreate,
        BlogUpdate,
        ContactFormRequest,
        ContactFormResponse,
        Project,
        ProjectCreate,
        ProjectUpdate,
    )
    return {
        'Blog': Blog,
        'BlogCreate': BlogCreate,
        'BlogUpdate': BlogUpdate,
        'ContactFormRequest': ContactFormRequest,
        'ContactFormResponse': ContactFormResponse,
        'Project': Project,
        'ProjectCreate': ProjectCreate,
        'ProjectUpdate': ProjectUpdate,
    }


def _json_response(status: int, body: Any) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        },
        "body": json.dumps(body, default=lambda o: o.model_dump() if hasattr(o, "model_dump") else o),
    }


def _html_response(status: int, html: str) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "no-store",
        },
        "body": html,
    }


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def _get_master_token() -> str:
    return _get_env("MASTER_TOKEN", "your-secret-master-token")


def _require_auth(headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    auth = headers.get("authorization") or headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        return _json_response(HTTPStatus.UNAUTHORIZED, {"detail": "Invalid or missing master token"})
    token = auth.removeprefix("Bearer ").strip()
    if token != _get_master_token():
        return _json_response(HTTPStatus.UNAUTHORIZED, {"detail": "Invalid or missing master token"})
    return None


def _get_json_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raise ValueError("Base64-encoded bodies are not supported")
    return json.loads(body)


def _projects_response() -> Dict[str, Any]:
    db = _get_db()
    return _json_response(HTTPStatus.OK, [p.model_dump() for p in db.get_projects()])


def _blogs_response() -> Dict[str, Any]:
    db = _get_db()
    return _json_response(HTTPStatus.OK, [b.model_dump() for b in db.get_blogs()])


def _not_found() -> Dict[str, Any]:
    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Not found"})


def _docs_html() -> str:
    return """<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8' />
    <title>Portfolio API Docs</title>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css' />
  </head>
  <body>
    <div id='swagger-ui'></div>
    <script src='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js'></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: '/api/openapi.json',
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis],
        layout: 'BaseLayout'
      });
    </script>
  </body>
</html>"""


def _openapi_json() -> Dict[str, Any]:
    # Minimal OpenAPI so Swagger UI can render lock icons and try-it-out.
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Portfolio API",
            "version": "1.0.0",
            "description": "Protected API for managing portfolio projects and blogs",
        },
        "paths": {
            "/api/projects": {
                "get": {
                    "summary": "List projects",
                    "security": [{"bearerAuth": []}],
                    "responses": {"200": {"description": "OK"}},
                },
                "post": {
                    "summary": "Create project",
                    "security": [{"bearerAuth": []}],
                    "responses": {"201": {"description": "Created"}},
                },
            },
            "/api/blogs": {
                "get": {
                    "summary": "List blogs",
                    "security": [{"bearerAuth": []}],
                    "responses": {"200": {"description": "OK"}},
                },
                "post": {
                    "summary": "Create blog",
                    "security": [{"bearerAuth": []}],
                    "responses": {"201": {"description": "Created"}},
                },
            },
            "/api/contact": {
                "post": {
                    "summary": "Send contact email",
                    "security": [{"bearerAuth": []}],
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/docs": {
                "get": {
                    "summary": "Swagger UI",
                    "responses": {"200": {"description": "OK"}},
                }
            }
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    }


def _handle_contact(payload: Dict[str, Any]) -> Dict[str, Any]:
    schemas = _get_schemas()
    ContactFormRequest = schemas['ContactFormRequest']
    ContactFormResponse = schemas['ContactFormResponse']
    
    data = ContactFormRequest(**payload)
    # Maintain current behavior: store/send in backend service and return fast.
    try:
        success, message = True, "Email sent successfully"
        try:
            from backend.app.email_service import email_service
            email_service.send_contact_email(
                sender_name=data.name,
                sender_email=data.email,
                sender_subject=data.subject,
                sender_message=data.message,
            )
        except Exception as exc:
            success = False
            message = f"Error sending email: {exc}"
        return _json_response(HTTPStatus.OK, ContactFormResponse(success=success, message=message).model_dump())
    except Exception as exc:
        return _json_response(HTTPStatus.BAD_REQUEST, {"success": False, "message": str(exc)})


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    method = (event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method") or "GET").upper()
    path = event.get("path") or event.get("rawPath") or "/"
    headers = {str(k): str(v) for k, v in (event.get("headers") or {}).items()}

    if method == "OPTIONS":
        return _json_response(HTTPStatus.NO_CONTENT, {})

    if path in {"/docs", "/api/docs"} and method == "GET":
        return _html_response(HTTPStatus.OK, _docs_html())

    if path in {"/openapi.json", "/api/openapi.json"} and method == "GET":
        return _json_response(HTTPStatus.OK, _openapi_json())

    if path == "/health" and method == "GET":
        return _json_response(HTTPStatus.OK, {"status": "ok"})

    if path == "/" and method == "GET":
        return _html_response(HTTPStatus.OK, "<html><body><a href='/docs'>Docs</a></body></html>")

    # Protected routes
    if path.startswith("/api/"):
        auth_error = _require_auth(headers)
        if auth_error:
            return auth_error

        try:
            db = _get_db()
            schemas = _get_schemas()
            ProjectCreate = schemas['ProjectCreate']
            ProjectUpdate = schemas['ProjectUpdate']
            BlogCreate = schemas['BlogCreate']
            BlogUpdate = schemas['BlogUpdate']
            
            if path == "/api/projects" and method == "GET":
                return _projects_response()
            if path.startswith("/api/projects/") and method == "GET":
                project_id = int(path.rsplit("/", 1)[-1])
                item = db.get_project(project_id)
                if not item:
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Project not found"})
                return _json_response(HTTPStatus.OK, item.model_dump())
            if path == "/api/projects" and method == "POST":
                return _json_response(HTTPStatus.CREATED, db.create_project(ProjectCreate(**_get_json_body(event))).model_dump())
            if path.startswith("/api/projects/") and method == "PUT":
                project_id = int(path.rsplit("/", 1)[-1])
                updated = db.update_project(project_id, ProjectUpdate(**_get_json_body(event)))
                if not updated:
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Project not found"})
                return _json_response(HTTPStatus.OK, updated.model_dump())
            if path.startswith("/api/projects/") and method == "DELETE":
                project_id = int(path.rsplit("/", 1)[-1])
                if not db.delete_project(project_id):
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Project not found"})
                return _json_response(HTTPStatus.NO_CONTENT, {})

            if path == "/api/blogs" and method == "GET":
                return _blogs_response()
            if path.startswith("/api/blogs/") and method == "GET":
                blog_id = int(path.rsplit("/", 1)[-1])
                item = db.get_blog(blog_id)
                if not item:
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Blog not found"})
                return _json_response(HTTPStatus.OK, item.model_dump())
            if path == "/api/blogs" and method == "POST":
                return _json_response(HTTPStatus.CREATED, db.create_blog(BlogCreate(**_get_json_body(event))).model_dump())
            if path.startswith("/api/blogs/") and method == "PUT":
                blog_id = int(path.rsplit("/", 1)[-1])
                updated = db.update_blog(blog_id, BlogUpdate(**_get_json_body(event)))
                if not updated:
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Blog not found"})
                return _json_response(HTTPStatus.OK, updated.model_dump())
            if path.startswith("/api/blogs/") and method == "DELETE":
                blog_id = int(path.rsplit("/", 1)[-1])
                if not db.delete_blog(blog_id):
                    return _json_response(HTTPStatus.NOT_FOUND, {"detail": "Blog not found"})
                return _json_response(HTTPStatus.NO_CONTENT, {})

            if path == "/api/contact" and method == "POST":
                return _handle_contact(_get_json_body(event))
        except ValueError:
            return _json_response(HTTPStatus.BAD_REQUEST, {"detail": "Invalid request path or body"})
        except Exception as exc:
            return _json_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"detail": str(exc)})

    return _not_found()


app = handler
