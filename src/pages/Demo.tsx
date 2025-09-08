import { ArrowLeft, Play, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

export default function Demo() {
  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-24">
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <div className="mb-8">
            <Button variant="ghost" asChild>
              <Link to="/">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Home
              </Link>
            </Button>
          </div>

          {/* Demo Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center px-4 py-2 mb-6 glass-card rounded-full text-sm">
              <Sparkles className="h-4 w-4 mr-2 text-primary" />
              <span className="text-foreground-muted">Interactive Demo</span>
            </div>
            <h1 className="heading-1 mb-6">
              <span className="gradient-text">Experience AURA</span>
              <br />
              <span className="text-foreground">AI Tutoring</span>
            </h1>
            <p className="body-large text-foreground-muted mb-8 max-w-2xl mx-auto">
              See how AURA adapts to different learning styles and provides personalized support for neurodivergent learners.
            </p>
          </div>

          {/* Demo Video Section */}
          <div className="mb-12">
            <div className="relative glass-card p-8 rounded-2xl">
              <div className="aspect-video bg-gradient-primary rounded-xl flex items-center justify-center">
                <div className="text-center">
                  <div className="p-4 bg-white/20 rounded-full w-fit mx-auto mb-4">
                    <Play className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">Demo Coming Soon</h3>
                  <p className="text-white/80">
                    Interactive demo is being prepared to showcase AURA's adaptive AI tutoring capabilities.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Demo Features */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-3">Adaptive Learning</h3>
              <p className="text-foreground-muted mb-4">
                Watch how AURA adjusts its teaching style based on your responses and learning preferences.
              </p>
              <Button variant="outline" size="sm" disabled>
                Try Interactive Demo
              </Button>
            </div>

            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-3">Neurodivergent Support</h3>
              <p className="text-foreground-muted mb-4">
                Experience specialized tools designed for ADHD, Autism, and other learning differences.
              </p>
              <Button variant="outline" size="sm" disabled>
                Explore Features
              </Button>
            </div>

            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-3">AI Chat Interface</h3>
              <p className="text-foreground-muted mb-4">
                Try conversing with AURA's AI tutor and see how it provides personalized explanations.
              </p>
              <Button variant="outline" size="sm" asChild>
                <Link to="/signup">
                  Start Chatting
                </Link>
              </Button>
            </div>

            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-3">Progress Tracking</h3>
              <p className="text-foreground-muted mb-4">
                See how AURA visualizes your learning journey and tracks your progress over time.
              </p>
              <Button variant="outline" size="sm" asChild>
                <Link to="/signup">
                  View Dashboard
                </Link>
              </Button>
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center glass-card p-8 rounded-2xl">
            <h2 className="text-2xl font-bold text-foreground mb-4">Ready to Start Learning?</h2>
            <p className="text-foreground-muted mb-6">
              Join thousands of neurodivergent learners who are discovering their potential with AURA.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="hero" size="lg" asChild>
                <Link to="/signup">
                  Start Free Trial
                </Link>
              </Button>
              <Button variant="glass" size="lg" asChild>
                <Link to="/login">
                  Sign In
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}