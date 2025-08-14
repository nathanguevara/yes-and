import { useEffect, useRef } from 'react'
import { useMutation, useQuery } from 'react-query'
import { ChatMessage } from './ChatMessage'
import { ChatInput, TypingIndicator } from './ChatInput'
import { useChatStore } from '@/stores/chat'
import { apiClient, getErrorMessage } from '@/services/api'
import { AlertCircle, Wifi, WifiOff } from 'lucide-react'

export function ChatInterface() {
  const {
    messages,
    currentHumorStyle,
    sessionId,
    isGenerating,
    showMetrics,
    addMessage,
    updateMessage,
    setIsGenerating,
    rateMessage,
  } = useChatStore()

  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Health check query
  const { data: healthData, isError: healthError } = useQuery(
    'health',
    () => apiClient.healthCheck(),
    {
      refetchInterval: 30000, // Check every 30 seconds
      retry: 2,
    }
  )

  // Submit feedback mutation
  const submitFeedbackMutation = useMutation(
    (data: { messageId: string; rating: number; userMessage: string; aiResponse: string }) =>
      apiClient.submitFeedback(
        data.userMessage,
        data.aiResponse,
        data.rating,
        currentHumorStyle,
        sessionId
      ),
    {
      onSuccess: () => {
        console.log('Feedback submitted successfully')
      },
      onError: (error) => {
        console.error('Failed to submit feedback:', getErrorMessage(error))
      },
    }
  )

  // Generate response mutation
  const generateResponseMutation = useMutation(
    (message: string) =>
      apiClient.generateResponse(
        message,
        currentHumorStyle,
        messages.map(msg => ({ role: msg.role, content: msg.content })),
        sessionId
      ),
    {
      onMutate: () => {
        setIsGenerating(true)
      },
      onSuccess: (response, userMessage) => {
        // Add the AI response
        addMessage({
          role: 'assistant',
          content: response.enhanced_response,
          humor_style: response.humor_style,
          metadata: {
            generation_time: response.metadata.generation_time,
            humor_score: response.metadata.humor_score,
            enhanced: response.enhanced,
          },
          awaitingRating: true,
        })
      },
      onError: (error) => {
        // Add error message
        addMessage({
          role: 'assistant',
          content: `Sorry, I encountered an error: ${getErrorMessage(error)}. Please check if the backend is running!`,
          humor_style: 'self_deprecating',
        })
      },
      onSettled: () => {
        setIsGenerating(false)
      },
    }
  )

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isGenerating])

  const handleSendMessage = (message: string) => {
    // Add user message
    addMessage({
      role: 'user',
      content: message,
    })

    // Generate AI response
    generateResponseMutation.mutate(message)
  }

  const handleRateMessage = (messageId: string, rating: number) => {
    const message = messages.find(msg => msg.id === messageId)
    if (!message) return

    // Find the user message that preceded this AI response
    const messageIndex = messages.findIndex(msg => msg.id === messageId)
    const userMessage = messageIndex > 0 ? messages[messageIndex - 1] : null

    if (userMessage?.role === 'user') {
      // Submit feedback to backend
      submitFeedbackMutation.mutate({
        messageId,
        rating,
        userMessage: userMessage.content,
        aiResponse: message.content,
      })
    }

    // Update local state
    rateMessage(messageId, rating)
  }

  const isSystemHealthy = healthData?.status === 'healthy' && !healthError
  const showHealthWarning = !isSystemHealthy && messages.length === 0

  return (
    <div className="flex flex-col h-full">
      {/* Health Status Warning */}
      {showHealthWarning && (
        <div className="mx-4 mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg flex items-center gap-2">
          <WifiOff size={16} className="text-yellow-600 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium">Backend Connection Issues</p>
            <p>The AI comedy engine appears to be offline. Check if the backend is running.</p>
          </div>
        </div>
      )}

      {/* System Status (when healthy) */}
      {isSystemHealthy && messages.length === 0 && (
        <div className="mx-4 mt-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2">
          <Wifi size={16} className="text-green-600" />
          <div className="text-sm text-green-800">
            <p className="font-medium">Connected to AI Comedy Engine</p>
            <p>Ready for some laughs! Start a conversation below.</p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && isSystemHealthy && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎭</div>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Ready for Some Comedy?
            </h2>
            <p className="text-gray-500 max-w-md mx-auto">
              I'm your AI comedy cohost! Try asking me something funny, share a story, 
              or just say hello. I'll respond with my signature {currentHumorStyle} style.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            id={message.id}
            role={message.role}
            content={message.content}
            timestamp={message.timestamp}
            humor_style={message.humor_style}
            metadata={message.metadata}
            rating={message.rating}
            awaitingRating={message.awaitingRating}
            showMetrics={showMetrics}
            onRate={(rating) => handleRateMessage(message.id, rating)}
          />
        ))}

        {isGenerating && <TypingIndicator isVisible={true} />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isGenerating}
        disabled={!isSystemHealthy}
        placeholder={
          isSystemHealthy 
            ? "Say something to your comedy partner..."
            : "Waiting for backend connection..."
        }
      />
    </div>
  )
}