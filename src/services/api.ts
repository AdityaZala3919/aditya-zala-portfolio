/**
 * API Service Layer
 * Fetches projects and blogs from backend with fallback URLs.
 * Falls back to mock data if backend is unavailable.
 */

import { Project } from "@/components/ProjectCard";
import { Blog } from "@/components/BlogCard";
import { mockProjects, mockBlogs } from "@/data/mockData";
import { API_BASE_URL, fetchWithFallback } from "@/config/api";

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  isFromMock: boolean;
}

/**
 * Generic API call with fallback support
 */
async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetchWithFallback(endpoint, options);

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data = await response.json();
    return { data, error: null, isFromMock: false };
  } catch (error) {
    console.warn(`API call failed (${endpoint}), using mock data:`, error);
    return { data: null, error: String(error), isFromMock: true };
  }
}

/**
 * Fetch all projects
 */
export async function fetchProjects(): Promise<Project[]> {
  const result = await apiCall<Project[]>("/api/projects");
  if (result.isFromMock || !result.data) {
    return mockProjects;
  }
  return result.data;
}

/**
 * Fetch a single project
 */
export async function fetchProject(id: number): Promise<Project | null> {
  const result = await apiCall<Project>(`/api/projects/${id}`);
  if (result.isFromMock || !result.data) {
    return null;
  }
  return result.data;
}

/**
 * Create a new project
 */
export async function createProject(project: Omit<Project, "id">): Promise<Project | null> {
  const result = await apiCall<Project>("/api/projects", {
    method: "POST",
    body: JSON.stringify(project),
  });
  return result.data || null;
}

/**
 * Update a project
 */
export async function updateProject(
  id: number,
  updates: Partial<Omit<Project, "id">>
): Promise<Project | null> {
  const result = await apiCall<Project>(`/api/projects/${id}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  });
  return result.data || null;
}

/**
 * Delete a project
 */
export async function deleteProject(id: number): Promise<boolean> {
  const result = await apiCall<void>(`/api/projects/${id}`, {
    method: "DELETE",
  });
  return !result.error;
}

/**
 * Fetch all blogs
 */
export async function fetchBlogs(): Promise<Blog[]> {
  const result = await apiCall<Blog[]>("/api/blogs");
  if (result.isFromMock || !result.data) {
    return mockBlogs;
  }
  return result.data;
}

/**
 * Fetch a single blog
 */
export async function fetchBlog(id: number): Promise<Blog | null> {
  const result = await apiCall<Blog>(`/api/blogs/${id}`);
  if (result.isFromMock || !result.data) {
    return null;
  }
  return result.data;
}

/**
 * Create a new blog
 */
export async function createBlog(blog: Omit<Blog, "id">): Promise<Blog | null> {
  const result = await apiCall<Blog>("/api/blogs", {
    method: "POST",
    body: JSON.stringify(blog),
  });
  return result.data || null;
}

/**
 * Update a blog
 */
export async function updateBlog(
  id: number,
  updates: Partial<Omit<Blog, "id">>
): Promise<Blog | null> {
  const result = await apiCall<Blog>(`/api/blogs/${id}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  });
  return result.data || null;
}

/**
 * Delete a blog
 */
export async function deleteBlog(id: number): Promise<boolean> {
  const result = await apiCall<void>(`/api/blogs/${id}`, {
    method: "DELETE",
  });
  return !result.error;
}

interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

interface ContactFormResponse {
  success: boolean;
  message: string;
}

/**
 * Send contact form email
 * Simple API call - no validation
 */
export async function sendContactEmail(
  data: ContactFormData
): Promise<ContactFormResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/contact`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      return {
        success: false,
        message: `Error: ${response.statusText}`,
      };
    }

    const result = await response.json();
    return result;
  } catch (error) {
    return {
      success: false,
      message: `Failed to send email: ${String(error)}`,
    };
  }
}
