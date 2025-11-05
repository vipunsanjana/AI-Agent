import { useState } from "react";
import axios from "axios";

export const useAgentStart = () => {
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);
  const [startMessage, setStartMessage] = useState<string | null>(null);

  const startAgent = async () => {
    setStarting(true);
    setStartError(null);

    try {
      const res = await axios.get("http://localhost:8000/agent/start");
      setStartMessage(res.data.message || "Agent started successfully!");
    } catch (err: any) {
      console.error("Failed to start agent:", err);
      setStartError(err.message || "Failed to start agent");
    } finally {
      setStarting(false);
    }
  };

  return { startAgent, starting, startError, startMessage };
};
