"use client"

import { FileText, Sparkles, Image, Film } from "lucide-react"

const steps = [
  {
    number: 1,
    icon: FileText,
    title: "Type your idea",
    description: "Describe any video concept in plain text",
  },
  {
    number: 2,
    icon: Sparkles,
    title: "AI writes the script",
    description: "An LLM breaks your idea into scenes with narration and visual cues",
  },
  {
    number: 3,
    icon: Image,
    title: "Visuals + voice generated",
    description: "AI creates an image for each scene and narrates the script",
  },
  {
    number: 4,
    icon: Film,
    title: "Get your video",
    description: "FFmpeg assembles everything into a polished MP4 with crossfade transitions",
  },
]

export function HowItWorks() {
  return (
    <section className="py-24" aria-labelledby="how-it-works-heading">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <h2 id="how-it-works-heading" className="text-center text-3xl font-bold text-foreground sm:text-4xl">
          How It Works
        </h2>
        
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className="animate-fade-in-up relative rounded-xl border border-border bg-card p-6 transition-colors hover:border-primary/50"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="mb-4 flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
                  {step.number}
                </span>
                <step.icon className="h-5 w-5 text-accent" aria-hidden="true" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">{step.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
