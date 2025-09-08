import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'app.lovable.6e9ac0a59d8949729e86bb258a07ab43',
  appName: 'aura-mind-spark-tutor',
  webDir: 'dist',
  server: {
    url: 'https://6e9ac0a5-9d89-4972-9e86-bb258a07ab43.lovableproject.com?forceHideBadge=true',
    cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 0
    }
  }
};

export default config;