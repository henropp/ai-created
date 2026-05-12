export type StoryCategory =
  | 'Bible Stories'
  | 'Psalms & Prayer'
  | 'Faith Lessons'
  | 'Character & Virtue'
  | "Jesus' Teachings"
  | 'Bedtime Scripture';

export interface Story {
  id: string;
  title: string;
  category: StoryCategory;
  ageRange: string;
  duration: string;
  description: string;
  scriptureReference: string;
  doctrineTheme: string;
  audioUrl: string;
  imageUrl: string;
  bedtimeFriendly: boolean;
  favourite: boolean;
}
