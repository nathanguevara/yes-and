export interface Message {
  role: 'user' | 'assistant'
  content: string
}

export interface ConversationHistory extends Message {
  id?: string
  timestamp?: string
}

export interface GenerateRequest {
  user_input: string
  humor_style?: HumorStyle
  conversation_history?: ConversationHistory[]
  session_id?: string
}

export interface GenerateResponse {
  response: string
  enhanced_response: string
  metadata: {
    generation_time: number
    humor_score: number
  }
  humor_style: string
  enhanced: boolean
}

export interface FeedbackRequest {
  user_input: string
  ai_response: string
  rating: number
  humor_style: string
  session_id?: string
}

export interface FeedbackResponse {
  message: string
}

export interface HealthResponse {
  status: string
  model: string
  ollama_host: string
  timestamp: string
  ollama_connection: string
  feedback_system: string
  ollama_available?: boolean
}

export interface FeedbackStats {
  total_ratings: number
  average_rating: number
  rating_distribution: Record<string, number>
  by_humor_style: Record<string, {
    count: number
    average: number
  }>
  period: string
}

export interface ModelInfo {
  model_name: string
  ollama_version: string
  available_humor_styles: string[]
  generation_params: {
    temperature: number
    top_p: number
    max_tokens: number
  }
}

export interface ApiError {
  detail: string
  error_code?: string
  timestamp?: string
}

export type HumorStyle = 'witty' | 'sarcastic' | 'observational' | 'self_deprecating' | 'absurd'

export const HUMOR_STYLES: Record<HumorStyle, { label: string; description: string; emoji: string }> = {
  witty: {
    label: 'Witty',
    description: 'Clever wordplay and smart observations',
    emoji: '🧠'
  },
  sarcastic: {
    label: 'Sarcastic', 
    description: 'Dry humor with a hint of irony',
    emoji: '😏'
  },
  observational: {
    label: 'Observational',
    description: 'Funny takes on everyday situations',
    emoji: '🔍'
  },
  self_deprecating: {
    label: 'Self-Deprecating',
    description: 'Humble humor at one\'s own expense',
    emoji: '😅'
  },
  absurd: {
    label: 'Absurd',
    description: 'Wildly imaginative and unexpected humor',
    emoji: '🤡'
  }
}