/// <reference types="vite/client" />

import { Alpine } from "alpinejs";
import Notification from "./alert";

declare global {
  interface Window {
    Alpine: Alpine;
    Notification: Notification
  }
}
