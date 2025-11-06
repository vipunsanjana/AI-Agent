import { useEffect, useState } from "react";
import axios from "axios";
import { CronJobStatus } from "../types";

const API_URL = import.meta.env.VITE_API_URL

export const useCronJobStatus = (userId: string | null) => {
  const [jobs, setJobs] = useState<CronJobStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;

    const fetchJobs = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await axios.get(`${API_URL}/agent/summary`);
        const { total_completed, total_failed } = res.data;

        // Convert totals into array of "summary jobs"
        const summaryJobs: CronJobStatus[] = [];

        for (let i = 0; i < total_completed; i++) {
          summaryJobs.push({
            id: `completed-${i + 1}`,
            status: "completed",
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            user_id: userId,
            user_logged: true,
          });
        }

        for (let i = 0; i < total_failed; i++) {
          summaryJobs.push({
            id: `failed-${i + 1}`,
            status: "failed",
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            user_id: userId,
            user_logged: true,
          });
        }

        setJobs(summaryJobs);
      } catch (err: any) {
        console.error("Failed to fetch jobs:", err);
        setError(err.message || "Failed to fetch jobs");
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, [userId]);

  return { jobs, loading, error };
};
