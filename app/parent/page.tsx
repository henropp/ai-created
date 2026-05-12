'use client';

import { FormEvent, useMemo, useState } from 'react';
import Link from 'next/link';
import { mockStories } from '@/app/data/mockStories';
import { Story, StoryCategory } from '@/app/lib/types';

const categories: StoryCategory[] = ['Bible Stories', 'Psalms & Prayer', 'Faith Lessons', 'Character & Virtue', "Jesus' Teachings", 'Bedtime Scripture'];

export default function ParentPage() {
  const [stories, setStories] = useState<Story[]>(mockStories);
  const [filterCategory, setFilterCategory] = useState<string>('All');
  const [filterAge, setFilterAge] = useState<string>('All');
  const [form, setForm] = useState<Story>({ ...mockStories[0], id: '' });

  const filtered = useMemo(() => stories.filter((story) =>
    (filterCategory === 'All' || story.category === filterCategory) &&
    (filterAge === 'All' || story.ageRange === filterAge)
  ), [stories, filterCategory, filterAge]);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    const id = form.id || String(Date.now());
    const candidate = { ...form, id };
    setStories((prev) => prev.some((s) => s.id === id) ? prev.map((s) => s.id === id ? candidate : s) : [candidate, ...prev]);
    setForm({ ...mockStories[0], id: '' });
  };

  return (
    <main className="mx-auto max-w-6xl p-4 md:p-8">
      <div className="mb-4 flex items-center justify-between"><h1 className="text-3xl font-black">Parent Dashboard</h1><Link href="/" className="rounded-full bg-white/80 px-4 py-2">Back Home</Link></div>
      <form onSubmit={onSubmit} className="grid gap-3 rounded-3xl bg-white/85 p-4 md:grid-cols-2">
        {['title','ageRange','duration','scriptureReference','doctrineTheme','audioUrl','imageUrl','description'].map((field) => (
          <label key={field} className="text-sm">{field}<input required={field !== 'imageUrl'} value={(form as any)[field]} onChange={(e) => setForm((prev) => ({ ...prev, [field]: e.target.value }))} className="mt-1 w-full rounded-xl border p-2" /></label>
        ))}
        <label className="text-sm">Category<select value={form.category} onChange={(e) => setForm((prev) => ({ ...prev, category: e.target.value as StoryCategory }))} className="mt-1 w-full rounded-xl border p-2">{categories.map((c)=><option key={c}>{c}</option>)}</select></label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={form.bedtimeFriendly} onChange={(e) => setForm((p)=>({...p, bedtimeFriendly:e.target.checked}))} /> Bedtime-friendly</label>
        <label className="flex items-center gap-2"><input type="checkbox" checked={form.favourite} onChange={(e) => setForm((p)=>({...p, favourite:e.target.checked}))} /> Favourite</label>
        <button className="rounded-full bg-faithBlue px-4 py-2 font-semibold text-white md:col-span-2">Save Story</button>
      </form>

      <div className="my-4 flex gap-3">
        <select value={filterCategory} onChange={(e)=>setFilterCategory(e.target.value)} className="rounded-xl border p-2"><option>All</option>{categories.map((c)=><option key={c}>{c}</option>)}</select>
        <select value={filterAge} onChange={(e)=>setFilterAge(e.target.value)} className="rounded-xl border p-2"><option>All</option>{[...new Set(stories.map((s)=>s.ageRange))].map((a)=><option key={a}>{a}</option>)}</select>
      </div>

      <div className="grid gap-3">
        {filtered.map((story) => (
          <button key={story.id} onClick={() => setForm(story)} className="rounded-2xl bg-white/80 p-4 text-left">
            <p className="font-bold">{story.title}</p>
            <p className="text-sm">{story.category} • Ages {story.ageRange} • {story.duration}</p>
            <p className="text-sm">{story.scriptureReference} | {story.doctrineTheme}</p>
          </button>
        ))}
      </div>
    </main>
  );
}
