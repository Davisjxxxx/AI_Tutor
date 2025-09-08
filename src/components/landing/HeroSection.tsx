import { ArrowRight, Sparkles, Brain, Users, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

export default function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-32 h-32 rounded-full bg-primary/10 animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute top-40 right-20 w-24 h-24 rounded-full bg-secondary/10 animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-40 left-20 w-40 h-40 rounded-full bg-accent/10 animate-float" style={{ animationDelay: '4s' }} />
        <div className="absolute bottom-20 right-10 w-28 h-28 rounded-full bg-primary/5 animate-float" style={{ animationDelay: '1s' }} />
      </div>

      <div className="container mx-auto px-4 text-center relative z-10">
        {/* Announcement Badge */}
        <div className="inline-flex items-center px-4 py-2 mb-8 glass-card rounded-full text-sm">
          <Sparkles className="h-4 w-4 mr-2 text-primary" />
          <span className="text-foreground-muted">Introducing AURA AI Tutor - Now in Beta</span>
        </div>

        {/* Main Headline */}
        <h1 className="heading-1 mb-6 max-w-4xl mx-auto">
          <span className="gradient-text">Adaptive AI Tutor</span>
          <br />
          <span className="text-foreground">for Every Mind</span>
        </h1>

        {/* Subheadline */}
        <p className="body-large text-foreground-muted mb-8 max-w-2xl mx-auto">
          Discover your unique learning path with personalized AI tutoring 
          designed for neurodivergent individuals.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
          <Button variant="hero" size="xl" asChild>
            <Link to="/signup">
              Start Your Learning Journey
              <ArrowRight className="h-5 w-5 ml-2" />
            </Link>
          </Button>
          <Button variant="glass" size="xl" asChild>
            <Link to="/demo">
              Watch Demo
            </Link>
          </Button>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="glass-card p-6 group hover:scale-105 transition-transform duration-300">
            <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
              <Brain className="h-6 w-6 text-primary-foreground" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Adaptive Tutoring</h3>
            <p className="text-foreground-muted text-sm">
              AI-powered personalization that adapts to your unique learning style and pace
            </p>
          </div>

          <div className="glass-card p-6 group hover:scale-105 transition-transform duration-300">
            <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
              <Users className="h-6 w-6 text-primary-foreground" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Neurodivergent Support</h3>
            <p className="text-foreground-muted text-sm">
              Specialized tools for ADHD, Autism, Dyslexia, and anxiety-friendly learning
            </p>
          </div>

          <div className="glass-card p-6 group hover:scale-105 transition-transform duration-300">
            <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
              <Zap className="h-6 w-6 text-primary-foreground" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">AI-Powered</h3>
            <p className="text-foreground-muted text-sm">
              Advanced AI models provide real-time support and emotional intelligence
            </p>
          </div>
        </div>

        {/* Trust Indicators */}
        <div className="mt-16 text-center">
          <p className="text-foreground-muted text-sm mb-6">Trusted by learners worldwide</p>
          <div className="flex items-center justify-center space-x-8 opacity-60">
            <div className="text-foreground-muted text-lg font-semibold">10K+ Students</div>
            <div className="w-px h-6 bg-glass-border"></div>
            <div className="text-foreground-muted text-lg font-semibold">95% Success Rate</div>
            <div className="w-px h-6 bg-glass-border"></div>
            <div className="text-foreground-muted text-lg font-semibold">24/7 AI Support</div>
          </div>
        </div>
      </div>
    </section>
  );
}