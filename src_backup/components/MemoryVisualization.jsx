import React, { useState, useEffect } from 'react';

export default function MemoryVisualization({ user }) {
  const [memories, setMemories] = useState([]);
  const [selectedMemory, setSelectedMemory] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch real memories from backend
  useEffect(() => {
    const fetchMemories = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`http://localhost:9000/api/memories?user_id=${user?.id || 'default_user'}&limit=20`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const realMemories = await response.json();
        
        // Transform backend memories to frontend format
        const transformedMemories = realMemories.map((memory, index) => ({
          id: memory.id || index,
          type: 'learning_session', // Could be enhanced to detect type from content
          title: memory.content.substring(0, 50) + (memory.content.length > 50 ? '...' : ''),
          content: memory.response,
          timestamp: memory.timestamp ? new Date(memory.timestamp) : new Date(),
          importance: 'medium', // Could be enhanced with importance scoring
          tags: extractTags(memory.content) // Extract tags from content
        }));
        
        setMemories(transformedMemories);
      } catch (error) {
        console.error('Error fetching memories:', error);
        // Fallback to empty array - user will see "no memories" message
        setMemories([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMemories();
  }, [user]);

  // Helper function to extract tags from content
  const extractTags = (content) => {
    const words = content.toLowerCase().split(/\s+/);
    const commonTags = ['python', 'javascript', 'ai', 'ml', 'api', 'programming', 'coding', 'web', 'backend', 'frontend'];
    return commonTags.filter(tag => words.some(word => word.includes(tag))).slice(0, 3);
  };

  const getMemoryIcon = (type) => {
    switch (type) {
      case 'learning_session':
        return '📚';
      case 'project_work':
        return '🔧';
      case 'struggle':
        return '🤔';
      case 'breakthrough':
        return '💡';
      default:
        return '📝';
    }
  };

  const getImportanceColor = (importance) => {
    switch (importance) {
      case 'high':
        return 'border-red-400 bg-red-400/10';
      case 'medium':
        return 'border-yellow-400 bg-yellow-400/10';
      case 'low':
        return 'border-green-400 bg-green-400/10';
      default:
        return 'border-zinc-400 bg-zinc-400/10';
    }
  };

  const formatRelativeTime = (date) => {
    const now = new Date();
    const diffMs = now - date;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    return `${diffDays} days ago`;
  };

  return (
    <div className="bg-darkglass rounded-2xl p-6 shadow-glass backdrop-blur">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-accent">Your Learning Journey</h3>
        <div className="text-sm text-zinc-400">
          {memories.length} memories tracked
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Memory Timeline */}
          <div className="max-h-64 overflow-y-auto space-y-3">
            {memories.map((memory) => (
              <div
                key={memory.id}
                onClick={() => setSelectedMemory(memory)}
                className={`p-4 rounded-lg border cursor-pointer transition-all duration-200 hover:scale-[1.02] ${
                  getImportanceColor(memory.importance)
                } ${
                  selectedMemory?.id === memory.id ? 'ring-2 ring-accent' : ''
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{getMemoryIcon(memory.type)}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h4 className="font-semibold text-white truncate">
                        {memory.title}
                      </h4>
                      <span className="text-xs text-zinc-400 ml-2">
                        {formatRelativeTime(memory.timestamp)}
                      </span>
                    </div>
                    <p className="text-sm text-zinc-300 mt-1 line-clamp-2">
                      {memory.content}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {memory.tags.map((tag) => (
                        <span
                          key={tag}
                          className="px-2 py-1 text-xs bg-glass rounded-full text-zinc-300"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Memory Details Modal */}
          {selectedMemory && (
            <div className="mt-6 p-4 bg-glass rounded-lg border border-accent/30">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-accent">Memory Details</h4>
                <button
                  onClick={() => setSelectedMemory(null)}
                  className="text-zinc-400 hover:text-white"
                >
                  ✕
                </button>
              </div>
              <div className="space-y-2">
                <p><strong>Type:</strong> {selectedMemory.type.replace('_', ' ')}</p>
                <p><strong>When:</strong> {selectedMemory.timestamp.toLocaleDateString()}</p>
                <p><strong>Importance:</strong> <span className="capitalize">{selectedMemory.importance}</span></p>
                <p><strong>Content:</strong> {selectedMemory.content}</p>
                <div className="flex flex-wrap gap-1 mt-2">
                  {selectedMemory.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 text-xs bg-primary/20 rounded-full text-primary"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Learning Stats */}
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="bg-glass rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-primary">
                {memories.filter(m => m.type === 'learning_session').length}
              </div>
              <div className="text-xs text-zinc-400">Learning Sessions</div>
            </div>
            <div className="bg-glass rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-accent">
                {memories.filter(m => m.type === 'breakthrough').length}
              </div>
              <div className="text-xs text-zinc-400">Breakthroughs</div>
            </div>
            <div className="bg-glass rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-yellow-400">
                {memories.filter(m => m.importance === 'high').length}
              </div>
              <div className="text-xs text-zinc-400">Key Memories</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}