"use client"

import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"

export function HeroSection() {
  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden pt-16">
      {/* Animated gradient background */}
      <div 
        className="animate-gradient absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-accent/5"
        aria-hidden="true"
      />
      {/* Grain texture overlay */}
      <div 
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
        aria-hidden="true"
      />
      
      <div className="relative z-10 mx-auto max-w-4xl px-4 text-center sm:px-6">
        <h1 className="animate-fade-in-up text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl md:text-6xl lg:text-7xl text-balance">
          Turn Any Idea Into a Narrated Video
        </h1>
        <p className="animate-fade-in-up mx-auto mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl" style={{ animationDelay: '0.1s' }}>
          Type a prompt. Get a fully produced video with AI visuals, voiceover, and captions. No editing. No timeline. Just vibes.
        </p>
        
        <div className="animate-fade-in-up mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center" style={{ animationDelay: '0.2s' }}>
          <Button
            asChild
            size="lg"
            className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-6 text-lg"
          >
            <a href="#signup">Get Early Access to Pro</a>
          </Button>
          <Link
            href="https://github.com/mayurjobanputra/VibeYourVideos"
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-2 text-muted-foreground transition-colors hover:text-accent"
          >
            {"It's open source — try it free on GitHub"}
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden="true" />
          </Link>
        </div>
        
        <p className="animate-fade-in-up mt-8 text-sm text-muted-foreground" style={{ animationDelay: '0.3s' }}>
          Open source · MIT licensed · 100% local
        </p>
      </div>
    </section>
  )
}
