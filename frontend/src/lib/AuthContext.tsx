import { createContext, useContext, useMemo, useState } from "react";
import type { RoleName } from "./api";

type AuthContextValue = {
  token: string | null;
  role: RoleName | null;
  setSession: (token: string, role: RoleName) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState(() => localStorage.getItem("stadiumai_token"));
  const [role, setRole] = useState<RoleName | null>(() => localStorage.getItem("stadiumai_role") as RoleName | null);

  const value = useMemo<AuthContextValue>(() => ({
    token,
    role,
    setSession: (nextToken, nextRole) => {
      localStorage.setItem("stadiumai_token", nextToken);
      localStorage.setItem("stadiumai_role", nextRole);
      setToken(nextToken);
      setRole(nextRole);
    },
    logout: () => {
      localStorage.removeItem("stadiumai_token");
      localStorage.removeItem("stadiumai_role");
      setToken(null);
      setRole(null);
      window.location.assign("/auth");
    },
  }), [role, token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
