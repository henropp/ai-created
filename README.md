# Christian Story Player for Kids (MVP)

A child-friendly Christian audio-story web app built with Next.js, TypeScript, and Tailwind CSS.

## Features
- Home Player with play/pause, replay, skip ±15s, progress, volume, now playing, and scripture focus.
- Story card library across six categories.
- Parent dashboard for adding/editing stories and filtering by age/category.
- Child mode with large buttons and simplified interaction.
- 12 mock Christian stories included.

## Tech Stack
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Local mock data (no backend)

## Run locally
```bash
npm install
npm run dev
```
Open `http://localhost:3000`.

## Project structure
- `app/page.tsx` Home/player + library
- `app/child/page.tsx` Child mode
- `app/parent/page.tsx` Parent dashboard
- `app/components/*` Reusable UI components
- `app/data/mockStories.ts` Mock story data
- `app/lib/types.ts` Shared types
- `ROADMAP.md` Future feature direction
