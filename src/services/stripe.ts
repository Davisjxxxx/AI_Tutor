// Stripe integration for AURA AI Tutor
import { loadStripe, Stripe } from '@stripe/stripe-js';

// Use test key for demo - replace with your publishable key
const STRIPE_PUBLIC_KEY = 'pk_test_51234567890abcdef'; // Replace with your actual key

export interface PricingPlan {
  id: string;
  name: string;
  price: number;
  currency: string;
  interval: 'month' | 'year';
  features: string[];
  stripePriceId: string;
}

export const PRICING_PLANS: PricingPlan[] = [
  {
    id: 'basic',
    name: 'Basic Plan',
    price: 9.99,
    currency: 'usd',
    interval: 'month',
    features: [
      'AI Tutor Access',
      'Basic Learning Assessment',
      '50 Chat Messages/month',
      'Progress Tracking',
      'Email Support'
    ],
    stripePriceId: 'price_basic_monthly', // Replace with actual Stripe price ID
  },
  {
    id: 'pro',
    name: 'Pro Plan',
    price: 19.99,
    currency: 'usd',
    interval: 'month',
    features: [
      'Everything in Basic',
      'Advanced Learning Profile',
      'Unlimited Chat Messages',
      'Personalized Curriculum',
      'Memory Visualization',
      'Priority Support',
      'Learning Analytics'
    ],
    stripePriceId: 'price_pro_monthly', // Replace with actual Stripe price ID
  },
  {
    id: 'premium',
    name: 'Premium Plan',
    price: 39.99,
    currency: 'usd',
    interval: 'month',
    features: [
      'Everything in Pro',
      'Multiple AI Model Access',
      'Custom Learning Paths',
      '1-on-1 Support Sessions',
      'Advanced Analytics',
      'API Access',
      'White-label Options'
    ],
    stripePriceId: 'price_premium_monthly', // Replace with actual Stripe price ID
  },
];

class StripeService {
  private stripe: Promise<Stripe | null>;

  constructor() {
    this.stripe = loadStripe(STRIPE_PUBLIC_KEY);
  }

  async redirectToCheckout(priceId: string, userId?: string): Promise<void> {
    const stripe = await this.stripe;
    if (!stripe) {
      throw new Error('Stripe failed to load');
    }

    // In a real implementation, you would call your backend to create a checkout session
    // For demo purposes, we'll simulate this
    console.log('Demo: Would redirect to Stripe checkout for:', priceId);
    
    // Simulate checkout process
    const mockCheckoutSession = {
      id: 'cs_demo_' + Math.random().toString(36).substr(2, 9),
      url: `https://checkout.stripe.com/demo?session_id=cs_demo_session&price=${priceId}`
    };

    // In real implementation, you would redirect to the actual checkout URL:
    // window.location.href = mockCheckoutSession.url;
    
    // For demo, show success message
    alert(`Demo: Checkout initiated for plan ${priceId}!\n\nIn production, this would redirect to Stripe checkout.`);
  }

  async createCheckoutSession(priceId: string, userId?: string, metadata?: Record<string, string>) {
    // This would call your backend to create a Stripe checkout session
    const response = await fetch('/api/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        priceId,
        userId,
        metadata,
        successUrl: `${window.location.origin}/dashboard?success=true`,
        cancelUrl: `${window.location.origin}/pricing?canceled=true`,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create checkout session');
    }

    const session = await response.json();
    return session;
  }

  async createPortalSession(customerId: string) {
    // This would call your backend to create a Stripe billing portal session
    const response = await fetch('/api/create-portal-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customerId,
        returnUrl: `${window.location.origin}/dashboard`,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to create portal session');
    }

    const session = await response.json();
    return session;
  }

  // Demo function to simulate subscription status
  getMockSubscriptionStatus(userId?: string) {
    // In real app, this would come from your backend/database
    return {
      status: 'active',
      plan: 'basic',
      currentPeriodEnd: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      cancelAtPeriodEnd: false,
    };
  }

  // Format price for display
  formatPrice(price: number, currency = 'usd'): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency.toUpperCase(),
    }).format(price);
  }
}

export const stripeService = new StripeService();
export default stripeService;