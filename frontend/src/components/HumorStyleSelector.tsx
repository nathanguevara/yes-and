import clsx from 'clsx'
import { Select } from '@/components/ui'
import { HUMOR_STYLES, type HumorStyle } from '@/types/api'

interface HumorStyleSelectorProps {
  value: HumorStyle
  onChange: (style: HumorStyle) => void
  disabled?: boolean
}

export function HumorStyleSelector({ value, onChange, disabled }: HumorStyleSelectorProps) {
  return (
    <div className="space-y-2">
      <Select
        label="Humor Style"
        value={value}
        onChange={(e) => onChange(e.target.value as HumorStyle)}
        disabled={disabled}
      >
        {Object.entries(HUMOR_STYLES).map(([key, style]) => (
          <option key={key} value={key}>
            {style.emoji} {style.label}
          </option>
        ))}
      </Select>
      
      {/* Show description for selected style */}
      <p className="text-sm text-gray-600 px-1">
        {HUMOR_STYLES[value].description}
      </p>
    </div>
  )
}

interface HumorStyleBadgeProps {
  style: HumorStyle
  size?: 'sm' | 'md'
}

export function HumorStyleBadge({ style, size = 'sm' }: HumorStyleBadgeProps) {
  const styleInfo = HUMOR_STYLES[style]
  
  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
  }

  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1 bg-comedy-primary/10 text-comedy-primary rounded-full font-medium',
        sizeClasses[size]
      )}
      title={styleInfo.description}
    >
      <span role="img" aria-label={styleInfo.label}>
        {styleInfo.emoji}
      </span>
      {styleInfo.label}
    </span>
  )
}