import { useEffect, useState } from "react";

export function useRealtime(url: string) {
  const [events, setEvents] = useState<unknown[]>([]);
  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onmessage = event => setEvents(current => [JSON.parse(event.data), ...current].slice(0, 20));
    return () => socket.close();
  }, [url]);
  return events;
}
