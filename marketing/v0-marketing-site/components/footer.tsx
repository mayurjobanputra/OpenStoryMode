"use client"

import Link from "next/link"
import { Github, ArrowUp } from "lucide-react"

export function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  return (
    <footer className="border-t border-border py-8">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6">
        <p className="text-sm text-muted-foreground">
          © 2026 Vibe Your Videos
        </p>
        
        <nav className="flex items-center gap-6" aria-label="Footer navigation">
          <Link
            href="https://github.com/mayurjobanputra/VibeYourVideos"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
            aria-label="View on GitHub"
          >
            <Github className="h-4 w-4" aria-hidden="true" />
            GitHub
          </Link>
          <button
            onClick={scrollToTop}
            className="flex items-center gap-1 text-sm text-muted-foreground transition-colors hover:text-foreground"
            aria-label="Back to top"
          >
            Back to top
            <ArrowUp className="h-4 w-4" aria-hidden="true" />
          </button>
        </nav>
      </div>
    </footer>
  )
}
