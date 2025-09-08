import { ArrowRight, CheckCircle, Sparkles, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const benefits = [
  "Personalized learning assessment in under 10 minutes",
  "Immediate AI tutor matching based on your profile",
  "Access to neurodivergent-friendly learning tools",
  "24/7 emotional support and crisis detection",
  "Progress tracking with beautiful visualizations",
  "Community support from fellow learners"
];

export default function CTASection() {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-gradient-primary opacity-10 blur-3xl animate-pulse-glow" />
      </div>
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto">
          {/* Main CTA Card */}
          <div className="glass-strong rounded-3xl p-8 md:p-12 text-center border-gradient">
            {/* Header */}
            <div className="flex items-center justify-center mb-6">
              <Sparkles className="h-6 w-6 text-primary mr-2" />
              <span className="text-primary font-semibold">Start Your Journey Today</span>
              <Sparkles className="h-6 w-6 text-primary ml-2" />
            </div>

            <h2 className="heading-2 mb-6">
              Ready to Transform Your
              <br />
              <span className="gradient-text">Learning Experience?</span>
            </h2>

            <p className="body-large text-foreground-muted mb-8 max-w-2xl mx-auto">
              Join thousands of neurodivergent learners who have discovered their unique learning path 
              with AURA's adaptive AI tutoring platform.
            </p>

            {/* Benefits Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 text-left max-w-2xl mx-auto">
              {benefits.map((benefit, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-accent mt-0.5 flex-shrink-0" />
                  <span className="text-foreground-muted text-sm">{benefit}</span>
                </div>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
              <Button variant="hero" size="xl" asChild>
                <Link to="/signup">
                  Start Free Assessment
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Link>
              </Button>
              <Button variant="glass" size="xl" asChild>
                <Link to="/demo">
                  Schedule Demo
                </Link>
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="flex items-center justify-center space-x-6 text-foreground-muted text-sm">
              <div className="flex items-center">
                <Star className="h-4 w-4 text-accent mr-1" />
                <span>4.9/5 Rating</span>
              </div>
              <div className="w-px h-4 bg-glass-border"></div>
              <div>Free Forever Plan</div>
              <div className="w-px h-4 bg-glass-border"></div>
              <div>No Credit Card Required</div>
            </div>
          </div>

          {/* Testimonial Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="glass-card p-6 text-center animate-float" style={{ animationDelay: '0s' }}>
              <div className="flex justify-center mb-3">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 text-accent fill-current" />
                ))}
              </div>
              <p className="text-foreground-muted text-sm mb-4 italic">
                "AURA understood my ADHD learning style immediately. The personalized approach has been life-changing."
              </p>
              <div className="text-sm">
                <div className="font-semibold text-foreground">Sarah M.</div>
                <div className="text-foreground-muted">Frontend Developer</div>
              </div>
            </div>

            <div className="glass-card p-6 text-center animate-float" style={{ animationDelay: '2s' }}>
              <div className="flex justify-center mb-3">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 text-accent fill-current" />
                ))}
              </div>
              <p className="text-foreground-muted text-sm mb-4 italic">
                "The emotional regulation tools helped my daughter develop confidence while learning to code."
              </p>
              <div className="text-sm">
                <div className="font-semibold text-foreground">Michael R.</div>
                <div className="text-foreground-muted">Parent</div>
              </div>
            </div>

            <div className="glass-card p-6 text-center animate-float" style={{ animationDelay: '4s' }}>
              <div className="flex justify-center mb-3">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 text-accent fill-current" />
                ))}
              </div>
              <p className="text-foreground-muted text-sm mb-4 italic">
                "From zero coding knowledge to building my own AI projects in 6 months. AURA made it possible."
              </p>
              <div className="text-sm">
                <div className="font-semibold text-foreground">Alex K.</div>
                <div className="text-foreground-muted">AI Engineer</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}