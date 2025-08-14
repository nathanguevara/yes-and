import { useState } from 'react'
import { useQuery } from 'react-query'
import { 
  Settings, 
  BarChart3, 
  Trash2, 
  RefreshCw, 
  Info, 
  Heart,
  TrendingUp,
  Users,
  Clock,
  ChevronDown,
  ChevronUp
} from 'lucide-react'
import { Button, Card, CardHeader, CardTitle, CardContent } from '@/components/ui'
import { HumorStyleSelector } from './HumorStyleSelector'
import { useChatStore } from '@/stores/chat'
import { apiClient } from '@/services/api'
import clsx from 'clsx'

export function Sidebar() {
  const {
    currentHumorStyle,
    showMetrics,
    setHumorStyle,
    setShowMetrics,
    clearMessages,
    generateNewSession,
  } = useChatStore()

  const [expandedSections, setExpandedSections] = useState({
    controls: true,
    stats: true,
    modelInfo: false,
  })

  // Feedback stats query
  const { data: statsData } = useQuery(
    'feedback-stats',
    () => apiClient.getFeedbackStats(),
    {
      refetchInterval: 30000, // Refresh every 30 seconds
      retry: 2,
    }
  )

  // Model info query
  const { data: modelInfo } = useQuery(
    'model-info',
    () => apiClient.getModelInfo(),
    {
      retry: 2,
    }
  )

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const handleClearChat = () => {
    if (confirm('Are you sure you want to clear the chat history?')) {
      clearMessages()
    }
  }

  const handleNewSession = () => {
    if (confirm('Start a new session? This will clear the current conversation.')) {
      generateNewSession()
    }
  }

  return (
    <div className="w-80 h-full bg-gray-50 border-r border-gray-200 overflow-y-auto">
      <div className="p-4 space-y-4">
        {/* Header */}
        <div className="text-center py-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-1">
            🎭 Yes-And
          </h1>
          <p className="text-sm text-gray-600">
            AI Comedy Cohost
          </p>
        </div>

        {/* Controls Section */}
        <Card>
          <CardHeader className="pb-3">
            <button
              onClick={() => toggleSection('controls')}
              className="flex items-center justify-between w-full text-left"
            >
              <CardTitle className="flex items-center gap-2 text-base">
                <Settings size={16} />
                Comedy Controls
              </CardTitle>
              {expandedSections.controls ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
          </CardHeader>
          
          {expandedSections.controls && (
            <CardContent className="space-y-4">
              {/* Humor Style Selector */}
              <HumorStyleSelector
                value={currentHumorStyle}
                onChange={setHumorStyle}
              />

              {/* Settings Toggle */}
              <div className="flex items-center justify-between">
                <label htmlFor="show-metrics" className="text-sm font-medium text-gray-700">
                  Show Performance Metrics
                </label>
                <input
                  id="show-metrics"
                  type="checkbox"
                  checked={showMetrics}
                  onChange={(e) => setShowMetrics(e.target.checked)}
                  className="rounded border-gray-300 text-comedy-primary focus:ring-comedy-primary"
                />
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleClearChat}
                  className="flex items-center gap-1"
                >
                  <Trash2 size={14} />
                  Clear Chat
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleNewSession}
                  className="flex items-center gap-1"
                >
                  <RefreshCw size={14} />
                  New Session
                </Button>
              </div>
            </CardContent>
          )}
        </Card>

        {/* Statistics Section */}
        <Card>
          <CardHeader className="pb-3">
            <button
              onClick={() => toggleSection('stats')}
              className="flex items-center justify-between w-full text-left"
            >
              <CardTitle className="flex items-center gap-2 text-base">
                <BarChart3 size={16} />
                Feedback Stats
              </CardTitle>
              {expandedSections.stats ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
          </CardHeader>
          
          {expandedSections.stats && (
            <CardContent>
              {statsData && statsData.total_ratings > 0 ? (
                <div className="space-y-4">
                  {/* Overall Stats */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-center gap-1 mb-1">
                        <Heart size={14} className="text-red-500" />
                        <span className="text-xs text-gray-600">Avg Rating</span>
                      </div>
                      <div className="text-lg font-semibold text-gray-900">
                        {statsData.average_rating.toFixed(1)}
                      </div>
                    </div>
                    
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-center gap-1 mb-1">
                        <Users size={14} className="text-blue-500" />
                        <span className="text-xs text-gray-600">Total</span>
                      </div>
                      <div className="text-lg font-semibold text-gray-900">
                        {statsData.total_ratings}
                      </div>
                    </div>
                  </div>

                  {/* Rating Distribution */}
                  {statsData.rating_distribution && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Rating Distribution</h4>
                      <div className="space-y-1">
                        {[5, 4, 3, 2, 1].map(rating => {
                          const count = statsData.rating_distribution[rating.toString()] || 0
                          const percentage = statsData.total_ratings > 0 
                            ? (count / statsData.total_ratings * 100).toFixed(0)
                            : '0'
                          
                          return (
                            <div key={rating} className="flex items-center gap-2 text-xs">
                              <span className="w-3 text-gray-600">{rating}★</span>
                              <div className="flex-1 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-comedy-primary h-2 rounded-full transition-all duration-300"
                                  style={{ width: `${percentage}%` }}
                                />
                              </div>
                              <span className="w-8 text-gray-600 text-right">{count}</span>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )}

                  {/* Style Performance */}
                  {statsData.by_humor_style && Object.keys(statsData.by_humor_style).length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Performance by Style</h4>
                      <div className="space-y-2">
                        {Object.entries(statsData.by_humor_style).map(([style, data]) => (
                          <div key={style} className="flex justify-between items-center text-xs">
                            <span className="capitalize text-gray-600">{style}</span>
                            <div className="text-right">
                              <div className="font-medium">{data.average.toFixed(1)}★</div>
                              <div className="text-gray-500">({data.count})</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-6 text-gray-500">
                  <BarChart3 size={32} className="mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No ratings yet</p>
                  <p className="text-xs">Rate responses to see stats!</p>
                </div>
              )}
            </CardContent>
          )}
        </Card>

        {/* Model Info Section */}
        <Card>
          <CardHeader className="pb-3">
            <button
              onClick={() => toggleSection('modelInfo')}
              className="flex items-center justify-between w-full text-left"
            >
              <CardTitle className="flex items-center gap-2 text-base">
                <Info size={16} />
                Model Info
              </CardTitle>
              {expandedSections.modelInfo ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
          </CardHeader>
          
          {expandedSections.modelInfo && (
            <CardContent>
              {modelInfo ? (
                <div className="space-y-3 text-xs">
                  <div>
                    <span className="font-medium text-gray-700">Model:</span>
                    <span className="ml-2 text-gray-600">{modelInfo.model_name}</span>
                  </div>
                  
                  {modelInfo.ollama_version && (
                    <div>
                      <span className="font-medium text-gray-700">Ollama:</span>
                      <span className="ml-2 text-gray-600">{modelInfo.ollama_version}</span>
                    </div>
                  )}
                  
                  {modelInfo.generation_params && (
                    <div>
                      <span className="font-medium text-gray-700 block mb-1">Parameters:</span>
                      <div className="pl-2 space-y-1 text-gray-600">
                        <div>Temperature: {modelInfo.generation_params.temperature}</div>
                        <div>Top-P: {modelInfo.generation_params.top_p}</div>
                        <div>Max Tokens: {modelInfo.generation_params.max_tokens}</div>
                      </div>
                    </div>
                  )}
                  
                  {modelInfo.available_humor_styles && (
                    <div>
                      <span className="font-medium text-gray-700 block mb-1">Styles:</span>
                      <div className="flex flex-wrap gap-1">
                        {modelInfo.available_humor_styles.map(style => (
                          <span
                            key={style}
                            className="px-2 py-1 bg-gray-100 rounded text-gray-600"
                          >
                            {style}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  <Info size={24} className="mx-auto mb-2 opacity-50" />
                  <p className="text-sm">Loading model info...</p>
                </div>
              )}
            </CardContent>
          )}
        </Card>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500 py-4">
          <p>Built with ❤️ for comedy</p>
          <p className="mt-1">v1.0.0</p>
        </div>
      </div>
    </div>
  )
}