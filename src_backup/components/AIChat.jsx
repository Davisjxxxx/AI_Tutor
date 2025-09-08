import React, { useState, useRef, useEffect } from 'react';

export default function AIChat({ user }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm AURA, your AI tutor. I'm here to help you learn, remember context, and adapt to your needs. What would you like to work on today?",
      sender: 'ai',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getAIResponse = async (userMessage) => {
    try {
      const response = await fetch('http://localhost:9000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: user?.id || 'default_user',
          engine: 'llama' // Could be made configurable
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'AI response failed');
      }

      return data.response;
    } catch (error) {
      console.error('Error calling AI API:', error);
      // Fallback to a helpful error message
      return "I'm having trouble connecting right now. Please check that the backend server is running on port 9000 and try again.";
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const aiResponse = await getAIResponse(inputValue);
      
      setTimeout(() => {
        const aiMessage = {
          id: Date.now() + 1,
          text: aiResponse,
          sender: 'ai',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
        setIsTyping(false);
      }, 500);
    } catch (error) {
      console.error('Error getting AI response:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm having trouble connecting right now. Please try again in a moment.",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="bg-darkglass rounded-2xl p-6 shadow-glass backdrop-blur">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-primary">AURA AI Tutor</h3>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
          <span className="text-sm text-zinc-400">Online</span>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="chat-container mb-4 p-4 bg-glass rounded-lg">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message mb-4 flex ${
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-primary text-white'
                  : 'bg-glass text-white border border-primary/30'
              }`}
            >
              <p className="text-sm">{message.text}</p>
              <p className="text-xs opacity-70 mt-1">
                {formatTime(message.timestamp)}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start mb-4">
            <div className="bg-glass border border-primary/30 rounded-lg px-4 py-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSendMessage} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask AURA anything about learning, coding, or your projects..."
          className="flex-1 px-4 py-3 rounded-lg bg-glass text-white border border-primary/30 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className={`px-6 py-3 rounded-lg font-bold transition-all duration-200 ${
            isLoading || !inputValue.trim()
              ? 'bg-zinc-600 text-zinc-400 cursor-not-allowed'
              : 'bg-accent text-white hover:bg-primary shadow-glass'
          }`}
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin"></div>
          ) : (
            'Send'
          )}
        </button>
      </form>

      {/* Quick Actions */}
      <div className="mt-4 flex flex-wrap gap-2">
        <button
          onClick={() => setInputValue("Help me understand this concept better")}
          className="px-3 py-1 text-sm bg-glass rounded-lg border border-primary/30 text-zinc-300 hover:bg-primary/20 transition"
        >
          Explain concept
        </button>
        <button
          onClick={() => setInputValue("Show me a practical example")}
          className="px-3 py-1 text-sm bg-glass rounded-lg border border-primary/30 text-zinc-300 hover:bg-primary/20 transition"
        >
          Show example
        </button>
        <button
          onClick={() => setInputValue("I'm feeling stuck, can you help?")}
          className="px-3 py-1 text-sm bg-glass rounded-lg border border-primary/30 text-zinc-300 hover:bg-primary/20 transition"
        >
          I'm stuck
        </button>
      </div>
    </div>
  );
}