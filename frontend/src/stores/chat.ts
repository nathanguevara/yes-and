import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { HumorStyle, ConversationHistory } from '@/types/api'

interface ChatMessage extends ConversationHistory {
  id: string
  timestamp: string
  humor_style?: string
  metadata?: {
    generation_time?: number
    humor_score?: number
    enhanced?: boolean
  }
  rating?: number
  awaitingRating?: boolean
}

interface ChatState {
  // State
  messages: ChatMessage[]
  currentHumorStyle: HumorStyle
  sessionId: string
  isGenerating: boolean
  showMetrics: boolean
  
  // Actions
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  updateMessage: (id: string, updates: Partial<ChatMessage>) => void
  deleteMessage: (id: string) => void
  clearMessages: () => void
  setHumorStyle: (style: HumorStyle) => void
  setIsGenerating: (generating: boolean) => void
  setShowMetrics: (show: boolean) => void
  generateNewSession: () => void
  rateMessage: (id: string, rating: number) => void
}

const generateSessionId = () => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      // Initial state
      messages: [],
      currentHumorStyle: 'witty',
      sessionId: generateSessionId(),
      isGenerating: false,
      showMetrics: false,

      // Actions
      addMessage: (message) => {
        const newMessage: ChatMessage = {
          ...message,
          id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          timestamp: new Date().toISOString(),
        }
        
        set((state) => ({
          messages: [...state.messages, newMessage]
        }))
      },

      updateMessage: (id, updates) => {
        set((state) => ({
          messages: state.messages.map((msg) =>
            msg.id === id ? { ...msg, ...updates } : msg
          )
        }))
      },

      deleteMessage: (id) => {
        set((state) => ({
          messages: state.messages.filter((msg) => msg.id !== id)
        }))
      },

      clearMessages: () => {
        set({ messages: [] })
      },

      setHumorStyle: (style) => {
        set({ currentHumorStyle: style })
      },

      setIsGenerating: (generating) => {
        set({ isGenerating: generating })
      },

      setShowMetrics: (show) => {
        set({ showMetrics: show })
      },

      generateNewSession: () => {
        set({
          sessionId: generateSessionId(),
          messages: []
        })
      },

      rateMessage: (id, rating) => {
        set((state) => ({
          messages: state.messages.map((msg) =>
            msg.id === id 
              ? { ...msg, rating, awaitingRating: false }
              : msg
          )
        }))
      },
    }),
    {
      name: 'yes-and-chat-storage',
      partialize: (state) => ({
        currentHumorStyle: state.currentHumorStyle,
        showMetrics: state.showMetrics,
        sessionId: state.sessionId,
        // Don't persist messages for privacy, but could be configurable
      }),
    }
  )
)