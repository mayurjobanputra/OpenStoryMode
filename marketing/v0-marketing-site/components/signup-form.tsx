"use client"

import { useState, useTransition } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Check, Loader2 } from "lucide-react"

export function SignupForm() {
  const [email, setEmail] = useState("")
  const [error, setError] = useState("")
  const [isSuccess, setIsSuccess] = useState(false)
  const [isPending, startTransition] = useTransition()

  const validateEmail = (email: string) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return regex.test(email)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!email) {
      setError("Please enter your email address")
      return
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email address")
      return
    }

    startTransition(async () => {
      try {
        const response = await fetch("/api/waitlist", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        })

        if (!response.ok) {
          throw new Error("Failed to join waitlist")
        }

        setIsSuccess(true)
      } catch {
        setError("Something went wrong. Please try again.")
      }
    })
  }

  return (
    <section id="signup" className="py-24" aria-labelledby="signup-heading">
      <div className="mx-auto max-w-xl px-4 sm:px-6">
        <div className="rounded-2xl border border-border bg-card p-8 text-center sm:p-12">
          {isSuccess ? (
            <div className="animate-fade-in-up">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/20">
                <Check className="h-8 w-8 text-primary" aria-hidden="true" />
              </div>
              <h2 className="mt-6 text-2xl font-bold text-foreground sm:text-3xl">
                {"You're on the list 🎬"}
              </h2>
              <p className="mt-2 text-muted-foreground">
                {"We'll let you know when Pro is ready."}
              </p>
              {/* Confetti effect */}
              <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
                {[...Array(12)].map((_, i) => (
                  <div
                    key={i}
                    className="animate-confetti absolute h-3 w-3 rounded-sm"
                    style={{
                      left: `${Math.random() * 100}%`,
                      top: `${Math.random() * 50 + 50}%`,
                      backgroundColor: i % 2 === 0 ? "#7c3aed" : "#a78bfa",
                      animationDelay: `${Math.random() * 0.5}s`,
                    }}
                  />
                ))}
              </div>
            </div>
          ) : (
            <>
              <h2 id="signup-heading" className="text-2xl font-bold text-foreground sm:text-3xl">
                Get Early Access
              </h2>
              <p className="mt-2 text-muted-foreground">
                {"Drop your email. We'll let you know when Pro is ready — plus early-bird pricing."}
              </p>
              
              <form onSubmit={handleSubmit} className="mt-8">
                <div className="flex flex-col gap-3 sm:flex-row">
                  <Input
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="flex-1 bg-background border-border text-foreground placeholder:text-muted-foreground"
                    aria-label="Email address"
                    aria-describedby={error ? "email-error" : undefined}
                    disabled={isPending}
                  />
                  <Button
                    type="submit"
                    className="bg-primary text-primary-foreground hover:bg-primary/90"
                    disabled={isPending}
                  >
                    {isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
                        Joining...
                      </>
                    ) : (
                      "Join the Waitlist"
                    )}
                  </Button>
                </div>
                {error && (
                  <p id="email-error" className="mt-2 text-sm text-red-400" role="alert">
                    {error}
                  </p>
                )}
              </form>
              
              <p className="mt-4 text-sm text-muted-foreground">
                No spam. Unsubscribe anytime.
              </p>
            </>
          )}
        </div>
      </div>
    </section>
  )
}
