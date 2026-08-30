import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CreatorRadar — Open-Source Creator Intelligence Platform',
  description: 'Monitor creators, detect patterns, and convert inspiration into original content opportunities.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-slate-950 text-slate-100 selection:bg-blue-600 selection:text-white">
        {children}
      </body>
    </html>
  );
}
