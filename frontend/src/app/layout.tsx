import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/components/providers/QueryProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Wildlife Drone Detection",
  description: "AI-powered wildlife detection and tracking from drone footage",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryProvider>
          <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
            {children}
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}

