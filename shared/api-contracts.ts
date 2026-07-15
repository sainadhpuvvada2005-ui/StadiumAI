export type RoleName = "fan" | "volunteer" | "organizer" | "admin";
export type LanguageCode = "en" | "es" | "fr" | "pt" | "ar" | "hi";
export interface AIChatRequest { message: string; language: LanguageCode; context: Record<string, unknown>; }
export interface AIChatResponse { answer: string; language: LanguageCode; sources: string[]; recommendations: string[]; }
