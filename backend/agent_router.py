"""
Agent Router - MCP-style intelligent handoff system for specialized AI responses
"""

import json
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel

class AgentType(Enum):
    CODING_TUTOR = "coding_tutor"
    NEURODIVERGENT_SUPPORT = "neurodivergent_support"
    GENERAL_TUTOR = "general_tutor"
    MOTIVATION_COACH = "motivation_coach"
    ASSESSMENT_SPECIALIST = "assessment_specialist"
    LEARNING_STRATEGIST = "learning_strategist"

@dataclass
class AgentCapability:
    name: str
    description: str
    keywords: List[str]
    priority: int = 1

class AgentRouter:
    """
    Intelligent agent routing system that determines which specialized AI agent
    should handle a given query based on content analysis, user context, and capabilities.
    """
    
    def __init__(self):
        self.agents = self._initialize_agents()
        
    def _initialize_agents(self) -> Dict[AgentType, Dict[str, Any]]:
        return {
            AgentType.CODING_TUTOR: {
                "capabilities": [
                    AgentCapability("Frontend Development", "HTML, CSS, JavaScript, React, Vue", 
                                  ["html", "css", "javascript", "react", "vue", "frontend", "web", "code", "programming", "syntax", "function", "variable", "component"]),
                    AgentCapability("Backend Development", "Python, Node.js, APIs, databases",
                                  ["python", "node", "api", "database", "backend", "server", "django", "flask", "fastapi"]),
                    AgentCapability("Mobile Development", "React Native, Flutter, Capacitor",
                                  ["mobile", "app", "react native", "flutter", "capacitor", "android", "ios"]),
                    AgentCapability("DevOps & Tools", "Git, deployment, CI/CD",
                                  ["git", "deploy", "docker", "aws", "devops", "build", "test"])
                ],
                "system_prompt": """You are a specialized coding tutor with expertise in web development, 
                mobile apps, and software engineering. You provide clear, practical coding examples, 
                debug issues, explain concepts step-by-step, and adapt to different skill levels. 
                Always include working code examples and best practices."""
            },
            
            AgentType.NEURODIVERGENT_SUPPORT: {
                "capabilities": [
                    AgentCapability("ADHD Support", "Focus, attention, hyperactivity management",
                                  ["adhd", "focus", "attention", "hyperactive", "distracted", "concentrate", "procrastination"]),
                    AgentCapability("Autism Support", "Social communication, sensory processing",
                                  ["autism", "autistic", "sensory", "communication", "social", "routine", "stimming"]),
                    AgentCapability("Dyslexia Support", "Reading, writing, processing differences",
                                  ["dyslexia", "reading", "writing", "processing", "letters", "words", "spelling"]),
                    AgentCapability("Anxiety Management", "Learning anxiety, performance pressure",
                                  ["anxiety", "anxious", "stress", "worried", "nervous", "overwhelmed", "panic"])
                ],
                "system_prompt": """You are a specialized neurodivergent support specialist with deep 
                understanding of ADHD, autism, dyslexia, and anxiety. You provide accommodations, 
                coping strategies, and personalized learning approaches. You communicate with empathy, 
                validate experiences, and offer practical tools for success."""
            },
            
            AgentType.MOTIVATION_COACH: {
                "capabilities": [
                    AgentCapability("Emotional Support", "Encouragement, confidence building",
                                  ["discouraged", "frustrated", "stuck", "difficult", "hard", "give up", "motivation", "confidence"]),
                    AgentCapability("Goal Setting", "Breaking down tasks, progress tracking",
                                  ["goal", "objective", "plan", "progress", "achieve", "accomplish", "milestone"]),
                    AgentCapability("Overcoming Blocks", "Mental barriers, imposter syndrome",
                                  ["block", "barrier", "imposter", "doubt", "fear", "failure", "perfectionism"])
                ],
                "system_prompt": """You are a motivational learning coach who provides emotional support, 
                encouragement, and practical strategies for overcoming learning challenges. You help 
                build confidence, set achievable goals, and maintain momentum. Your tone is warm, 
                understanding, and empowering."""
            },
            
            AgentType.ASSESSMENT_SPECIALIST: {
                "capabilities": [
                    AgentCapability("Learning Style Assessment", "Visual, auditory, kinesthetic preferences",
                                  ["learning style", "visual", "auditory", "kinesthetic", "assessment", "test", "evaluate"]),
                    AgentCapability("Skill Gap Analysis", "Identifying knowledge gaps",
                                  ["skill gap", "knowledge", "level", "beginner", "intermediate", "advanced", "evaluate"])
                ],
                "system_prompt": """You are an assessment specialist who evaluates learning needs, 
                identifies skill gaps, and recommends personalized learning paths. You create 
                comprehensive assessments and provide detailed analysis of learning preferences 
                and capabilities."""
            },
            
            AgentType.LEARNING_STRATEGIST: {
                "capabilities": [
                    AgentCapability("Curriculum Design", "Structured learning paths",
                                  ["curriculum", "course", "lesson", "module", "structure", "path", "roadmap"]),
                    AgentCapability("Study Methods", "Effective learning techniques",
                                  ["study", "method", "technique", "practice", "review", "memorize", "retain"])
                ],
                "system_prompt": """You are a learning strategist who designs effective curriculum, 
                creates structured learning paths, and recommends proven study methods. You focus 
                on pedagogy, learning science, and adaptive instruction techniques."""
            },
            
            AgentType.GENERAL_TUTOR: {
                "capabilities": [
                    AgentCapability("General Questions", "Basic questions and explanations",
                                  ["what", "how", "why", "explain", "help", "question", "understand"])
                ],
                "system_prompt": """You are a general AI tutor who provides helpful explanations, 
                answers questions, and guides learning across various topics. You adapt your 
                communication style to the user's needs and provide clear, comprehensive responses."""
            }
        }
    
    def analyze_message(self, message: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze a message to determine intent, complexity, and emotional state
        """
        message_lower = message.lower()
        
        # Detect emotional indicators
        frustration_words = ["frustrated", "stuck", "difficult", "hard", "give up", "can't", "impossible"]
        anxiety_words = ["worried", "nervous", "anxious", "scared", "overwhelmed"]
        motivation_words = ["motivation", "encourage", "confidence", "believe"]
        
        emotion_score = {
            "frustration": sum(1 for word in frustration_words if word in message_lower),
            "anxiety": sum(1 for word in anxiety_words if word in message_lower),
            "needs_motivation": sum(1 for word in motivation_words if word in message_lower)
        }
        
        # Detect technical complexity
        technical_indicators = ["error", "debug", "code", "function", "variable", "syntax", "implement"]
        technical_score = sum(1 for indicator in technical_indicators if indicator in message_lower)
        
        # Detect learning focus
        learning_indicators = ["learn", "understand", "explain", "how to", "what is", "why does"]
        learning_score = sum(1 for indicator in learning_indicators if indicator in message_lower)
        
        return {
            "emotions": emotion_score,
            "technical_complexity": technical_score,
            "learning_focus": learning_score,
            "message_length": len(message.split()),
            "question_markers": message.count("?")
        }
    
    def route_message(self, message: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Route a message to the most appropriate agent based on content analysis
        """
        analysis = self.analyze_message(message, user_context)
        message_lower = message.lower()
        
        # Calculate agent scores
        agent_scores = {}
        
        for agent_type, agent_data in self.agents.items():
            score = 0
            matched_capabilities = []
            
            # Check capability keywords
            for capability in agent_data["capabilities"]:
                keyword_matches = sum(1 for keyword in capability.keywords if keyword in message_lower)
                if keyword_matches > 0:
                    score += keyword_matches * capability.priority
                    matched_capabilities.append(capability.name)
            
            agent_scores[agent_type] = {
                "score": score,
                "matched_capabilities": matched_capabilities
            }
        
        # Special routing logic
        
        # High emotional distress -> Motivation Coach or Neurodivergent Support
        if analysis["emotions"]["frustration"] > 2 or analysis["emotions"]["anxiety"] > 1:
            if any(keyword in message_lower for keyword in ["adhd", "autism", "dyslexia", "neurodivergent"]):
                agent_scores[AgentType.NEURODIVERGENT_SUPPORT]["score"] += 10
            else:
                agent_scores[AgentType.MOTIVATION_COACH]["score"] += 8
        
        # High technical content -> Coding Tutor
        if analysis["technical_complexity"] > 2:
            agent_scores[AgentType.CODING_TUTOR]["score"] += 5
        
        # Assessment keywords -> Assessment Specialist
        assessment_keywords = ["assess", "evaluate", "test", "level", "skill", "gap"]
        if any(keyword in message_lower for keyword in assessment_keywords):
            agent_scores[AgentType.ASSESSMENT_SPECIALIST]["score"] += 7
        
        # Find best agent
        best_agent = max(agent_scores.items(), key=lambda x: x[1]["score"])
        
        # Fallback to general tutor if no strong match
        if best_agent[1]["score"] == 0:
            best_agent = (AgentType.GENERAL_TUTOR, agent_scores[AgentType.GENERAL_TUTOR])
        
        return {
            "selected_agent": best_agent[0],
            "confidence": min(best_agent[1]["score"] / 10, 1.0),
            "matched_capabilities": best_agent[1]["matched_capabilities"],
            "all_scores": {agent.value: score["score"] for agent, score in agent_scores.items()},
            "analysis": analysis,
            "system_prompt": self.agents[best_agent[0]]["system_prompt"]
        }
    
    def get_enhanced_prompt(self, message: str, user_context: Optional[Dict] = None) -> str:
        """
        Get an enhanced prompt with agent-specific context and user personalization
        """
        routing_result = self.route_message(message, user_context)
        agent_prompt = routing_result["system_prompt"]
        
        # Add user context if available
        context_addition = ""
        if user_context:
            context_addition = f"\n\nUSER CONTEXT:\n"
            if user_context.get("learning_profile"):
                profile = user_context["learning_profile"]
                context_addition += f"- Learning Style: {profile.get('learning_style_primary', 'unknown')}\n"
                context_addition += f"- Neurodivergent Traits: {', '.join(profile.get('neurodivergent_factors', []))}\n"
                context_addition += f"- Communication Preference: {profile.get('communication_preference', 'supportive')}\n"
            
            if user_context.get("session_history"):
                context_addition += f"- Recent Topics: {', '.join(user_context['session_history'][-3:])}\n"
        
        # Add routing context
        routing_info = f"\n\nROUTING INFO:\n"
        routing_info += f"- Selected Agent: {routing_result['selected_agent'].value}\n"
        routing_info += f"- Confidence: {routing_result['confidence']:.2f}\n"
        routing_info += f"- Matched Capabilities: {', '.join(routing_result['matched_capabilities'])}\n"
        
        return f"{agent_prompt}{context_addition}{routing_info}\n\nUSER MESSAGE: {message}"

# Global router instance
agent_router = AgentRouter()