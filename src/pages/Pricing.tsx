import { useState } from "react";
import { Check, ArrowLeft, Crown, Zap, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { PRICING_PLANS, stripeService } from "@/services/stripe";
import { useToast } from "@/hooks/use-toast";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

const planIcons = {
  basic: Zap,
  pro: Star,
  premium: Crown,
};

export default function Pricing() {
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const { user } = useAuth();
  const { toast } = useToast();

  const handleSubscribe = async (plan: typeof PRICING_PLANS[0]) => {
    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please sign in to subscribe to a plan",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(plan.id);
    try {
      await stripeService.redirectToCheckout(plan.stripePriceId, user.id);
    } catch (error) {
      toast({
        title: "Checkout Failed",
        description: error instanceof Error ? error.message : "Failed to start checkout",
        variant: "destructive",
      });
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-24">
        <div className="max-w-6xl mx-auto">
          {/* Back Button */}
          <div className="mb-8">
            <Button variant="ghost" asChild>
              <Link to="/dashboard">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </Link>
            </Button>
          </div>

          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="heading-1 mb-6">
              <span className="gradient-text">Choose Your Plan</span>
            </h1>
            <p className="body-large text-foreground-muted mb-8 max-w-2xl mx-auto">
              Unlock the full potential of personalized AI tutoring designed for neurodivergent learners.
            </p>
            <div className="inline-flex items-center px-4 py-2 glass-card rounded-full text-sm">
              <Star className="h-4 w-4 mr-2 text-primary" />
              <span className="text-foreground-muted">7-day free trial • Cancel anytime</span>
            </div>
          </div>

          {/* Pricing Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {PRICING_PLANS.map((plan, index) => {
              const Icon = planIcons[plan.id as keyof typeof planIcons];
              const isPopular = plan.id === 'pro';
              
              return (
                <Card key={plan.id} className={`relative ${isPopular ? 'ring-2 ring-primary' : ''}`}>
                  {isPopular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <Badge className="bg-gradient-primary text-primary-foreground">
                        Most Popular
                      </Badge>
                    </div>
                  )}
                  
                  <CardHeader className="text-center pb-8">
                    <div className="mx-auto p-3 bg-gradient-primary rounded-xl w-fit mb-4">
                      <Icon className="h-6 w-6 text-primary-foreground" />
                    </div>
                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                    <CardDescription>
                      <div className="text-3xl font-bold text-foreground mt-2">
                        {stripeService.formatPrice(plan.price)}
                        <span className="text-base font-normal text-foreground-muted">/{plan.interval}</span>
                      </div>
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent className="space-y-6">
                    <ul className="space-y-3">
                      {plan.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-3">
                          <Check className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                          <span className="text-foreground-muted text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    
                    <Button 
                      variant={isPopular ? "hero" : "outline"} 
                      size="lg" 
                      className="w-full"
                      onClick={() => handleSubscribe(plan)}
                      disabled={isLoading === plan.id}
                    >
                      {isLoading === plan.id ? (
                        "Processing..."
                      ) : (
                        `Start ${plan.name}`
                      )}
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Features Comparison */}
          <div className="glass-card p-8 rounded-2xl">
            <h2 className="text-2xl font-bold text-center text-foreground mb-8">
              Why Choose Nova AI Tutor?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
                  <Zap className="h-6 w-6 text-primary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Neurodivergent-First Design</h3>
                <p className="text-sm text-foreground-muted">
                  Built specifically for ADHD, Autism, Dyslexia, and other learning differences
                </p>
              </div>
              
              <div className="text-center">
                <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
                  <Star className="h-6 w-6 text-primary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Adaptive AI Technology</h3>
                <p className="text-sm text-foreground-muted">
                  AI that learns your unique style and adapts in real-time
                </p>
              </div>
              
              <div className="text-center">
                <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
                  <Crown className="h-6 w-6 text-primary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Comprehensive Assessment</h3>
                <p className="text-sm text-foreground-muted">
                  MBTI, IQ components, learning styles, and neurodivergent screening
                </p>
              </div>
              
              <div className="text-center">
                <div className="p-3 bg-gradient-primary rounded-xl w-fit mx-auto mb-4">
                  <Check className="h-6 w-6 text-primary-foreground" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Evidence-Based Methods</h3>
                <p className="text-sm text-foreground-muted">
                  Research-backed teaching strategies for neurodivergent success
                </p>
              </div>
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mt-16 text-center">
            <h2 className="text-2xl font-bold text-foreground mb-4">Frequently Asked Questions</h2>
            <div className="max-w-2xl mx-auto space-y-4 text-left">
              <div className="glass-card p-6 rounded-lg">
                <h3 className="font-semibold text-foreground mb-2">Can I cancel anytime?</h3>
                <p className="text-foreground-muted text-sm">
                  Yes! You can cancel your subscription at any time. You'll continue to have access until the end of your current billing period.
                </p>
              </div>
              
              <div className="glass-card p-6 rounded-lg">
                <h3 className="font-semibold text-foreground mb-2">Is my learning data secure?</h3>
                <p className="text-foreground-muted text-sm">
                  Absolutely. We use industry-standard encryption and never share your personal learning data with third parties.
                </p>
              </div>
              
              <div className="glass-card p-6 rounded-lg">
                <h3 className="font-semibold text-foreground mb-2">What makes this different from other AI tutors?</h3>
                <p className="text-foreground-muted text-sm">
                  Nova AI is the first AI tutor designed specifically for neurodivergent learners, with specialized assessments and teaching methods.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}