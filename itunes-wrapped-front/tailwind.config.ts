import type { Config } from 'tailwindcss/types/config'

const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,vue}'],
  theme: {
    extend: {
      colors: {
        blue: '#35c0fb',
        pink: '#ff5e73',
        purple: '#35c0fb',
      },
    },
  },
}

export default config
