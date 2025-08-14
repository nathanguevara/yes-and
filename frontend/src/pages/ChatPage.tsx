import { ChatInterface } from '@/components/ChatInterface'
import { Sidebar } from '@/components/Sidebar'

export function ChatPage() {
  return (
    <div className="h-screen flex">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <ChatInterface />
      </div>
    </div>
  )
}