import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        skyBless: '#dff5ff',
        peachGrace: '#ffe8d9',
        mintHope: '#e4f9ef',
        faithBlue: '#1f4f7a',
        warmGold: '#f4b860'
      }
    }
  },
  plugins: []
};

export default config;
