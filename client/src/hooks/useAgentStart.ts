import { useState } from "react";
import axios from "axios";
import { AgentStartResponse } from "../types";

const API_URL = import.meta.env.VITE_API_URL

export const useAgentStart = () => {
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);
  const [startMessage, setStartMessage] = useState<string | null>(null);

  // ✅ Strongly typed return
  const startAgent = async (niche: string): Promise<AgentStartResponse> => {
    setStarting(true);
    setStartError(null);
    setStartMessage(null);

    try {
      const res = await axios.post(`${API_URL}/agent/start`, { niche });

      const response: AgentStartResponse = {
        success: res.status === 200,
        status: "completed",
        message: res.data?.message || "Agent started successfully!",
      };

      setStartMessage(response.message);
      return response;
    } catch (err: any) {
      console.error("Failed to start agent:", err);

      const response: AgentStartResponse = {
        success: false,
        status: "failed",
        message: err.response?.data?.message || err.message || "Failed to start agent",
      };

      setStartError(response.message);
      return response;
    } finally {
      setStarting(false);
    }
  };

  return { startAgent, starting, startError, startMessage };
};
