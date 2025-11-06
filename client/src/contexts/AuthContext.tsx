import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import axios from "axios";

const LINKEDIN_CLIENT_ID = "";
const REDIRECT_URI = import.meta.env.VITE_LINKEDIN_REDIRECT_URI;

interface User {
  id: string;
  name: string;
  email: string;
  picture?: string;
  accessToken: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signInWithLinkedIn: () => void;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("linkedin_user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setLoading(false);
      return;
    }

    // Run LinkedIn callback logic only once per session
    if (window.location.pathname === "/auth/callback") {
      const hasRun = sessionStorage.getItem("linkedin_callback_handled");
      if (!hasRun) {
        sessionStorage.setItem("linkedin_callback_handled", "true");
        handleLinkedInCallback();
      } else {
        console.log("⚠️ Skipping duplicate callback handling");
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const signInWithLinkedIn = () => {
    // Reset callback guard before new login attempt
    sessionStorage.removeItem("linkedin_callback_handled");

    const state = crypto.randomUUID();
    localStorage.setItem("linkedin_state", state);

    const scope = "openid profile email";
    const authUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${LINKEDIN_CLIENT_ID}&redirect_uri=${encodeURIComponent(
      REDIRECT_URI
    )}&scope=${encodeURIComponent(scope)}&state=${state}`;

    window.location.href = authUrl;
  };

  const handleLinkedInCallback = async () => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const state = params.get("state");
    const error = params.get("error");

    if (error) {
      alert("LinkedIn login failed: " + error);
      setLoading(false);
      return;
    }

    if (!code || !state) {
      setLoading(false);
      return;
    }

    const savedState = localStorage.getItem("linkedin_state");
    if (state !== savedState) {
      console.error("❌ Invalid OAuth state");
      setLoading(false);
      return;
    }

    try {
      console.log("🔹 Exchanging code for token...");
      const tokenResponse = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/auth/linkedin/token`,
        { code, redirect_uri: REDIRECT_URI }
      );

      const access_token = tokenResponse.data.access_token;
      if (!access_token) throw new Error("No access token returned");

      console.log("✅ Token received. Fetching user info...");
      const userInfo = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/auth/linkedin/me`,
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      const userData: User = {
        id: userInfo.data.sub || userInfo.data.id,
        name: userInfo.data.name,
        email: userInfo.data.email,
        picture: userInfo.data.picture,
        accessToken: access_token,
      };

      setUser(userData);
      localStorage.setItem("linkedin_user", JSON.stringify(userData));
      localStorage.removeItem("linkedin_state");

      // Replace history to remove ?code=... from URL
      window.history.replaceState({}, document.title, "/dashboard");
    } catch (err: any) {
      console.error("❌ LinkedIn login error:", err.response?.data || err.message);
      alert("Login failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const signOut = () => {
    setUser(null);
    localStorage.removeItem("linkedin_user");
    sessionStorage.removeItem("linkedin_callback_handled");
  };

  return (
    <AuthContext.Provider value={{ user, loading, signInWithLinkedIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
