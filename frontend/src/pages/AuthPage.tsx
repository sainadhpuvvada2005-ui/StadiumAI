import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { api, RoleName } from "../lib/api";
import { useAuth } from "../lib/AuthContext";

export function AuthPage() {
  const [mode, setMode] = useState<"login" | "register" | "forgot">("login");
  const [role, setRole] = useState<RoleName>("fan");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setSession } = useAuth();
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      const body = Object.fromEntries(form.entries());
      const data = await api<{ access_token: string; role: RoleName }>(mode === "register" ? "/auth/register" : mode === "forgot" ? "/auth/forgot-password" : "/auth/login", { method: "POST", body: JSON.stringify({ ...body, role }) });
      if ("access_token" in data) {
        setSession(data.access_token, data.role);
        navigate(`/${data.role}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    }
  }
  return (
    <main className="grid min-h-screen place-items-center bg-slate-100 px-4 dark:bg-night">
      <Card className="w-full max-w-md">
        <h1 className="text-3xl font-black">STADIUMAI</h1>
        <p className="mt-1 text-slate-600 dark:text-slate-300">Secure access for fans, volunteers, organizers, and admins.</p>
        <div className="mt-5 grid grid-cols-3 gap-2">{(["login", "register", "forgot"] as const).map(item => <Button key={item} onClick={() => setMode(item)} type="button" className={mode === item ? "" : "bg-slate-200 text-slate-900 hover:bg-slate-300 dark:bg-slate-800 dark:text-white"}>{item}</Button>)}</div>
        <form onSubmit={submit} className="mt-5 space-y-3">
          {mode === "register" && <input name="full_name" required minLength={2} className="w-full rounded-md border p-3 dark:border-slate-700 dark:bg-slate-950" placeholder="Full name" />}
          <input name="email" required type="email" className="w-full rounded-md border p-3 dark:border-slate-700 dark:bg-slate-950" placeholder="Email" />
          {mode !== "forgot" && <input name="password" required minLength={10} type="password" className="w-full rounded-md border p-3 dark:border-slate-700 dark:bg-slate-950" placeholder="Password" />}
          {mode === "register" && <select value={role} onChange={e => setRole(e.target.value as RoleName)} className="w-full rounded-md border p-3 dark:border-slate-700 dark:bg-slate-950"><option value="fan">Fan</option><option value="volunteer">Volunteer</option><option value="organizer">Organizer</option><option value="admin">Admin</option></select>}
          {error && <p role="alert" className="rounded-md bg-red-50 p-3 text-red-700">{error}</p>}
          <Button className="w-full" type="submit">{mode === "forgot" ? "Send reset link" : "Continue"}</Button>
          <Button type="button" className="w-full bg-white text-slate-950 ring-1 ring-slate-200 hover:bg-slate-50">Continue with Google</Button>
        </form>
      </Card>
    </main>
  );
}
