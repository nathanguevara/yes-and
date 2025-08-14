import axios, { AxiosInstance, AxiosError } from 'axios'
import type {
  GenerateRequest,
  GenerateResponse,
  FeedbackRequest,
  FeedbackResponse,
  HealthResponse,
  FeedbackStats,
  ModelInfo,
  ApiError,
  ConversationHistory,
  HumorStyle,
} from '@/types/api'

class ComedyAPIClient {
  private client: AxiosInstance
  private baseURL: string

  constructor(baseURL: string = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') {
    this.baseURL = baseURL
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        const apiError: ApiError = {
          detail: error.response?.data?.detail || error.message || 'Unknown error occurred',
          error_code: error.response?.data?.error_code,
          timestamp: error.response?.data?.timestamp || new Date().toISOString(),
        }
        return Promise.reject(apiError)
      }
    )
  }

  /**
   * Check API health status
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health')
    return response.data
  }

  /**
   * Quick boolean health check
   */
  async isHealthy(): Promise<boolean> {
    try {
      const health = await this.healthCheck()
      return health.status === 'healthy'
    } catch {
      return false
    }
  }

  /**
   * Generate a humorous response
   */
  async generateResponse(
    message: string,
    humorStyle: HumorStyle = 'witty',
    conversationHistory: ConversationHistory[] = [],
    sessionId?: string
  ): Promise<GenerateResponse> {
    const request: GenerateRequest = {
      user_input: message,
      humor_style: humorStyle,
      conversation_history: conversationHistory,
      session_id: sessionId,
    }

    const response = await this.client.post<GenerateResponse>('/generate', request)
    return response.data
  }

  /**
   * Submit user feedback for a response
   */
  async submitFeedback(
    message: string,
    response: string,
    rating: number,
    humorStyle: string,
    sessionId?: string
  ): Promise<FeedbackResponse> {
    const request: FeedbackRequest = {
      user_input: message,
      ai_response: response,
      rating,
      humor_style: humorStyle,
      session_id: sessionId,
    }

    const apiResponse = await this.client.post<FeedbackResponse>('/feedback', request)
    return apiResponse.data
  }

  /**
   * Get feedback statistics
   */
  async getFeedbackStats(humorStyle?: string, days?: number): Promise<FeedbackStats> {
    const params: Record<string, string> = {}
    if (humorStyle) params.humor_style = humorStyle
    if (days) params.days = days.toString()

    const response = await this.client.get<FeedbackStats>('/feedback/stats', { params })
    return response.data
  }

  /**
   * Get model information
   */
  async getModelInfo(): Promise<ModelInfo> {
    const response = await this.client.get<ModelInfo>('/model/info')
    return response.data
  }

  /**
   * Get root API information
   */
  async getApiInfo(): Promise<{ name: string; version: string; description: string }> {
    const response = await this.client.get('/')
    return response.data
  }
}

// Create and export a singleton instance
export const apiClient = new ComedyAPIClient()

// Export error handling utilities
export const isApiError = (error: unknown): error is ApiError => {
  return typeof error === 'object' && error !== null && 'detail' in error
}

export const getErrorMessage = (error: unknown): string => {
  if (isApiError(error)) {
    return error.detail
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unexpected error occurred'
}