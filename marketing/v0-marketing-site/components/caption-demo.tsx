"use client"

import { useEffect, useState } from "react"

export function CaptionDemo() {
  const [displayedText, setDisplayedText] = useState("")
  const fullText = "Words roll onto screen as they're spoken..."
  
  useEffect(() => {
    let index = 0
    const interval = setInterval(() => {
      if (index <= fullText.length) {
        setDisplayedText(fullText.slice(0, index))
        index++
      } else {
        // Reset after a pause
        setTimeout(() => {
          index = 0
          setDisplayedText("")
        }, 2000)
      }
    }, 100)
    
    return () => clearInterval(interval)
  }, [])

  return (
    <section className="py-24" aria-labelledby="caption-demo-heading">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <h2 id="caption-demo-heading" className="text-3xl font-bold text-foreground sm:text-4xl text-balance">
              Captions That Keep Viewers Locked In
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Words roll onto screen as they're spoken — bold, high-contrast typewriter text. Choose captions on, off, or generate both versions in one job.
            </p>
          </div>
          
          {/* Visual mockup */}
          <div className="relative aspect-video overflow-hidden rounded-xl border border-border bg-card">
            {/* Dark video frame background */}
            <div className="absolute inset-0 bg-gradient-to-br from-background via-card to-background" />
            
            {/* Terminal-style frame */}
            <div className="absolute inset-4 flex flex-col rounded-lg border border-border/50 bg-background/80 font-mono">
              {/* Terminal header */}
              <div className="flex items-center gap-2 border-b border-border/50 px-4 py-2">
                <div className="h-3 w-3 rounded-full bg-red-500/70" />
                <div className="h-3 w-3 rounded-full bg-yellow-500/70" />
                <div className="h-3 w-3 rounded-full bg-green-500/70" />
                <span className="ml-2 text-xs text-muted-foreground">captions.mp4</span>
              </div>
              
              {/* Caption display area */}
              <div className="flex flex-1 items-center justify-center p-6">
                <p className="text-center text-xl font-bold text-foreground sm:text-2xl">
                  {displayedText}
                  <span className="animate-blink ml-0.5 inline-block h-6 w-0.5 bg-accent" aria-hidden="true" />
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
