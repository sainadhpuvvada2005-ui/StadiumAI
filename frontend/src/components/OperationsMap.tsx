import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export function OperationsMap() {
  const center: [number, number] = [25.958, -80.239];
  return (
    <div className="h-80 overflow-hidden rounded-lg border border-slate-200 dark:border-slate-800" aria-label="Interactive stadium operations map">
      <MapContainer center={center} zoom={15} className="h-full w-full">
        <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={center}><Popup>Command Center</Popup></Marker>
        <Marker position={[25.961, -80.236]}><Popup>Gate B congestion rising</Popup></Marker>
        <Marker position={[25.955, -80.241]}><Popup>Accessible route to Exit D</Popup></Marker>
      </MapContainer>
    </div>
  );
}
