// API service for connecting to AURA backend
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com/api' // Replace with your production API URL
  : 'http://193.186.4.224:9000/api';

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  learning_profile?: string;
  subscription_status?: string;
}

export interface ChatMessage {
  message: string;
  user_id?: string;
  engine?: string;
}

export interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

export interface Memory {
  id: string;
  content: string;
  response: string;
  timestamp: string;
  similarity?: number;
}

export interface LearningProfile {
  learning_style_primary: string;
  learning_style_secondary?: string;
  has_adhd: boolean;
  has_autism: boolean;
  has_dyslexia: boolean;
  has_anxiety: boolean;
  mbti_type?: string;
  verbal_iq_estimate?: number;
  processing_speed_estimate?: number;
  attention_span_minutes: number;
  stress_triggers: string[];
  motivation_factors: string[];
  communication_preference: string;
  feedback_style: string;
}

export interface AssessmentQuestions {
  learning_style: any[];
  neurodivergent_screening: any[];
  mbti_quick: any[];
  cognitive_assessment: any[];
}

class ApiService {
  private baseUrl = API_BASE_URL;

  // Helper method for making requests
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  // Real Authentication
  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await this.request<{ user: User; token: string; success: boolean; message: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Login failed');
    }
    
    return {
      user: response.user,
      token: response.token
    };
  }

  async signup(name: string, email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await this.request<{ user: User; token: string; success: boolean; message: string }>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Signup failed');
    }
    
    return {
      user: response.user,
      token: response.token
    };
  }

  async getCurrentUser(token: string): Promise<User> {
    const response = await this.request<{ user: User; success: boolean }>('/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.success) {
      throw new Error('Failed to get user info');
    }
    
    return response.user;
  }

  async googleAuth(credential: string): Promise<{ user: User; token: string }> {
    const response = await this.request<{ user: User; token: string; success: boolean; message: string }>('/auth/google', {
      method: 'POST',
      body: JSON.stringify({ credential }),
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Google authentication failed');
    }
    
    return {
      user: response.user,
      token: response.token
    };
  }

  // AI Chat
  async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
    return this.request<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({
        message: message.message,
        user_id: message.user_id || 'default_user',
        engine: message.engine || 'llama',
      }),
    });
  }

  async sendPersonalizedChatMessage(
    message: ChatMessage, 
    profileData?: Partial<LearningProfile>
  ): Promise<ChatResponse> {
    return this.request<ChatResponse>('/chat/personalized', {
      method: 'POST',
      body: JSON.stringify({
        message: message.message,
        user_id: message.user_id || 'default_user',
        engine: message.engine || 'llama',
        profile_data: profileData,
      }),
    });
  }

  // Memory Management
  async getUserMemories(userId?: string, limit = 10): Promise<Memory[]> {
    const params = new URLSearchParams({
      user_id: userId || 'default_user',
      limit: limit.toString(),
    });
    return this.request<Memory[]>(`/memories?${params}`);
  }

  async searchMemories(query: string, limit = 5): Promise<{ query: string; memories: Memory[] }> {
    const params = new URLSearchParams({ query, limit: limit.toString() });
    return this.request(`/memories/search?${params}`);
  }

  // Learning Profile
  async getAssessmentQuestions(): Promise<AssessmentQuestions> {
    return this.request<AssessmentQuestions>('/assessment/questions');
  }

  async createLearningProfile(profile: LearningProfile): Promise<{
    profile: LearningProfile;
    teaching_strategy: any;
    curriculum: any;
    success: boolean;
  }> {
    return this.request('/profile/create', {
      method: 'POST',
      body: JSON.stringify(profile),
    });
  }

  async getTeachingStrategy(userId: string): Promise<{
    user_id: string;
    communication_style: string;
    lesson_structure: any;
    neurodivergent_adaptations: any;
  }> {
    return this.request(`/profile/${userId}/strategy`);
  }

  // Agent routing
  async analyzeMessageRouting(message: string, userId?: string): Promise<any> {
    return this.request('/chat/route-analysis', {
      method: 'POST',
      body: JSON.stringify({
        message,
        user_id: userId || 'default_user',
        engine: 'llama',
      }),
    });
  }

  async getAgentCapabilities(): Promise<any> {
    return this.request('/agents/capabilities');
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await fetch(`${this.baseUrl.replace('/api', '')}/docs`);
      return true;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();
export default apiService;