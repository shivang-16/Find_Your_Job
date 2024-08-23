import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils"
 
const fontSans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})


export const metadata: Metadata = {
  title: "Find Your Job",
  description: "Single Platform to get job from all platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={cn(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable
        )}>{children}</body>
    </html>
  );
}
