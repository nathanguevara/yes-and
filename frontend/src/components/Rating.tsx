import { useState } from 'react'
import clsx from 'clsx'

interface RatingProps {
  onRate: (rating: number) => void
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const RATING_OPTIONS = [
  { value: 1, emoji: '😴', label: 'Not funny', color: 'hover:bg-red-100' },
  { value: 2, emoji: '🙂', label: 'Slightly amusing', color: 'hover:bg-orange-100' },
  { value: 3, emoji: '😄', label: 'Pretty good', color: 'hover:bg-yellow-100' },
  { value: 4, emoji: '😂', label: 'Very funny', color: 'hover:bg-green-100' },
  { value: 5, emoji: '🤣', label: 'Hilarious!', color: 'hover:bg-purple-100' },
]

export function Rating({ onRate, disabled = false, size = 'md' }: RatingProps) {
  const [hoveredRating, setHoveredRating] = useState<number | null>(null)

  const sizeClasses = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-lg',
    lg: 'w-12 h-12 text-xl',
  }

  return (
    <div className="flex gap-2 justify-center">
      {RATING_OPTIONS.map((option) => (
        <button
          key={option.value}
          onClick={() => onRate(option.value)}
          onMouseEnter={() => setHoveredRating(option.value)}
          onMouseLeave={() => setHoveredRating(null)}
          disabled={disabled}
          className={clsx(
            'rating-button transition-all duration-200',
            sizeClasses[size],
            option.color,
            {
              'opacity-50 cursor-not-allowed': disabled,
              'transform scale-110': hoveredRating === option.value,
            }
          )}
          title={option.label}
          aria-label={`Rate ${option.value} out of 5: ${option.label}`}
        >
          <span role="img" aria-label={option.label}>
            {option.emoji}
          </span>
        </button>
      ))}
    </div>
  )
}

interface RatingDisplayProps {
  rating: number
  showLabel?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export function RatingDisplay({ rating, showLabel = false, size = 'sm' }: RatingDisplayProps) {
  const option = RATING_OPTIONS.find(opt => opt.value === rating)
  
  if (!option) return null

  const sizeClasses = {
    sm: 'w-6 h-6 text-sm',
    md: 'w-8 h-8 text-base',
    lg: 'w-10 h-10 text-lg',
  }

  return (
    <div className="flex items-center gap-2">
      <div className={clsx('flex items-center justify-center', sizeClasses[size])}>
        <span role="img" aria-label={option.label}>
          {option.emoji}
        </span>
      </div>
      {showLabel && (
        <span className="text-sm text-gray-600">
          {rating}/5 - {option.label}
        </span>
      )}
    </div>
  )
}