const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>
}

export class ApiError extends Error {
  status: number
  data?: unknown

  constructor(message: string, status: number, data?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

export async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers: customHeaders, ...restOptions } = options

  let url = `${BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`

  if (params) {
    const searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value))
      }
    })
    const queryString = searchParams.toString()
    if (queryString) {
      url += (url.includes('?') ? '&' : '?') + queryString
    }
  }

  const token = localStorage.getItem('dramaapp_token')

  const headers: Record<string, string> = {
    'Accept': 'application/json',
    ...(options.body && typeof options.body === 'string' ? { 'Content-Type': 'application/json' } : {}),
    ...(customHeaders as Record<string, string>),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  try {
    const response = await fetch(url, {
      ...restOptions,
      headers,
    })

    if (response.status === 401) {
      // Do not silently purge tokens during routine requests,
      // only warn so background fetches don't boot admin out of the session
      console.warn(`[API 401] Unauthorized response for: ${url}`)
    }

    if (!response.ok) {
      let errorMsg = `Error en la solicitud: ${response.status} ${response.statusText}`
      let errorData: unknown
      try {
        errorData = await response.json()
        if (errorData && typeof errorData === 'object' && 'message' in errorData) {
          errorMsg = String((errorData as { message: unknown }).message)
        }
      } catch {
        // Response was not JSON
      }
      throw new ApiError(errorMsg, response.status, errorData)
    }

    // If 204 No Content
    if (response.status === 204) {
      return {} as T
    }

    return (await response.json()) as T
  } catch (err: unknown) {
    if (err instanceof ApiError) {
      throw err
    }
    const message = err instanceof Error ? err.message : 'Error desconocido de conexión'
    throw new ApiError(message, 0)
  }
}

export const api = {
  get: <T>(url: string, params?: Record<string, string | number | boolean | undefined>, options?: RequestOptions) =>
    request<T>(url, { method: 'GET', params, ...options }),

  post: <T>(url: string, body?: unknown, options?: RequestOptions) =>
    request<T>(url, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  put: <T>(url: string, body?: unknown, options?: RequestOptions) =>
    request<T>(url, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  patch: <T>(url: string, body?: unknown, options?: RequestOptions) =>
    request<T>(url, {
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  delete: <T>(url: string, options?: RequestOptions) =>
    request<T>(url, { method: 'DELETE', ...options }),
}
