import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Christian Story Player for Kids',
  description: 'A gentle Christian audio-story player for children and families.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
