export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export type RoleName = "fan" | "volunteer" | "organizer" | "admin";

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("stadiumai_token");
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init.headers
    }
  });
  if (!response.ok) throw new Error((await response.text()) || response.statusText);
  return response.json() as Promise<T>;
}

export const demo = {
  crowd: [
    { zone: "Gate B", density: 0.88, queue_length: 620, wait_minutes: 28, risk: "critical", ai_summary: "Metro arrivals are increasing Gate B pressure.", alternative_route: "Redirect to Gate D via east concourse." },
    { zone: "Food Court North", density: 0.54, queue_length: 120, wait_minutes: 9, risk: "normal", ai_summary: "Food Court North remains within service capacity.", alternative_route: "Maintain routing." }
  ],
  sustainability: { water_liters: 82400, electricity_kwh: 21800, waste_kg: 5600, carbon_kg: 9510, recommendations: ["Dim low-density concourse lighting.", "Move recycling crews to North Stand.", "Promote Metro Line 2 for lower carbon travel."] }
};
