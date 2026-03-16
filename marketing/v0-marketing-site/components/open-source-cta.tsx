"use client"

import Link from "next/link"
import { Star } from "lucide-react"
import { Button } from "@/components/ui/button"

export function OpenSourceCTA() {
  return (
    <section className="py-24" aria-labelledby="open-source-heading">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="relative overflow-hidden rounded-2xl border border-primary/30 bg-card p-8 sm:p-12">
          {/* Purple accent glow */}
          <div 
            className="absolute -left-20 -top-20 h-40 w-40 rounded-full bg-primary/20 blur-3xl"
            aria-hidden="true"
          />
          <div 
            className="absolute -bottom-20 -right-20 h-40 w-40 rounded-full bg-accent/20 blur-3xl"
            aria-hidden="true"
          />
          
          <div className="relative z-10 text-center">
            <h2 id="open-source-heading" className="text-2xl font-bold text-foreground sm:text-3xl">
              Vibe Your Videos is free and open source.
            </h2>
            
            <div className="mt-6 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button
                asChild
                size="lg"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Link
                  href="https://github.com/mayurjobanputra/VibeYourVideos"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Star className="mr-2 h-5 w-5" aria-hidden="true" />
                  Star us on GitHub
                </Link>
              </Button>
              
              <span className="inline-flex items-center rounded-full border border-border bg-background px-4 py-2 text-sm font-medium text-muted-foreground">
                MIT Licensed
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
