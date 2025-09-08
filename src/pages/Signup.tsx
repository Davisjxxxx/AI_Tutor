import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Mail, Lock, User, Brain, ArrowLeft, CheckCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";

const benefits = [
  "Personalized learning assessment",
  "AI tutor matching",
  "Neurodivergent-friendly tools",
  "24/7 emotional support",
  "Progress visualization",
  "Community access"
];

export default function Signup() {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });
  const navigate = useNavigate();
  const { signup, isLoading } = useAuth();
  const { toast } = useToast();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.name || !formData.email || !formData.password) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }
    
    if (formData.password.length < 6) {
      toast({
        title: "Error",
        description: "Password must be at least 6 characters",
        variant: "destructive",
      });
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Error",
        description: "Passwords do not match",
        variant: "destructive",
      });
      return;
    }

    try {
      await signup(formData.name, formData.email, formData.password);
      toast({
        title: "Success",
        description: "Account created successfully!",
      });
      navigate("/dashboard");
    } catch (error) {
      toast({
        title: "Signup Failed",
        description: error instanceof Error ? error.message : "Failed to create account",
        variant: "destructive",
      });
    }
  };

  const handleSocialLogin = async (provider: string) => {
    try {
      // For demo purposes, simulate social signup with a demo account
      await signup(`Demo User`, `demo@${provider.toLowerCase()}.com`, "demo123");
      toast({
        title: "Success",
        description: `Account created with ${provider}!`,
      });
      navigate("/dashboard");
    } catch (error) {
      toast({
        title: "Signup Failed",
        description: `${provider} signup failed`,
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 right-20 w-40 h-40 rounded-full bg-primary/10 animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute bottom-20 left-20 w-32 h-32 rounded-full bg-secondary/10 animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 right-10 w-24 h-24 rounded-full bg-accent/10 animate-float" style={{ animationDelay: '4s' }} />
      </div>

      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">
        {/* Left Side - Benefits */}
        <div className="hidden lg:flex flex-col justify-center">
          <div className="mb-8">
            <Link 
              to="/" 
              className="inline-flex items-center text-foreground-muted hover:text-primary transition-colors duration-200 mb-6"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
            
            <h2 className="heading-2 mb-4">
              Start Your
              <br />
              <span className="gradient-text">Learning Journey</span>
            </h2>
            <p className="body-large text-foreground-muted mb-8">
              Join thousands of neurodivergent learners discovering their potential with AURA's adaptive AI education.
            </p>
          </div>

          <div className="space-y-4">
            {benefits.map((benefit, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="p-1 bg-gradient-primary rounded-full">
                  <CheckCircle className="h-4 w-4 text-primary-foreground" />
                </div>
                <span className="text-foreground">{benefit}</span>
              </div>
            ))}
          </div>

          <div className="mt-8 glass-card p-6 rounded-2xl">
            <blockquote className="text-foreground-muted italic mb-4">
              "AURA's personalized approach helped me understand my learning style and achieve goals I never thought possible."
            </blockquote>
            <cite className="text-foreground font-medium">— Sarah M., Frontend Developer</cite>
          </div>
        </div>

        {/* Right Side - Signup Form */}
        <div className="flex flex-col justify-center">
          <div className="lg:hidden mb-6">
            <Link 
              to="/" 
              className="inline-flex items-center text-foreground-muted hover:text-primary transition-colors duration-200 mb-4"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
          </div>

          <div className="glass-strong rounded-3xl p-8 border border-glass-border shadow-strong">
            {/* Header */}
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-gradient-primary rounded-2xl">
                  <Brain className="h-8 w-8 text-primary-foreground" />
                </div>
              </div>
              <h1 className="heading-3 mb-2">Create Your AURA Account</h1>
              <p className="text-foreground-muted">Get started with personalized AI learning</p>
            </div>

            {/* Signup Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name Field */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-foreground-muted" />
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 glass-strong rounded-xl border border-glass-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 text-foreground placeholder-foreground-muted transition-all duration-200"
                    placeholder="Enter your full name"
                    required
                  />
                </div>
              </div>

              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-foreground-muted" />
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 glass-strong rounded-xl border border-glass-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 text-foreground placeholder-foreground-muted transition-all duration-200"
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-foreground-muted" />
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full pl-10 pr-12 py-3 glass-strong rounded-xl border border-glass-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 text-foreground placeholder-foreground-muted transition-all duration-200"
                    placeholder="Create a password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-foreground-muted hover:text-foreground transition-colors duration-200"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password Field */}
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-foreground-muted" />
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showPassword ? "text" : "password"}
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 glass-strong rounded-xl border border-glass-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 text-foreground placeholder-foreground-muted transition-all duration-200"
                    placeholder="Confirm your password"
                    required
                  />
                </div>
              </div>

              {/* Terms Checkbox */}
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  id="terms"
                  className="w-4 h-4 mt-1 text-primary bg-glass-strong border-glass-border rounded focus:ring-primary focus:ring-2"
                  required
                />
                <label htmlFor="terms" className="text-sm text-foreground-muted">
                  I agree to the{" "}
                  <Link to="/terms" className="text-primary hover:text-primary-glow transition-colors">
                    Terms of Service
                  </Link>{" "}
                  and{" "}
                  <Link to="/privacy" className="text-primary hover:text-primary-glow transition-colors">
                    Privacy Policy
                  </Link>
                </label>
              </div>

              {/* Signup Button */}
              <Button type="submit" variant="hero" size="lg" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Creating Account...
                  </>
                ) : (
                  "Create Account"
                )}
              </Button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center">
              <div className="flex-1 border-t border-glass-border"></div>
              <div className="px-4 text-foreground-muted text-sm">or</div>
              <div className="flex-1 border-t border-glass-border"></div>
            </div>

            {/* Social Signup */}
            <div className="space-y-3">
              <Button 
                variant="glass" 
                size="lg" 
                className="w-full"
                onClick={() => handleSocialLogin('Google')}
                type="button"
              >
                <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </Button>
              <Button 
                variant="glass" 
                size="lg" 
                className="w-full"
                onClick={() => handleSocialLogin('Facebook')}
                type="button"
              >
                <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                Continue with Facebook
              </Button>
            </div>

            {/* Login Link */}
            <div className="text-center mt-6">
              <span className="text-foreground-muted text-sm">Already have an account? </span>
              <Link 
                to="/login" 
                className="text-primary hover:text-primary-glow transition-colors duration-200 font-medium"
              >
                Sign in
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}