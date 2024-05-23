import { writable } from "svelte/store";

interface CreateAlert {
    color: "green" | "red" | "yellow";
    message: string;
    dismissible?: boolean;
    timeout?: number;
}

interface Alert extends CreateAlert {
    id: number;
}

export const alerts = writable<Alert[]>([]);

export const addAlert = (alert: CreateAlert) => {
  // Create a unique ID so we can easily find/remove it
  // if it is dismissible/has a timeout.
  const id = Math.floor(Math.random() * 10000);

  // Setup some sensible defaults for a alert.
  const defaults = {
    id,
    color: "yellow",
    dismissible: true,
    timeout: 3000,
  };

  // Push the alert to the top of the list of alerts
  alerts.update((all) => [{ ...defaults, ...alert }, ...all]);

  // If alert is dismissible, dismiss it after "timeout" amount of time.
  if (alert.timeout) setTimeout(() => dismissAlert(id), alert.timeout);
};

export const dismissAlert = (id: number) => {
  alerts.update((all) => all.filter((t) => t.id !== id));
};