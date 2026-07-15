import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const crowdData = [{ zone: "A", wait: 8, density: 42 }, { zone: "B", wait: 28, density: 88 }, { zone: "C", wait: 15, density: 61 }, { zone: "D", wait: 6, density: 35 }];
const sustainData = [{ name: "Water", value: 82 }, { name: "Energy", value: 64 }, { name: "Waste", value: 51 }, { name: "Carbon", value: 47 }];

export function CrowdChart() {
  return <ResponsiveContainer width="100%" height={220}><BarChart data={crowdData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="zone" /><YAxis /><Tooltip /><Bar dataKey="wait" fill="#0F766E" name="Wait minutes" /><Bar dataKey="density" fill="#F5C451" name="Density" /></BarChart></ResponsiveContainer>;
}

export function SustainabilityChart() {
  return <ResponsiveContainer width="100%" height={220}><AreaChart data={sustainData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Area type="monotone" dataKey="value" stroke="#0F766E" fill="#99F6E4" /></AreaChart></ResponsiveContainer>;
}
