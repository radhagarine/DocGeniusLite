import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a2817] to-[#164430] text-[#f4f9f7]">
      {/* Navigation */}
      <header className="container mx-auto py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-3xl font-bold bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text">D</span>
            <span className="text-2xl font-bold ml-[-3px] text-[#f4f9f7]">oc</span>
            <span className="text-3xl font-bold bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text">G</span>
            <span className="text-2xl font-bold ml-[-3px] text-[#f4f9f7]">enius</span>
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <a href="#features" className="text-[#f4f9f7] hover:text-[#3fd7a5] transition-colors">Features</a>
            <a href="#pricing" className="text-[#f4f9f7] hover:text-[#3fd7a5] transition-colors">Pricing</a>
            <a href="#testimonials" className="text-[#f4f9f7] hover:text-[#3fd7a5] transition-colors">Testimonials</a>
            <a href="/login" className="text-[#f4f9f7] hover:text-[#3fd7a5] transition-colors">Login</a>
            <Button className="bg-gradient-to-r from-[#3fd7a5] to-[#26856c] hover:opacity-90 transition-opacity">
              Get Started
            </Button>
          </div>
          <Button variant="ghost" className="md:hidden text-[#f4f9f7]">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </Button>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto py-20 px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
              Protect your data with{" "}
              <span className="bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text">
                next-generation AI
              </span>
            </h1>
            <p className="text-xl mb-8 text-[rgba(244,249,247,0.7)]">
              Our AI-powered document system creates and validates business documents in real time, ensuring perfect legal compliance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="bg-gradient-to-r from-[#3fd7a5] to-[#26856c] hover:opacity-90 transition-opacity text-white px-8 py-6 text-lg">
                Get Started
              </Button>
              <Button variant="outline" className="border-[#3fd7a5] text-[#3fd7a5] hover:bg-[rgba(63,215,165,0.1)] px-8 py-6 text-lg">
                Learn More
              </Button>
            </div>
          </div>
          <div className="relative">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#3fd7a5] to-[#26856c] rounded-lg blur opacity-30"></div>
            <div className="relative bg-[#0a2817] p-6 rounded-lg border border-[rgba(63,215,165,0.2)]">
              <img 
                src="/dashboard-preview.png" 
                alt="DocGenius Dashboard" 
                className="rounded-lg shadow-2xl"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "https://placehold.co/600x400/164430/f4f9f7?text=DocGenius+Dashboard";
                }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto py-20 px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Powerful Features</h2>
          <p className="text-xl text-[rgba(244,249,247,0.7)] max-w-3xl mx-auto">
            DocGenius combines cutting-edge AI with intuitive design to revolutionize your document workflow
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[
            {
              icon: "🔍",
              title: "Intelligent threat detection",
              description: "AI analyzes and detects security threats in real-time, ensuring maximum protection."
            },
            {
              icon: "🛡️",
              title: "Personalized protection",
              description: "Customized security measures tailored to your specific needs and requirements."
            },
            {
              icon: "⚡",
              title: "Real-time response",
              description: "Instant threat mitigation and protection against potential security breaches."
            },
            {
              icon: "📝",
              title: "Smart document generation",
              description: "Create professional documents with AI assistance in minutes instead of hours."
            },
            {
              icon: "🔒",
              title: "Secure storage",
              description: "End-to-end encryption ensures your sensitive documents remain private and secure."
            },
            {
              icon: "🔄",
              title: "Seamless integration",
              description: "Works with your existing tools and workflows for a frictionless experience."
            }
          ].map((feature, index) => (
            <Card key={index} className="bg-[rgba(22,68,48,0.3)] border-[rgba(63,215,165,0.2)] shadow-lg hover:translate-y-[-5px] transition-transform">
              <CardHeader>
                <div className="text-4xl mb-4">{feature.icon}</div>
                <CardTitle className="text-xl font-bold">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-[rgba(244,249,247,0.7)]">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="container mx-auto py-20 px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">How DocGenius Works</h2>
          <p className="text-xl text-[rgba(244,249,247,0.7)] max-w-3xl mx-auto">
            Our streamlined process makes document creation and management effortless
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: "01",
              title: "Select a template",
              description: "Choose from our library of professionally designed document templates."
            },
            {
              step: "02",
              title: "Customize content",
              description: "Our AI helps you fill in the details with smart suggestions and validation."
            },
            {
              step: "03",
              title: "Generate & share",
              description: "Create your finalized document and securely share it with stakeholders."
            }
          ].map((step, index) => (
            <div key={index} className="relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-[#3fd7a5] to-[#26856c] rounded-lg blur opacity-20"></div>
              <div className="relative bg-[rgba(10,40,23,0.3)] p-8 rounded-lg border border-[rgba(63,215,165,0.2)]">
                <div className="text-5xl font-bold bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text mb-4">
                  {step.step}
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-[rgba(244,249,247,0.7)]">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="container mx-auto py-20 px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Simple, Transparent Pricing</h2>
          <p className="text-xl text-[rgba(244,249,247,0.7)] max-w-3xl mx-auto">
            Choose the plan that works best for your needs
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Free Plan */}
          <Card className="bg-[rgba(22,68,48,0.3)] border-[rgba(63,215,165,0.2)] shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold">Free</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold">$0</span>
                <span className="text-[rgba(244,249,247,0.7)]">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>3 documents per month</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Basic templates</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>7-day document storage</span>
                </li>
                <li className="flex items-center text-[rgba(244,249,247,0.5)]">
                  <svg className="w-5 h-5 mr-2 text-[rgba(244,249,247,0.5)]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  <span>Advanced customization</span>
                </li>
                <li className="flex items-center text-[rgba(244,249,247,0.5)]">
                  <svg className="w-5 h-5 mr-2 text-[rgba(244,249,247,0.5)]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                  <span>Priority support</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full bg-[rgba(63,215,165,0.1)] text-[#3fd7a5] hover:bg-[rgba(63,215,165,0.2)] border border-[rgba(63,215,165,0.3)]">
                Get Started
              </Button>
            </CardFooter>
          </Card>

          {/* Pro Plan */}
          <Card className="bg-gradient-to-b from-[rgba(22,68,48,0.6)] to-[rgba(22,68,48,0.3)] border-[#3fd7a5] shadow-lg relative">
            <div className="absolute top-0 right-0 bg-[#3fd7a5] text-[#0a2817] font-bold py-1 px-4 rounded-bl-lg rounded-tr-lg text-sm">
              POPULAR
            </div>
            <CardHeader>
              <CardTitle className="text-2xl font-bold">Pro</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold">$19</span>
                <span className="text-[rgba(244,249,247,0.7)]">/month</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Unlimited documents</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>All templates</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>1-year document storage</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Advanced customization</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Priority support</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full bg-gradient-to-r from-[#3fd7a5] to-[#26856c] hover:opacity-90 transition-opacity">
                Upgrade Now
              </Button>
            </CardFooter>
          </Card>

          {/* Enterprise Plan */}
          <Card className="bg-[rgba(22,68,48,0.3)] border-[rgba(63,215,165,0.2)] shadow-lg">
            <CardHeader>
              <CardTitle className="text-2xl font-bold">Enterprise</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold">Custom</span>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Unlimited everything</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Custom templates</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Unlimited storage</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>Dedicated account manager</span>
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 mr-2 text-[#3fd7a5]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span>API access</span>
                </li>
              </ul>
            </CardContent>
            <CardFooter>
              <Button className="w-full bg-[rgba(63,215,165,0.1)] text-[#3fd7a5] hover:bg-[rgba(63,215,165,0.2)] border border-[rgba(63,215,165,0.3)]">
                Contact Sales
              </Button>
            </CardFooter>
          </Card>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="container mx-auto py-20 px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">What Our Customers Say</h2>
          <p className="text-xl text-[rgba(244,249,247,0.7)] max-w-3xl mx-auto">
            Trusted by businesses worldwide
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              quote: "DocGenius has transformed how we handle our legal documents. The AI-powered validation has saved us from countless potential issues.",
              author: "Sarah Johnson",
              role: "Legal Director, TechCorp"
            },
            {
              quote: "The document generation is lightning fast and the templates are professional. We've cut our document creation time by 75%.",
              author: "Michael Chen",
              role: "Operations Manager, Startify"
            },
            {
              quote: "As a small business owner, DocGenius gives me the confidence that my documents are legally sound without the expense of a legal team.",
              author: "Emma Rodriguez",
              role: "Founder, GreenStart"
            }
          ].map((testimonial, index) => (
            <Card key={index} className="bg-[rgba(22,68,48,0.3)] border-[rgba(63,215,165,0.2)] shadow-lg">
              <CardContent className="pt-6">
                <div className="mb-4 text-[#3fd7a5]">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-8 h-8">
                    <path d="M9.17 6C6.4 7.23 4.5 9.66 4.5 13.5V18H9V13.5H6.75C6.75 10.5 7.5 9.5 9.17 8.5V6ZM19.17 6C16.4 7.23 14.5 9.66 14.5 13.5V18H19V13.5H16.75C16.75 10.5 17.5 9.5 19.17 8.5V6Z" fill="currentColor"/>
                  </svg>
                </div>
                <p className="mb-6 text-[rgba(244,249,247,0.9)]">{testimonial.quote}</p>
                <div className="flex items-center">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-r from-[#3fd7a5] to-[#26856c] flex items-center justify-center text-white font-bold">
                    {testimonial.author.charAt(0)}
                  </div>
                  <div className="ml-4">
                    <p className="font-bold">{testimonial.author}</p>
                    <p className="text-sm text-[rgba(244,249,247,0.7)]">{testimonial.role}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto py-20 px-4">
        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-[#3fd7a5] to-[#26856c] rounded-lg blur opacity-30"></div>
          <div className="relative bg-[rgba(22,68,48,0.5)] p-12 rounded-lg border border-[rgba(63,215,165,0.3)] text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to transform your document workflow?</h2>
            <p className="text-xl mb-8 text-[rgba(244,249,247,0.7)] max-w-3xl mx-auto">
              Join thousands of businesses that trust DocGenius for their document needs.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button className="bg-gradient-to-r from-[#3fd7a5] to-[#26856c] hover:opacity-90 transition-opacity text-white px-8 py-6 text-lg">
                Get Started for Free
              </Button>
              <Button variant="outline" className="border-[#3fd7a5] text-[#3fd7a5] hover:bg-[rgba(63,215,165,0.1)] px-8 py-6 text-lg">
                Schedule a Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="container mx-auto py-20 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">Stay Updated</h2>
          <p className="text-[rgba(244,249,247,0.7)] mb-6">
            Subscribe to our newsletter for the latest updates, tips, and special offers.
          </p>
          <div className="flex flex-col sm:flex-row gap-2">
            <Input 
              type="email" 
              placeholder="Enter your email" 
              className="bg-[rgba(10,40,23,0.3)] border-[rgba(63,215,165,0.2)] text-[#f4f9f7] focus:border-[#3fd7a5] focus:ring-[#3fd7a5]"
            />
            <Button className="bg-gradient-to-r from-[#3fd7a5] to-[#26856c] hover:opacity-90 transition-opacity whitespace-nowrap">
              Subscribe
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#0a2817] border-t border-[rgba(63,215,165,0.2)] py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <span className="text-2xl font-bold bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text">D</span>
                <span className="text-xl font-bold ml-[-2px] text-[#f4f9f7]">oc</span>
                <span className="text-2xl font-bold bg-gradient-to-r from-[#3fd7a5] to-[#26856c] text-transparent bg-clip-text">G</span>
                <span className="text-xl font-bold ml-[-2px] text-[#f4f9f7]">enius</span>
              </div>
              <p className="text-[rgba(244,249,247,0.7)] mb-4">
                AI-powered document creation and validation for modern businesses.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-[#3fd7a5] hover:text-[#26856c]">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22.162 5.656a8.384 8.384 0 0 1-2.402.658A4.196 4.196 0 0 0 21.6 4c-.82.488-1.719.83-2.656 1.015a4.182 4.182 0 0 0-7.126 3.814 11.874 11.874 0 0 1-8.62-4.37 4.168 4.168 0 0 0-.566 2.103c0 1.45.738 2.731 1.86 3.481a4.168 4.168 0 0 1-1.894-.523v.052a4.185 4.185 0 0 0 3.355 4.101 4.21 4.21 0 0 1-1.89.072A4.185 4.185 0 0 0 7.97 16.65a8.394 8.394 0 0 1-6.191 1.732 11.83 11.83 0 0 0 6.41 1.88c7.693 0 11.9-6.373 11.9-11.9 0-.18-.005-.362-.013-.54a8.496 8.496 0 0 0 2.087-2.165z"/>
                  </svg>
                </a>
                <a href="#" className="text-[#3fd7a5] hover:text-[#26856c]">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.137 20.164 22 16.42 22 12c0-5.523-4.477-10-10-10z"/>
                  </svg>
                </a>
                <a href="#" className="text-[#3fd7a5] hover:text-[#26856c]">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                  </svg>
                </a>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Product</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Features</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Pricing</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Templates</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Security</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Company</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">About</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Blog</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Careers</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Contact</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-bold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Privacy Policy</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Terms of Service</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">Cookie Policy</a></li>
                <li><a href="#" className="text-[rgba(244,249,247,0.7)] hover:text-[#3fd7a5]">GDPR</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-[rgba(63,215,165,0.2)] mt-12 pt-8 text-center text-[rgba(244,249,247,0.5)]">
            <p>© {new Date().getFullYear()} DocGenius. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}