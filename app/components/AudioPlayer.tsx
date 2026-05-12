'use client';

import { useEffect, useRef, useState } from 'react';
import { Pause, Play, RotateCcw, SkipBack, SkipForward, Volume2 } from 'lucide-react';
import { Story } from '@/app/lib/types';

const fmt = (v: number) => `${Math.floor(v / 60)}:${`${Math.floor(v % 60)}`.padStart(2, '0')}`;

export function AudioPlayer({ story }: { story: Story }) {
  const ref = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);

  useEffect(() => {
    if (ref.current) {
      ref.current.load();
      setCurrent(0);
      setIsPlaying(false);
    }
  }, [story.id]);

  const toggle = () => {
    if (!ref.current) return;
    if (isPlaying) ref.current.pause(); else ref.current.play();
    setIsPlaying(!isPlaying);
  };

  const seek = (seconds: number) => {
    if (!ref.current) return;
    ref.current.currentTime = Math.max(0, Math.min(ref.current.currentTime + seconds, duration));
  };

  return (
    <section className="rounded-3xl bg-white/90 p-5 shadow-lg">
      <audio
        ref={ref}
        onTimeUpdate={(e) => setCurrent(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => setDuration(e.currentTarget.duration || 0)}
        onEnded={() => setIsPlaying(false)}
      >
        <source src={story.audioUrl} />
      </audio>
      <div className="flex flex-col gap-4 md:flex-row md:items-center">
        <img src={story.imageUrl} alt={story.title} className="h-40 w-full rounded-3xl object-cover md:w-60" />
        <div className="w-full">
          <h2 className="text-2xl font-bold">Now Playing: {story.title}</h2>
          <p className="text-sm">{story.scriptureReference}</p>
          <p className="mb-4 text-sm text-faithBlue/80">{story.doctrineTheme}</p>
          <input type="range" min={0} max={duration || 1} value={current} onChange={(e) => { if (ref.current) ref.current.currentTime = Number(e.target.value); }} className="w-full" aria-label="Seek" />
          <div className="mt-1 flex justify-between text-xs"><span>{fmt(current)}</span><span>{fmt(duration)}</span></div>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <button className="rounded-full bg-peachGrace p-3" onClick={() => seek(-15)} aria-label="Skip back 15 seconds"><SkipBack /></button>
            <button className="rounded-full bg-faithBlue p-4 text-white" onClick={toggle} aria-label="Play or pause">{isPlaying ? <Pause /> : <Play />}</button>
            <button className="rounded-full bg-peachGrace p-3" onClick={() => seek(15)} aria-label="Skip forward 15 seconds"><SkipForward /></button>
            <button className="rounded-full bg-mintHope p-3" onClick={() => { if (ref.current) ref.current.currentTime = 0; }} aria-label="Replay"><RotateCcw /></button>
            <label className="ml-auto flex items-center gap-2 text-sm"><Volume2 size={16} />
              <input type="range" min={0} max={1} step={0.05} value={volume} onChange={(e) => { const v = Number(e.target.value); setVolume(v); if (ref.current) ref.current.volume = v; }} aria-label="Volume" />
            </label>
          </div>
        </div>
      </div>
    </section>
  );
}
