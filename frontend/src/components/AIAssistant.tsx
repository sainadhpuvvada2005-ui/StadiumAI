import { useState } from "react";
import { Bot, Send, Languages, Loader, LogOut } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { api } from "../lib/api";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";
import { useAuth } from "../lib/AuthContext";

type ChatOut = { answer: string; sources: string[]; recommendations: string[] };

export function AIAssistant() {
  const [message, setMessage] = useState("Which gate should I use and how crowded is Gate B?");
  const [language, setLanguage] = useState("en");
  const chat = useMutation({
    mutationFn: (vars: { message: string; language: string }) => api<ChatOut>("/ai/chat", { method: "POST", body: JSON.stringify({ ...vars, context: {} }) }),
  });
  const { logout } = useAuth();

  const handleAsk = () => {
    chat.mutate({ message, language });
  };

  return (
    <Card className="space-y-3">
      <div className="flex items-center justify-between gap-2">
        <h2 className="flex items-center gap-2 text-lg font-bold"><Bot size={20} /> AI Stadium Assistant</h2>
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2 text-sm"><Languages size={16} /><select value={language} onChange={e => setLanguage(e.target.value)} className="rounded-md border border-slate-300 bg-white px-2 py-1 dark:border-slate-700 dark:bg-slate-950"><option value="en">English</option><option value="es">Spanish</option><option value="fr">French</option><option value="pt">Portuguese</option><option value="ar">Arabic</option><option value="hi">Hindi</option></select></label>
          <Button onClick={logout} className="bg-slate-600 hover:bg-slate-700"><LogOut size={16} /> Sign Out</Button>
        </div>
      </div>
      <textarea value={message} onChange={e => setMessage(e.target.value)} className="min-h-24 w-full rounded-md border border-slate-300 bg-white p-3 dark:border-slate-700 dark:bg-slate-950" aria-label="Ask the AI assistant" />
      <Button onClick={handleAsk} disabled={chat.isPending}>{chat.isPending ? <><Loader size={16} className="animate-spin" /> Thinking...</> : <><Send size={16} /> Ask AI</>}</Button>
      {chat.isError && <p role="alert" className="rounded-md bg-red-50 p-3 text-red-700 dark:bg-red-950 dark:text-red-200">The assistant could not respond. Check API connectivity and authentication.</p>}
      {chat.isSuccess && <div className="rounded-md bg-teal-50 p-3 text-sm dark:bg-teal-950"><p>{chat.data.answer}</p><p className="mt-2 font-semibold">Sources: {chat.data.sources.join(", ")}</p></div>}
    </Card>
  );
}
