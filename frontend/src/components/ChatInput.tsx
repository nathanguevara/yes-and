import { useState, KeyboardEvent } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui'
import clsx from 'clsx'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  isLoading?: boolean
  disabled?: boolean
  placeholder?: string
}

export function ChatInput({ 
  onSendMessage, 
  isLoading = false, 
  disabled = false,
  placeholder = "Say something to your comedy partner..."
}: ChatInputProps) {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    const trimmedMessage = message.trim()
    if (trimmedMessage && !isLoading && !disabled) {
      onSendMessage(trimmedMessage)
      setMessage('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const canSend = message.trim().length > 0 && !isLoading && !disabled

  return (
    <div className="flex gap-2 items-end p-4 bg-white border-t border-gray-200">
      <div className="flex-1 relative">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={disabled || isLoading}
          rows={1}
          className={clsx(
            'w-full px-4 py-3 pr-12 border border-gray-300 rounded-2xl resize-none',
            'focus:outline-none focus:ring-2 focus:ring-comedy-primary focus:border-comedy-primary',
            'disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed',
            'placeholder:text-gray-400',
            'max-h-32 overflow-y-auto',
            {
              'opacity-50': disabled || isLoading,
            }
          )}
          style={{
            minHeight: '48px',
            height: Math.min(Math.max(48, (message.split('\n').length) * 24 + 24), 128)
          }}
        />
        
        {/* Character count (optional) */}
        {message.length > 100 && (
          <div className="absolute -top-6 right-0 text-xs text-gray-400">
            {message.length} characters
          </div>
        )}
      </div>

      <Button
        onClick={handleSend}
        disabled={!canSend}
        isLoading={isLoading}
        size="md"
        className="h-12 w-12 rounded-2xl p-0 flex-shrink-0"
        aria-label="Send message"
      >
        {isLoading ? (
          <Loader2 size={20} className="animate-spin" />
        ) : (
          <Send size={20} />
        )}
      </Button>
    </div>
  )
}

interface TypingIndicatorProps {
  isVisible: boolean
}

export function TypingIndicator({ isVisible }: TypingIndicatorProps) {
  if (!isVisible) return null

  return (
    <div className="flex gap-3 mb-6 animate-in slide-in-from-bottom-2 duration-300">
      {/* Avatar */}
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-comedy-secondary text-white flex items-center justify-center">
        <span className="text-sm">🤖</span>
      </div>

      {/* Typing Animation */}
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1 items-center">
          <span className="text-sm text-gray-600 mr-2">Cooking up something funny</span>
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      </div>
    </div>
  )
}