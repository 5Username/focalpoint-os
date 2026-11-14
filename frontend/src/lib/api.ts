/**
 * Central API base URL.
 * In development it falls back to localhost.
 * In production set VITE_API_URL on Vercel.
 */
export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function apiUrl(path: string): string {
  return `${API_BASE}${path.startsWith('/') ? path : '/' + path}`;
}
