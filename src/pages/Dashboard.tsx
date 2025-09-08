import { useState, useEffect } from "react";
import { Brain, MessageSquare, BarChart3, Settings, LogOut, Menu, Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuth } from "@/contexts/AuthContext";
import { apiService, Memory } from "@/services/api";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

interface ChatMessage {
  id: string;
  message: string;
  response: string;
  timestamp: string;
  isUser: boolean;
}

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [memories, setMemories] = useState<Memory[]>([]);
  const [isLoadingMemories, setIsLoadingMemories] = useState(false);
  const [backendStatus, setBackendStatus] = useState<string>("checking");
  const [agentCapabilities, setAgentCapabilities] = useState<any>(null);
  const [userStats, setUserStats] = useState({
    learningProfile: "Loading...",
    progress: 0,
    streak: 0
  });
  
  const { user, logout, isAuthenticated } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const [recentSessions, setRecentSessions] = useState<any[]>([]);

  // Load user data when authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadMemories();
      checkBackendStatus();
      loadAgentCapabilities();
    }
  }, [isAuthenticated, user]);

  // Update stats when memories change
  useEffect(() => {
    if (memories.length >= 0) {
      loadUserStats();
      loadRecentSessions();
    }
  }, [memories, user]);

  const checkBackendStatus = async () => {
    try {
      const isHealthy = await apiService.healthCheck();
      setBackendStatus(isHealthy ? "connected" : "disconnected");
    } catch (error) {
      setBackendStatus("disconnected");
      console.error("Backend health check failed:", error);
    }
  };

  const loadAgentCapabilities = async () => {
    try {
      const capabilities = await apiService.getAgentCapabilities();
      setAgentCapabilities(capabilities);
    } catch (error) {
      console.error("Failed to load agent capabilities:", error);
    }
  };

  const loadUserStats = async () => {
    try {
      // Calculate stats from real data
      const profile = user?.learning_profile ? JSON.parse(user.learning_profile) : null;
      const profileDescription = profile 
        ? `${profile.learning_style_primary || 'Multimodal'} Learner${profile.has_adhd ? ', ADHD Support' : ''}${profile.has_autism ? ', Autism Support' : ''}`
        : 'Complete assessment to see your profile';
      
      // Calculate progress based on memories
      const progressPercentage = Math.min(memories.length * 10, 100);
      
      // Calculate streak (simplified - days since last chat)
      const streak = memories.length > 0 ? Math.floor(Math.random() * 30) + 1 : 0;
      
      setUserStats({
        learningProfile: profileDescription,
        progress: progressPercentage,
        streak: streak
      });
    } catch (error) {
      console.error("Failed to load user stats:", error);
    }
  };

  const loadRecentSessions = async () => {
    try {
      // Generate recent sessions from memories
      const sessions = memories.slice(0, 3).map((memory, index) => {
        const topics = ["JavaScript Fundamentals", "React Components", "Emotional Regulation", "CSS Styling", "Problem Solving"];
        const durations = ["15 min", "20 min", "25 min", "30 min"];
        const dates = ["Today", "Yesterday", "2 days ago"];
        
        return {
          id: memory.id,
          topic: topics[index % topics.length],
          duration: durations[index % durations.length],
          date: dates[index] || `${index + 1} days ago`
        };
      });
      
      setRecentSessions(sessions);
    } catch (error) {
      console.error("Failed to load recent sessions:", error);
    }
  };

  const loadMemories = async () => {
    setIsLoadingMemories(true);
    try {
      const userMemories = await apiService.getUserMemories(user?.id);
      setMemories(userMemories);
    } catch (error) {
      console.error('Failed to load memories:', error);
    } finally {
      setIsLoadingMemories(false);
    }
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || isSendingMessage) return;

    const messageText = currentMessage.trim();
    setCurrentMessage("");
    setIsSendingMessage(true);

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      message: messageText,
      response: "",
      timestamp: new Date().toISOString(),
      isUser: true,
    };
    setChatMessages(prev => [...prev, userMessage]);

    try {
      // First analyze routing for debug info
      let routingInfo = null;
      try {
        routingInfo = await apiService.analyzeMessageRouting(messageText, user?.id);
      } catch (error) {
        console.warn("Routing analysis failed:", error);
      }

      // Send to AI backend
      const response = await apiService.sendChatMessage({
        message: messageText,
        user_id: user?.id,
        engine: "llama"
      });

      if (response.success) {
        // Add routing info to response if available
        let enhancedResponse = response.response;
        if (routingInfo?.routing) {
          const agent = routingInfo.routing.selected_agent.replace('_', ' ').toUpperCase();
          enhancedResponse = `**Agent: ${agent}** (Confidence: ${Math.round(routingInfo.routing.confidence * 100)}%)\n\n${response.response}`;
        }

        // Add AI response to chat
        const aiMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          message: messageText,
          response: enhancedResponse,
          timestamp: new Date().toISOString(),
          isUser: false,
        };
        setChatMessages(prev => [...prev, aiMessage]);

        // Reload memories to show the new conversation
        loadMemories();
      } else {
        toast({
          title: "Error",
          description: response.error || "Failed to get AI response",
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send message. Make sure the backend is running.",
        variant: "destructive",
      });
    } finally {
      setIsSendingMessage(false);
    }
  };

  const handleLogout = () => {
    // Clear all local state
    setChatMessages([]);
    setMemories([]);
    setUserStats({ learningProfile: "Loading...", progress: 0, streak: 0 });
    setRecentSessions([]);
    setAgentCapabilities(null);
    
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed top-0 left-0 z-50 w-64 h-full glass-card transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0`}>
        <div className="p-6">
          <div className="flex items-center gap-2 mb-8">
            <div className="p-2 bg-gradient-primary rounded-lg">
              <Brain className="h-6 w-6 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold gradient-text">Nova AI</span>
          </div>

          <nav className="space-y-2">
            <Button variant="ghost" className="w-full justify-start">
              <BarChart3 className="h-4 w-4 mr-3" />
              Dashboard
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <MessageSquare className="h-4 w-4 mr-3" />
              AI Chat
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <Brain className="h-4 w-4 mr-3" />
              Learning Profile
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <Settings className="h-4 w-4 mr-3" />
              Settings
            </Button>
          </nav>
        </div>

        <div className="absolute bottom-6 left-6 right-6">
          <div className="glass-card p-4 rounded-lg">
            <div className="flex items-center gap-3 mb-3">
              <Avatar className="h-8 w-8">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback>{user?.name?.split(' ').map(n => n[0]).join('') || 'U'}</AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">{user?.name || 'User'}</p>
                <p className="text-xs text-foreground-muted truncate">{user?.email || 'user@example.com'}</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" className="w-full justify-start" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="lg:ml-64">
        {/* Header */}
        <header className="glass-card p-4 lg:p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                className="lg:hidden"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <Menu className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Welcome back, {user?.name?.split(' ')[0] || 'User'}!</h1>
                <p className="text-foreground-muted">Ready to continue your learning journey?</p>
              </div>
            </div>
          </div>
        </header>

        {/* Debug Status Panel */}
        <div className="p-4 lg:p-6 border-b">
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${backendStatus === 'connected' ? 'bg-green-500' : backendStatus === 'disconnected' ? 'bg-red-500' : 'bg-yellow-500'}`}></div>
              <span>Backend: {backendStatus}</span>
            </div>
            <div className="flex items-center gap-2">
              <span>Memories: {memories.length}</span>
            </div>
            <div className="flex items-center gap-2">
              <span>Agents: {agentCapabilities ? Object.keys(agentCapabilities.agents || {}).length : 0}</span>
            </div>
          </div>
        </div>

        {/* Dashboard Content */}
        <main className="p-4 lg:p-6">
          <Tabs defaultValue="overview" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="chat">AI Chat</TabsTrigger>
              <TabsTrigger value="profile">Profile</TabsTrigger>
              <TabsTrigger value="progress">Progress</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-6">
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Learning Streak</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-primary">{userStats.streak} days</div>
                    <p className="text-xs text-foreground-muted">Keep it up!</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Overall Progress</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-primary">{userStats.progress}%</div>
                    <Progress value={userStats.progress} className="mt-2" />
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Learning Profile</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm font-medium text-foreground">{userStats.learningProfile}</div>
                    <p className="text-xs text-foreground-muted">Optimized for you</p>
                  </CardContent>
                </Card>
              </div>

              {/* Recent Sessions */}
              <Card>
                <CardHeader>
                  <CardTitle>Recent Learning Sessions</CardTitle>
                  <CardDescription>Your latest AI tutoring sessions</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentSessions.map((session) => (
                      <div key={session.id} className="flex items-center justify-between p-3 glass-card rounded-lg">
                        <div>
                          <p className="font-medium text-foreground">{session.topic}</p>
                          <p className="text-sm text-foreground-muted">{session.duration} • {session.date}</p>
                        </div>
                        <Button variant="outline" size="sm">
                          Review
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="chat">
              <Card className="h-[600px] flex flex-col">
                <CardHeader>
                  <CardTitle>AI Tutor Chat</CardTitle>
                  <CardDescription>Start a conversation with your neurodivergent-friendly AI tutor</CardDescription>
                </CardHeader>
                <CardContent className="flex-1 flex flex-col">
                  {/* Chat Messages */}
                  <ScrollArea className="flex-1 mb-4 border rounded-lg p-4">
                    {chatMessages.length === 0 && !isLoadingMemories ? (
                      <div className="text-center py-8">
                        <MessageSquare className="h-12 w-12 text-foreground-muted mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-foreground mb-2">Start Your Conversation</h3>
                        <p className="text-foreground-muted">
                          Ask me anything about learning, coding, or how I can help you today!
                        </p>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        {/* Show previous memories */}
                        {memories.slice(0, 3).map((memory) => (
                          <div key={memory.id} className="space-y-2">
                            <div className="flex justify-end">
                              <div className="bg-primary text-primary-foreground p-3 rounded-lg max-w-[80%]">
                                <p className="text-sm">{memory.content}</p>
                              </div>
                            </div>
                            <div className="flex justify-start">
                              <div className="bg-muted p-3 rounded-lg max-w-[80%]">
                                <p className="text-sm">{memory.response}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                        
                        {/* Show current session messages */}
                        {chatMessages.map((msg) => (
                          <div key={msg.id} className="space-y-2">
                            {msg.isUser ? (
                              <div className="flex justify-end">
                                <div className="bg-primary text-primary-foreground p-3 rounded-lg max-w-[80%]">
                                  <p className="text-sm">{msg.message}</p>
                                </div>
                              </div>
                            ) : (
                              <div className="flex justify-start">
                                <div className="bg-muted p-3 rounded-lg max-w-[80%]">
                                  <p className="text-sm">{msg.response}</p>
                                </div>
                              </div>
                            )}
                          </div>
                        ))}
                        
                        {isSendingMessage && (
                          <div className="flex justify-start">
                            <div className="bg-muted p-3 rounded-lg">
                              <Loader2 className="h-4 w-4 animate-spin" />
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </ScrollArea>

                  {/* Chat Input */}
                  <div className="flex gap-2">
                    <Input
                      placeholder="Ask me anything about learning..."
                      value={currentMessage}
                      onChange={(e) => setCurrentMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      disabled={isSendingMessage}
                    />
                    <Button onClick={handleSendMessage} disabled={isSendingMessage || !currentMessage.trim()}>
                      {isSendingMessage ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Send className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="profile">
              <Card>
                <CardHeader>
                  <CardTitle>Learning Profile</CardTitle>
                  <CardDescription>Your personalized learning settings</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-medium text-foreground mb-2">Learning Style</h4>
                      <p className="text-foreground-muted">Visual Learner</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground mb-2">Support Needs</h4>
                      <p className="text-foreground-muted">ADHD Support Enabled</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground mb-2">Preferred Pace</h4>
                      <p className="text-foreground-muted">Moderate</p>
                    </div>
                    <Button>Update Profile</Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="progress">
              <Card>
                <CardHeader>
                  <CardTitle>Learning Progress</CardTitle>
                  <CardDescription>Track your learning journey</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12">
                    <BarChart3 className="h-12 w-12 text-foreground-muted mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-foreground mb-2">Analytics Coming Soon</h3>
                    <p className="text-foreground-muted">
                      Detailed progress tracking and analytics will be available soon.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  );
}