/// <reference types="vite/client" />

import { Alpine } from 'alpinejs';

declare global {
  interface Window {
    Alpine: Alpine;
  }
}
