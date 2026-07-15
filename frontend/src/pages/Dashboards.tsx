import { useQuery } from "@tanstack/react-query";
import type { ElementType } from "react";
import { AlertTriangle, Car, ClipboardCheck, Droplets, Flame, MapPin, ParkingCircle, Shield, Ticket, Users, Utensils, Zap } from "lucide-react";
import { AIAssistant } from "../components/AIAssistant";
import { CrowdChart, SustainabilityChart } from "../components/Charts";
import { OperationsMap } from "../components/OperationsMap";
import { Card } from "../components/ui/Card";
import { api, demo } from "../lib/api";

function Metric({ label, value, icon: Icon }: { label: string; value: string; icon: ElementType }) {
  return <div className="metric"><div className="flex items-center justify-between"><p className="text-sm text-slate-600 dark:text-slate-300">{label}</p><Icon size={18} className="text-fifa" /></div><p className="mt-2 text-2xl font-black">{value}</p></div>;
}

function CrowdPanel() {
  const { data, isError } = useQuery({ queryKey: ["crowd"], queryFn: () => api<typeof demo.crowd>("/dashboards/crowd"), retry: false });
  const rows = data ?? demo.crowd;
  return <Card><div className="mb-3 flex items-center justify-between"><h2 className="text-lg font-bold">Crowd Intelligence</h2>{isError && <span className="text-xs text-amber-700">demo data</span>}</div><CrowdChart /><div className="mt-3 space-y-2">{rows.map(item => <div key={item.zone} className="rounded-md bg-slate-50 p-3 dark:bg-slate-950"><p className="font-semibold">{item.zone} - {item.risk}</p><p className="text-sm text-slate-600 dark:text-slate-300">{item.ai_summary} {item.alternative_route}</p></div>)}</div></Card>;
}

function SustainabilityPanel() {
  const { data } = useQuery({ queryKey: ["sustainability"], queryFn: () => api<typeof demo.sustainability>("/dashboards/sustainability"), retry: false });
  const value = data ?? demo.sustainability;
  return <Card><h2 className="text-lg font-bold">Sustainability</h2><SustainabilityChart /><div className="grid gap-2 sm:grid-cols-4"><Metric label="Water" value={`${Math.round(value.water_liters / 1000)}k L`} icon={Droplets} /><Metric label="Energy" value={`${Math.round(value.electricity_kwh)} kWh`} icon={Zap} /><Metric label="Waste" value={`${Math.round(value.waste_kg)} kg`} icon={ClipboardCheck} /><Metric label="Carbon" value={`${Math.round(value.carbon_kg)} kg`} icon={Flame} /></div><ul className="mt-3 list-disc pl-5 text-sm text-slate-600 dark:text-slate-300">{value.recommendations.map(item => <li key={item}>{item}</li>)}</ul></Card>;
}

export function FanDashboard() {
  return (
    <div className="space-y-5">
      <div><h1 className="text-3xl font-black">Fan Dashboard</h1><p className="text-slate-600 dark:text-slate-300">Tickets, navigation, crowd conditions, parking, food, alerts, language, and voice support.</p></div>
      <div className="grid gap-3 md:grid-cols-4"><Metric label="Upcoming match" value="USA vs CAN" icon={Ticket} /><Metric label="Seat" value="B-21-18" icon={MapPin} /><Metric label="Parking" value="Lot C 128" icon={ParkingCircle} /><Metric label="Food queue" value="7 min" icon={Utensils} /></div>
      <div className="grid gap-5 lg:grid-cols-[1.2fr_.8fr]"><Card><h2 className="mb-3 text-lg font-bold">Seat Finder and Accessible Navigation</h2><OperationsMap /></Card><AIAssistant /></div>
      <CrowdPanel />
    </div>
  );
}

export function VolunteerDashboard() {
  return (
    <div className="space-y-5">
      <div><h1 className="text-3xl font-black">Volunteer Dashboard</h1><p className="text-slate-600 dark:text-slate-300">Assigned zone, current tasks, shift schedule, crowd alerts, and incident reporting.</p></div>
      <div className="grid gap-3 md:grid-cols-4"><Metric label="Assigned zone" value="Gate B" icon={MapPin} /><Metric label="Open tasks" value="6" icon={ClipboardCheck} /><Metric label="Shift" value="14:00-22:00" icon={Users} /><Metric label="Alerts" value="2" icon={AlertTriangle} /></div>
      <div className="grid gap-5 lg:grid-cols-2"><Card><h2 className="mb-3 text-lg font-bold">Current Tasks</h2>{["Redirect fans to Gate D", "Assist wheelchair route near elevator E2", "Report queue spillback every 10 minutes"].map(task => <label key={task} className="mt-2 flex items-center gap-2 rounded-md bg-slate-50 p-3 dark:bg-slate-950"><input type="checkbox" />{task}</label>)}</Card><AIAssistant /></div>
      <CrowdPanel />
    </div>
  );
}

export function OrganizerDashboard() {
  return (
    <div className="space-y-5">
      <div><h1 className="text-3xl font-black">Organizer Command Center</h1><p className="text-slate-600 dark:text-slate-300">Crowd analytics, queue length, heat maps, incidents, transport, food, utilities, and AI recommendations.</p></div>
      <div className="grid gap-3 md:grid-cols-4"><Metric label="Gate B wait" value="28 min" icon={Users} /><Metric label="Open incidents" value="3" icon={Shield} /><Metric label="Metro ETA" value="4 min" icon={Car} /><Metric label="Energy load" value="64%" icon={Zap} /></div>
      <div className="grid gap-5 lg:grid-cols-[1fr_1fr]"><CrowdPanel /><Card><h2 className="mb-3 text-lg font-bold">Heat Map and Volunteer Locations</h2><OperationsMap /></Card></div>
      <div className="grid gap-5 lg:grid-cols-2"><SustainabilityPanel /><AIAssistant /></div>
    </div>
  );
}

export function AdminDashboard() {
  return (
    <div className="space-y-5">
      <div><h1 className="text-3xl font-black">Admin Dashboard</h1><p className="text-slate-600 dark:text-slate-300">Manage users, stadium, volunteers, matches, tickets, gates, analytics, and audit logs.</p></div>
      <div className="grid gap-3 md:grid-cols-4"><Metric label="Users" value="18,420" icon={Users} /><Metric label="Matches" value="8" icon={Ticket} /><Metric label="Gates" value="12" icon={MapPin} /><Metric label="Audit events" value="1,204" icon={Shield} /></div>
      <div className="grid gap-5 lg:grid-cols-2"><Card><h2 className="text-lg font-bold">Management Console</h2>{["Users", "Stadium", "Volunteers", "Matches", "Tickets", "Gates"].map(item => <button key={item} className="mt-2 w-full rounded-md border border-slate-200 p-3 text-left font-semibold hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-950">{item}</button>)}</Card><Card><h2 className="text-lg font-bold">Audit Logs</h2>{["admin.updated_gate_capacity", "organizer.created_incident", "volunteer.completed_task", "fan.changed_language"].map(item => <p key={item} className="mt-2 rounded-md bg-slate-50 p-3 font-mono text-sm dark:bg-slate-950">{item}</p>)}</Card></div>
    </div>
  );
}
