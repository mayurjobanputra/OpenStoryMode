import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { HowItWorks } from "@/components/how-it-works"
import { FeaturesGrid } from "@/components/features-grid"
import { CaptionDemo } from "@/components/caption-demo"
import { ProTeaser } from "@/components/pro-teaser"
import { SignupForm } from "@/components/signup-form"
import { OpenSourceCTA } from "@/components/open-source-cta"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />
        <HowItWorks />
        <FeaturesGrid />
        <CaptionDemo />
        <ProTeaser />
        <SignupForm />
        <OpenSourceCTA />
      </main>
      <Footer />
    </>
  )
}
