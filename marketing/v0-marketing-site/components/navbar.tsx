"use client"

import Link from "next/link"
import { Github } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Navbar() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6" aria-label="Main navigation">
        <Link href="/" className="text-xl font-bold text-accent">
          Vibe Your Videos
        </Link>
        <div className="flex items-center gap-4">
          <Link
            href="https://github.com/mayurjobanputra/VibeYourVideos"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
            aria-label="View on GitHub"
          >
            <Github className="h-5 w-5" aria-hidden="true" />
            <span className="hidden sm:inline">GitHub</span>
          </Link>
          <Button
            asChild
            className="bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <a href="#signup">Get Early Access</a>
          </Button>
        </div>
      </nav>
    </header>
  )
}
