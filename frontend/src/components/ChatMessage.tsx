import { formatDistanceToNow } from 'date-fns'
import { User, Bot, Clock, Zap, TrendingUp } from 'lucide-react'
import clsx from 'clsx'
import { Rating, RatingDisplay } from './Rating'
import { HumorStyleBadge } from './HumorStyleSelector'
import type { HumorStyle } from '@/types/api'

interface ChatMessageProps {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  humor_style?: string
  metadata?: {
    generation_time?: number
    humor_score?: number
    enhanced?: boolean
  }
  rating?: number
  awaitingRating?: boolean
  showMetrics?: boolean
  onRate?: (rating: number) => void
}

export function ChatMessage({
  id,
  role,
  content,
  timestamp,
  humor_style,
  metadata,
  rating,
  awaitingRating,
  showMetrics,
  onRate,
}: ChatMessageProps) {
  const isUser = role === 'user'
  const timeAgo = formatDistanceToNow(new Date(timestamp), { addSuffix: true })

  return (
    <div
      className={clsx(
        'flex gap-3 mb-6 animate-in slide-in-from-bottom-2 duration-300',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
    >
      {/* Avatar */}
      <div
        className={clsx(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          isUser 
            ? 'bg-comedy-primary text-white' 
            : 'bg-comedy-secondary text-white'
        )}
      >
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Message Content */}
      <div className={clsx('flex flex-col max-w-[70%]', isUser ? 'items-end' : 'items-start')}>
        {/* Message Bubble */}
        <div
          className={clsx(
            'px-4 py-3 rounded-2xl shadow-sm',
            isUser
              ? 'bg-comedy-primary text-white rounded-br-sm'
              : 'bg-white border border-gray-200 rounded-bl-sm'
          )}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {content}
          </p>
        </div>

        {/* Message Metadata */}
        <div className="flex items-center gap-2 mt-1 px-1">
          <span className="text-xs text-gray-500">{timeAgo}</span>
          
          {!isUser && humor_style && (
            <HumorStyleBadge style={humor_style as HumorStyle} size="sm" />
          )}
          
          {!isUser && rating && (
            <RatingDisplay rating={rating} size="sm" />
          )}
        </div>

        {/* Performance Metrics */}
        {!isUser && showMetrics && metadata && (
          <div className="mt-2 p-3 bg-gray-50 rounded-lg border border-gray-200 text-xs space-y-2 w-full">
            <h4 className="font-medium text-gray-700 mb-2 flex items-center gap-1">
              <TrendingUp size={12} />
              Performance Metrics
            </h4>
            
            <div className="grid grid-cols-3 gap-3">
              {metadata.generation_time !== undefined && (
                <div className="flex items-center gap-1">
                  <Clock size={10} className="text-gray-400" />
                  <span className="text-gray-600">
                    {metadata.generation_time.toFixed(2)}s
                  </span>
                </div>
              )}
              
              {metadata.humor_score !== undefined && (
                <div className="flex items-center gap-1">
                  <span className="text-gray-400">😄</span>
                  <span className="text-gray-600">
                    {metadata.humor_score.toFixed(2)}
                  </span>
                </div>
              )}
              
              {metadata.enhanced !== undefined && (
                <div className="flex items-center gap-1">
                  <Zap size={10} className="text-gray-400" />
                  <span className="text-gray-600">
                    {metadata.enhanced ? 'Enhanced' : 'Original'}
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Rating Widget */}
        {!isUser && awaitingRating && onRate && (
          <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200 w-full">
            <p className="text-sm text-blue-800 mb-2 text-center">
              How funny was that? Rate this response:
            </p>
            <Rating onRate={onRate} size="sm" />
          </div>
        )}
      </div>
    </div>
  )
}