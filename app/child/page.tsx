'use client';

import Link from 'next/link';
import { useState } from 'react';
import { AudioPlayer } from '@/app/components/AudioPlayer';
import { mockStories } from '@/app/data/mockStories';

export default function ChildPage() {
  const [selected, setSelected] = useState(mockStories[0]);
  return (
    <main className="mx-auto max-w-5xl p-4 md:p-8">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-3xl font-black">Child Mode</h1>
        <Link href="/" className="rounded-full bg-white/80 px-4 py-2">Back Home</Link>
      </div>
      <AudioPlayer story={selected} />
      <h2 className="mt-6 mb-3 text-xl font-bold">Choose a Story</h2>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {mockStories.map((story) => (
          <button key={story.id} className="rounded-3xl bg-white/85 p-3 text-left text-sm font-semibold" onClick={() => setSelected(story)}>
            <img src={story.imageUrl} alt="" className="mb-2 h-20 w-full rounded-2xl object-cover" />
            {story.title}
          </button>
        ))}
      </div>
    </main>
  );
}
