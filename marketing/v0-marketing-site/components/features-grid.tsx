"use client"

import { Clock, Smartphone, Type, FileText, ImageIcon, Server } from "lucide-react"

const features = [
  {
    icon: Clock,
    title: "Up to 90s videos",
    description: "Short-form content, ready to post",
  },
  {
    icon: Smartphone,
    title: "Vertical + Horizontal",
    description: "9:16 for Reels/TikTok, 16:9 for YouTube",
  },
  {
    icon: Type,
    title: "Typewriter Captions",
    description: "Words appear as they're spoken, bold high-contrast text",
  },
  {
    icon: FileText,
    title: "AI Script Writing",
    description: "Scene-by-scene scripts from a single prompt",
  },
  {
    icon: ImageIcon,
    title: "AI Image Generation",
    description: "Unique visuals for every scene",
  },
  {
    icon: Server,
    title: "Runs 100% Locally",
    description: "Your content, your data, your machine",
  },
]

export function FeaturesGrid() {
  return (
    <section className="bg-card/30 py-24" aria-labelledby="features-heading">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 id="features-heading" className="text-center text-3xl font-bold text-foreground sm:text-4xl">
          What You Get (Free)
        </h2>
        
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="animate-fade-in-up rounded-xl border border-border bg-card p-6 transition-all hover:border-primary/50 hover:shadow-lg hover:shadow-primary/5"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <feature.icon className="h-6 w-6 text-primary" aria-hidden="true" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">{feature.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
