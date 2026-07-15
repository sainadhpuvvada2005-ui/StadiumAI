export type RoleName = "fan" | "volunteer" | "organizer" | "admin";
export type LanguageCode = "en" | "es" | "fr" | "pt" | "ar" | "hi";
export type IncidentType = "medical" | "fire" | "security" | "lost_child" | "operations";
export interface CrowdInsight { zone: string; density: number; queue_length: number; wait_minutes: number; risk: string; ai_summary: string; alternative_route: string; }
