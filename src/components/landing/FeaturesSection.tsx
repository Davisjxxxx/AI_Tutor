import { 
  Brain, 
  Heart, 
  Code, 
  Zap, 
  Target, 
  Users, 
  BookOpen, 
  LineChart,
  Shield,
  Mic,
  Eye,
  Headphones
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Comprehensive Learning Profiles",
    description: "Multi-dimensional assessment including MBTI, IQ components, learning styles, and neurodivergent screening for truly personalized tutoring.",
    color: "from-primary to-primary-glow"
  },
  {
    icon: Heart,
    title: "Emotional Regulation Support",
    description: "Age-appropriate coping strategies, mindfulness techniques, and emotional intelligence development tailored to your needs.",
    color: "from-secondary to-accent"
  },
  {
    icon: Code,
    title: "Frontend Development Mastery",
    description: "Zero-to-hero web development journey from HTML/CSS basics to advanced React and full-stack development.",
    color: "from-accent to-primary"
  },
  {
    icon: Zap,
    title: "AI/ML Education Track",
    description: "Progressive complexity from basic AI concepts to advanced machine learning implementation and real-world applications.",
    color: "from-primary to-secondary"
  },
  {
    icon: Target,
    title: "Adaptive AI Teaching",
    description: "Multi-model intelligence with real-time adaptation based on your response patterns and emotional state.",
    color: "from-secondary to-primary"
  },
  {
    icon: Users,
    title: "Neurodivergent Adaptations",
    description: "Specialized support for ADHD, Autism, Dyslexia, and anxiety with personalized accommodations and strategies.",
    color: "from-accent to-secondary"
  },
  {
    icon: BookOpen,
    title: "Memory & Progress System",
    description: "ChromaDB vector memory for semantic storage and retrieval of all learning interactions with visual progress tracking.",
    color: "from-primary-glow to-accent"
  },
  {
    icon: LineChart,
    title: "Learning Journey Visualization",
    description: "Interactive progress tracking with memory network graphs and gamified achievement system.",
    color: "from-secondary to-primary-glow"
  }
];

const accessibilityFeatures = [
  {
    icon: Eye,
    title: "Visual Accessibility",
    description: "High contrast modes, adjustable text sizes, and reduced motion options for comfortable learning."
  },
  {
    icon: Headphones,
    title: "Audio Support",
    description: "Voice message support, text-to-speech, and audio descriptions for comprehensive accessibility."
  },
  {
    icon: Shield,
    title: "Safe Learning Environment",
    description: "Crisis detection, stress pattern identification, and immediate coping strategy deployment."
  },
  {
    icon: Mic,
    title: "Voice Interaction",
    description: "Hands-free learning with voice commands and verbal response capabilities for diverse interaction styles."
  }
];

export default function FeaturesSection() {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-secondary/5 blur-3xl" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="heading-2 mb-6">
            <span className="gradient-text">Powerful Features</span>
            <br />
            <span className="text-foreground">for Every Learning Style</span>
          </h2>
          <p className="body-large text-foreground-muted max-w-3xl mx-auto">
            AURA combines cutting-edge AI technology with deep understanding of neurodivergent learning needs 
            to create the most adaptive and supportive tutoring experience possible.
          </p>
        </div>

        {/* Main Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-20">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="glass-card p-6 group hover:scale-105 transition-all duration-300 hover:shadow-glow"
            >
              <div className={`p-3 bg-gradient-to-br ${feature.color} rounded-xl w-fit mb-4`}>
                <feature.icon className="h-6 w-6 text-primary-foreground" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-3 group-hover:text-primary transition-colors">
                {feature.title}
              </h3>
              <p className="text-foreground-muted text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Accessibility Features */}
        <div className="glass-card p-8 rounded-3xl">
          <div className="text-center mb-12">
            <h3 className="heading-3 mb-4">
              <span className="gradient-text">Accessibility First</span>
            </h3>
            <p className="body-medium text-foreground-muted max-w-2xl mx-auto">
              Designed with neurodivergent learners at the center, ensuring everyone can learn comfortably and effectively.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {accessibilityFeatures.map((feature, index) => (
              <div 
                key={index}
                className="text-center group"
              >
                <div className="p-4 bg-gradient-primary rounded-2xl w-fit mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                  <feature.icon className="h-8 w-8 text-primary-foreground" />
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                  {feature.title}
                </h4>
                <p className="text-foreground-muted text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text mb-2">98%</div>
            <div className="text-foreground-muted text-sm">User Satisfaction</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text mb-2">10K+</div>
            <div className="text-foreground-muted text-sm">Active Learners</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text mb-2">50+</div>
            <div className="text-foreground-muted text-sm">Learning Paths</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text mb-2">24/7</div>
            <div className="text-foreground-muted text-sm">AI Support</div>
          </div>
        </div>
      </div>
    </section>
  );
}