"use client"

import { Check } from "lucide-react"

const proFeatures = [
  "Longer videos beyond 90 seconds",
  "Content Design Studio — fine-tune scripts, visuals, and pacing before rendering",
  "Advanced caption styling and positioning",
  "Animated content instead of static images",
  "Brand Kit — logos, fonts, color palettes for consistent branding",
  "Video reference — use existing footage as a style guide",
  "Scheduler — queue and schedule video generation",
  "Automation Engine — trigger video creation from external events",
  "Direct upload to social platforms",
]

export function ProTeaser() {
  const midpoint = Math.ceil(proFeatures.length / 2)
  const leftColumn = proFeatures.slice(0, midpoint)
  const rightColumn = proFeatures.slice(midpoint)

  return (
    <section className="bg-card/30 py-24" aria-labelledby="pro-teaser-heading">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="text-center">
          <span className="inline-block rounded-full border border-primary/50 bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
            Coming Soon
          </span>
          <h2 id="pro-teaser-heading" className="mt-4 text-3xl font-bold text-foreground sm:text-4xl">
            Vibe Your Videos Pro
          </h2>
        </div>
        
        <div className="mt-12 rounded-2xl border border-border bg-card p-8 sm:p-12">
          <h3 className="text-2xl font-bold text-foreground sm:text-3xl text-balance">
            Go Beyond 90 Seconds
          </h3>
          <p className="mt-2 text-lg text-muted-foreground">
            Pro is for creators and teams who want full control.
          </p>
          
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            <ul className="space-y-4" aria-label="Pro features, part 1">
              {leftColumn.map((feature) => (
                <li key={feature} className="flex items-start gap-3">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/20">
                    <Check className="h-3 w-3 text-primary" aria-hidden="true" />
                  </span>
                  <span className="text-foreground">{feature}</span>
                </li>
              ))}
            </ul>
            <ul className="space-y-4" aria-label="Pro features, part 2">
              {rightColumn.map((feature) => (
                <li key={feature} className="flex items-start gap-3">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/20">
                    <Check className="h-3 w-3 text-primary" aria-hidden="true" />
                  </span>
                  <span className="text-foreground">{feature}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <p className="mt-10 text-center text-lg font-medium text-accent">
            Be first in line when Pro launches.
          </p>
        </div>
      </div>
    </section>
  )
}
