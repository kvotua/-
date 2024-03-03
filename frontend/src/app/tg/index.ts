declare global {
  interface Window {
    Telegram: unknown;
  }
}

// @ts-expect-error unknown type used right now, later Telegram interface must be here
export const tg = window.Telegram.WebApp;
