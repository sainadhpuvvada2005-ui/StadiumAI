import { motion } from "framer-motion";
import type { ElementType } from "react";
import { Activity, ArrowRight, Globe2, Leaf, Map, ShieldAlert, Users } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";

const features: Array<[string, ElementType, string]> = [
  ["AI Navigation", Map, "Seat, gate, restroom, parking, food, and accessible routing from live operations data."],
  ["Crowd Intelligence", Users, "Queue prediction, congestion alerts, heat maps, and alternative route generation."],
  ["Emergency Copilot", ShieldAlert, "Medical, fire, security, and lost-child response summaries with priority and actions."],
  ["Sustainability", Leaf, "Water, electricity, waste, and carbon recommendations for venue operators."],
  ["Multilingual Voice", Globe2, "English, Spanish, French, Portuguese, Arabic, and Hindi assistance."]
];

export function Landing() {
  return (
    <div>
      <section className="relative min-h-[92vh] overflow-hidden bg-[url('https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=1800&q=80')] bg-cover bg-center text-white">
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/55 to-emerald-950/60" />
        <div className="relative mx-auto flex min-h-[92vh] max-w-7xl flex-col justify-center px-4 pb-16 pt-24">
          <motion.p initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-3 font-semibold text-signal">FIFA World Cup 2026 Operations AI</motion.p>
          <motion.h1 initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .08 }} className="max-w-4xl text-5xl font-black md:text-7xl">STADIUMAI</motion.h1>
          <p className="mt-5 max-w-2xl text-xl text-slate-100">The AI-Powered Smart Stadium Assistant for FIFA World Cup 2026</p>
          <div className="mt-8 flex flex-wrap gap-3"><Link to="/auth"><Button><ArrowRight size={18} />Open Dashboard</Button></Link><Link to="/organizer"><Button className="bg-white text-slate-950 hover:bg-slate-100"><Activity size={18} />Live Operations</Button></Link></div>
          <div className="mt-14 grid gap-3 sm:grid-cols-3">
            {[["74k", "fans guided"], ["11 min", "queue reduction"], ["6", "languages live"]].map(([value, label]) => <div key={label} className="rounded-lg border border-white/20 bg-white/10 p-4 backdrop-blur"><p className="text-3xl font-black">{value}</p><p className="text-slate-200">{label}</p></div>)}
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-7xl px-4 py-14">
        <h2 className="text-3xl font-black">Operational AI, not just chat</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">{features.map(([title, Icon, body]) => <Card key={title as string}><Icon className="text-fifa" /><h3 className="mt-3 text-xl font-bold">{title as string}</h3><p className="mt-2 text-slate-600 dark:text-slate-300">{body as string}</p></Card>)}</div>
      </section>
      <section className="bg-slate-100 py-14 dark:bg-slate-950"><div className="mx-auto grid max-w-7xl gap-4 px-4 md:grid-cols-3"><Card><h3 className="font-bold">Organizer testimonial</h3><p className="mt-2">"The command center gets a plain-language summary before a queue becomes a safety issue."</p></Card><Card><h3 className="font-bold">Volunteer testimonial</h3><p className="mt-2">"Tasks, crowd alerts, and incident guidance are in one place."</p></Card><Card><h3 className="font-bold">Fan testimonial</h3><p className="mt-2">"I found my seat, food, and the quietest exit without guessing."</p></Card></div></section>
      <section className="mx-auto max-w-4xl px-4 py-14"><h2 className="text-3xl font-black">FAQ</h2>{["Does it support accessibility?", "Can it answer in my language?", "Does it use live data?"].map(q => <details key={q} className="mt-3 rounded-lg border border-slate-200 p-4 dark:border-slate-800"><summary className="font-bold">{q}</summary><p className="mt-2 text-slate-600 dark:text-slate-300">Yes. STADIUMAI combines operational data, RAG, voice, and role permissions to guide fans and staff safely.</p></details>)}</section>
      <footer className="border-t border-slate-200 px-4 py-8 text-center dark:border-slate-800">STADIUMAI - Smart stadium assistance for safer, faster, more sustainable events. Contact: ops@stadiumai.example</footer>
    </div>
  );
}
