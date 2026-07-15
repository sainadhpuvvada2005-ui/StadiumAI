import React from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./styles.css";
import { AppShell } from "./components/AppShell";
import { AuthProvider } from "./lib/AuthContext";
import { Landing } from "./pages/Landing";
import { AuthPage } from "./pages/AuthPage";
import { FanDashboard, VolunteerDashboard, OrganizerDashboard, AdminDashboard } from "./pages/Dashboards";

const queryClient = new QueryClient();
const router = createBrowserRouter([
  { path: "/", element: <Landing /> },
  { path: "/auth", element: <AuthPage /> },
  { path: "/fan", element: <AppShell role="fan"><FanDashboard /></AppShell> },
  { path: "/volunteer", element: <AppShell role="volunteer"><VolunteerDashboard /></AppShell> },
  { path: "/organizer", element: <AppShell role="organizer"><OrganizerDashboard /></AppShell> },
  { path: "/admin", element: <AppShell role="admin"><AdminDashboard /></AppShell> }
]);

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
