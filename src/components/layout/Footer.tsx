import { Brain, Mail, Github, Twitter, Linkedin, Heart } from "lucide-react";
import { Link } from "react-router-dom";

const footerLinks = {
  product: [
    { name: "Features", href: "/features" },
    { name: "Pricing", href: "/pricing" },
    { name: "Demo", href: "/demo" },
    { name: "API", href: "/api" }
  ],
  resources: [
    { name: "Documentation", href: "/docs" },
    { name: "Blog", href: "/blog" },
    { name: "Community", href: "/community" },
    { name: "Support", href: "/support" }
  ],
  company: [
    { name: "About", href: "/about" },
    { name: "Careers", href: "/careers" },
    { name: "Privacy", href: "/privacy" },
    { name: "Terms", href: "/terms" }
  ],
  accessibility: [
    { name: "ADHD Support", href: "/adhd" },
    { name: "Autism Resources", href: "/autism" },
    { name: "Dyslexia Tools", href: "/dyslexia" },
    { name: "Anxiety Help", href: "/anxiety" }
  ]
};

export default function Footer() {
  return (
    <footer className="relative border-t border-glass-border">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-background-secondary/50 to-transparent" />
      
      <div className="container mx-auto px-4 py-16 relative z-10">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <div className="p-2 rounded-xl bg-gradient-primary">
                <Brain className="h-6 w-6 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold gradient-text">AURA</span>
            </Link>
            <p className="text-foreground-muted text-sm mb-6 max-w-sm">
              Adaptive AI tutoring designed for neurodivergent learners. 
              Empowering every mind to discover their unique learning path through 
              personalized, supportive tutoring experiences.
            </p>
            <div className="flex space-x-4">
              <a 
                href="https://twitter.com/aura-ai" 
                className="p-2 glass rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors duration-200"
                aria-label="Twitter"
              >
                <Twitter className="h-4 w-4" />
              </a>
              <a 
                href="https://github.com/aura-ai" 
                className="p-2 glass rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors duration-200"
                aria-label="GitHub"
              >
                <Github className="h-4 w-4" />
              </a>
              <a 
                href="https://linkedin.com/company/aura-ai" 
                className="p-2 glass rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors duration-200"
                aria-label="LinkedIn"
              >
                <Linkedin className="h-4 w-4" />
              </a>
              <a 
                href="mailto:hello@aura-ai.com" 
                className="p-2 glass rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors duration-200"
                aria-label="Email"
              >
                <Mail className="h-4 w-4" />
              </a>
            </div>
          </div>

          {/* Links Sections */}
          <div>
            <h3 className="font-semibold text-foreground mb-4">Product</h3>
            <ul className="space-y-3">
              {footerLinks.product.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-foreground-muted hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-foreground mb-4">Resources</h3>
            <ul className="space-y-3">
              {footerLinks.resources.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-foreground-muted hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-foreground mb-4">Company</h3>
            <ul className="space-y-3">
              {footerLinks.company.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-foreground-muted hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-foreground mb-4">Accessibility</h3>
            <ul className="space-y-3">
              {footerLinks.accessibility.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href}
                    className="text-foreground-muted hover:text-primary transition-colors duration-200 text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter Signup */}
        <div className="glass-card p-6 rounded-2xl mb-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="mb-4 md:mb-0">
              <h3 className="font-semibold text-foreground mb-2">Stay Updated</h3>
              <p className="text-foreground-muted text-sm">
                Get the latest neurodivergent-friendly learning tips and AI education insights.
              </p>
            </div>
            <div className="flex space-x-3 w-full md:w-auto">
              <input 
                type="email" 
                placeholder="Enter your email"
                className="flex-1 md:w-64 px-4 py-2 glass-strong rounded-lg border border-glass-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 text-foreground placeholder-foreground-muted"
              />
              <button className="px-6 py-2 bg-gradient-primary text-primary-foreground rounded-lg hover:scale-105 transition-transform duration-200 whitespace-nowrap">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-glass-border">
          <div className="text-foreground-muted text-sm mb-4 md:mb-0">
            © 2024 AURA AI Tutor. All rights reserved.
          </div>
          <div className="flex items-center text-foreground-muted text-sm">
            <span>Made with</span>
            <Heart className="h-4 w-4 mx-1 text-accent" />
            <span>for neurodivergent learners</span>
          </div>
        </div>
      </div>
    </footer>
  );
}