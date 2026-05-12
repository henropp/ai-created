import { PlayCircle } from 'lucide-react';
import { Story } from '@/app/lib/types';

export function StoryCard({ story, onPlay }: { story: Story; onPlay?: (story: Story) => void }) {
  return (
    <article className="rounded-3xl bg-white/85 p-4 shadow-sm ring-1 ring-faithBlue/10">
      <img src={story.imageUrl} alt={story.title} className="h-36 w-full rounded-2xl object-cover" />
      <h3 className="mt-3 text-lg font-bold">{story.title}</h3>
      <p className="text-sm">{story.category} • Ages {story.ageRange} • {story.duration}</p>
      <p className="mt-2 text-sm text-faithBlue/80">{story.description}</p>
      <p className="mt-2 text-xs"><strong>Scripture:</strong> {story.scriptureReference}</p>
      <p className="text-xs"><strong>Doctrine:</strong> {story.doctrineTheme}</p>
      {onPlay && (
        <button onClick={() => onPlay(story)} className="mt-3 flex w-full items-center justify-center gap-2 rounded-full bg-faithBlue px-4 py-2 text-white" aria-label={`Play ${story.title}`}>
          <PlayCircle size={18} /> Play Story
        </button>
      )}
    </article>
  );
}
