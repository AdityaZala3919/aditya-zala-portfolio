/**
 * API Configuration
 * Supports multiple backend URLs with fallback mechanism
 */

const API_URLS = [
  import.meta.env.VITE_API_URL,
  "https://aditya-zala-portfolio.onrender.com",
].filter(Boolean);

export const API_BASE_URL = API_URLS[0] || "http://localhost:8000";

// Fallback URLs in case primary fails
export const API_FALLBACK_URLS = API_URLS.slice(1);

// Helper function to try multiple URLs
export async function fetchWithFallback(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const urls = [API_BASE_URL, ...API_FALLBACK_URLS];

  let lastError: Error | null = null;

  for (const url of urls) {
    try {
      const response = await fetch(`${url}${endpoint}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      if (response.ok) {
        return response;
      }

      lastError = new Error(`HTTP ${response.status}: ${response.statusText}`);
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      continue; // Try next URL
    }
  }

  throw lastError || new Error("All API endpoints failed");
}
