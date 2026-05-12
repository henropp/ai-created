'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import { AudioPlayer } from '@/app/components/AudioPlayer';
import { StoryCard } from '@/app/components/StoryCard';
import { mockStories } from '@/app/data/mockStories';
import { Story } from '@/app/lib/types';

export default function HomePage() {
  const [currentStory, setCurrentStory] = useState<Story>(mockStories[0]);

  const categories = useMemo(() => [...new Set(mockStories.map((story) => story.category))], []);

  return (
    <main className="mx-auto max-w-6xl p-4 md:p-8">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-3xl font-black">Christian Story Player for Kids</h1>
        <nav className="flex gap-2 text-sm">
          <Link href="/child" className="rounded-full bg-white/80 px-4 py-2">Child Mode</Link>
          <Link href="/parent" className="rounded-full bg-faithBlue px-4 py-2 text-white">Parent Dashboard</Link>
        </nav>
      </header>

      <AudioPlayer story={currentStory} />

      <section className="mt-8 rounded-3xl bg-white/70 p-5">
        <h2 className="text-xl font-bold">Scripture for this story</h2>
        <p className="mt-1">{currentStory.scriptureReference} — {currentStory.doctrineTheme}</p>
      </section>

      <section className="mt-8">
        <h2 className="mb-4 text-2xl font-bold">Story Card Library</h2>
        {categories.map((category) => (
          <div key={category} className="mb-6">
            <h3 className="mb-3 text-lg font-semibold">{category}</h3>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {mockStories.filter((story) => story.category === category).map((story) => (
                <StoryCard key={story.id} story={story} onPlay={setCurrentStory} />
              ))}
            </div>
          </div>
        ))}
      </section>
    </main>
  );
}
