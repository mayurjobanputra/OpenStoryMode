import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: 'Vibe Your Videos — AI Video Generator | Turn Text Into Narrated Videos',
  description: 'Turn any idea into a narrated video with AI-generated visuals, voiceover, and typewriter captions. Open source, runs locally. Try free or join the Pro waitlist.',
  keywords: 'AI video generator, text to video, AI narration, AI visuals, open source video tool, typewriter captions, video from prompt, vibe your videos',
  authors: [{ name: 'Vibe Your Videos' }],
  icons: {
    icon: '/favicon.ico',
  },
  openGraph: {
    title: 'Vibe Your Videos — Turn Any Idea Into a Narrated Video',
    description: 'AI-generated visuals, voiceover, and typewriter captions. Open source and free. Pro coming soon.',
    type: 'website',
    url: 'https://vibeyourvideos.com',
    images: [
      {
        url: 'https://vibeyourvideos.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Vibe Your Videos - AI Video Generator',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Vibe Your Videos — Turn Any Idea Into a Narrated Video',
    description: 'AI-generated visuals, voiceover, and typewriter captions. Open source and free. Pro coming soon.',
    images: ['https://vibeyourvideos.com/og-image.png'],
  },
  alternates: {
    canonical: 'https://vibeyourvideos.com',
  },
}

export const viewport: Viewport = {
  themeColor: '#0f0f13',
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              "name": "Vibe Your Videos",
              "applicationCategory": "MultimediaApplication",
              "operatingSystem": "Cross-platform",
              "description": "Turn any idea into a narrated video with AI-generated visuals, voiceover, and typewriter captions.",
              "url": "https://vibeyourvideos.com",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              },
              "license": "https://opensource.org/licenses/MIT"
            })
          }}
        />
      </head>
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  )
}
