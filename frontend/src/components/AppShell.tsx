import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Bell, Contrast, LogOut, Menu, Mic, Moon, SunMedium } from "lucide-react";
import { Button } from "./ui/Button";

export function AppShell({ children, role }: { children: ReactNode; role: string }) {
  const [dark, setDark] = useState(() => localStorage.getItem("stadiumai_theme") === "dark");
  const [largeText, setLargeText] = useState(false);
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("stadiumai_theme", dark ? "dark" : "light");
  }, [dark]);
  return (
    <div className={largeText ? "text-lg" : ""}>
      <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-night/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="text-xl font-black tracking-wide">STADIUMAI</Link>
          <nav className="hidden items-center gap-3 md:flex" aria-label="Primary">
            {["fan", "volunteer", "organizer", "admin"].map(item => <Link key={item} className={item === role ? "font-bold text-fifa" : "text-slate-600 dark:text-slate-300"} to={`/${item}`}>{item}</Link>)}
          </nav>
          <div className="flex items-center gap-2">
            <Button className="bg-slate-100 p-2 text-slate-900 hover:bg-slate-200 dark:bg-slate-800 dark:text-white" aria-label="Voice assistant"><Mic size={18} /></Button>
            <Button className="bg-slate-100 p-2 text-slate-900 hover:bg-slate-200 dark:bg-slate-800 dark:text-white" aria-label="Notifications"><Bell size={18} /></Button>
            <Button onClick={() => setLargeText(v => !v)} className="bg-slate-100 p-2 text-slate-900 hover:bg-slate-200 dark:bg-slate-800 dark:text-white" aria-label="Adjust font size"><Contrast size={18} /></Button>
            <Button onClick={() => setDark(v => !v)} className="bg-slate-100 p-2 text-slate-900 hover:bg-slate-200 dark:bg-slate-800 dark:text-white" aria-label="Toggle dark mode">{dark ? <SunMedium size={18} /> : <Moon size={18} />}</Button>
            <Button className="hidden bg-slate-900 md:inline-flex"><LogOut size={18} />Sign out</Button>
            <Button className="bg-slate-100 p-2 text-slate-900 md:hidden dark:bg-slate-800 dark:text-white" aria-label="Open menu"><Menu size={18} /></Button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6">{children}</main>
    </div>
  );
}
