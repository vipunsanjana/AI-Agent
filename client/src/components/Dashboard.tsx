import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useCronJobStatus } from '../hooks/useCronJobStatus';
import { useAgentStart } from '../hooks/useAgentStart';
import { JobStatusCard } from './JobStatusCard';
import {
  LogOut,
  Sparkles,
  TrendingUp,
  Activity,
  CheckCircle2,
  Loader2,
  PlayCircle,
} from 'lucide-react';

export const Dashboard = () => {
  const { user, signOut } = useAuth();

  // Fetch jobs from backend
  const { jobs, loading, error } = useCronJobStatus(user?.id || null);

  // Handle Start Agent button
  const { startAgent, starting, startError, startMessage } = useAgentStart();

  // Local UI counters for dynamic job tracking
  const [runningJobs, setRunningJobs] = useState(0);
  const [completedJobs, setCompletedJobs] = useState(0);
  const [failedJobs, setFailedJobs] = useState(0);

  // --- Sync counters from backend ---
  useEffect(() => {
    if (jobs && jobs.length > 0) {
      setCompletedJobs(jobs.filter((j) => j.status === 'completed').length);
      setRunningJobs(jobs.filter((j) => j.status === 'running').length);
      setFailedJobs(jobs.filter((j) => j.status === 'failed').length);
    }
  }, [jobs]);

  // ==============================================================
  // 🔹 Handle Agent Start
  //    1️⃣ Set runningJobs = 1 immediately
  //    2️⃣ Trigger backend automation
  //    3️⃣ When done → update job counters accordingly
  // ==============================================================
  const handleStartAgent = async () => {
    try {
      setRunningJobs(1); // Start indicator immediately
      const response = await startAgent('AI Content');

      // Simulate backend job completion
      if (response?.success || response?.status === 'completed') {
        setRunningJobs(0);
        setCompletedJobs((prev) => prev + 1);
      } else {
        setRunningJobs(0);
        setFailedJobs((prev) => prev + 1);
      }
    } catch (err) {
      console.error('❌ Agent start failed:', err);
      setRunningJobs(0);
      setFailedJobs((prev) => prev + 1);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50">
      {/* Navbar */}
      <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10 backdrop-blur-lg bg-white/95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-500 to-cyan-500 p-2 rounded-xl shadow-md">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">LinkedIn Studio</h1>
                <p className="text-xs text-slate-600">Automated Content Pipeline</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-slate-900">{user?.email}</p>
                <p className="text-xs text-slate-600">OAuth Connected</p>
              </div>
              <button
                onClick={signOut}
                className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors font-medium"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline">Sign Out</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Body */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 mb-2">Workflow Dashboard</h2>
            <p className="text-slate-600">
              Monitor your automated content generation jobs in real-time
            </p>
          </div>

          {/* Start Agent Button */}
          <button
            onClick={handleStartAgent}
            disabled={starting || runningJobs > 0}
            className={`mt-4 sm:mt-0 inline-flex items-center gap-2 px-5 py-2 rounded-xl font-semibold text-white transition-all shadow-md ${
              starting || runningJobs > 0
                ? 'bg-blue-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600'
            }`}
          >
            {starting || runningJobs > 0 ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                {runningJobs > 0 ? 'Running Job...' : 'Starting Agent...'}
              </>
            ) : (
              <>
                <PlayCircle className="w-5 h-5" />
                Start Agent
              </>
            )}
          </button>
        </div>

        {/* Agent Start Feedback */}
        {(startMessage || startError) && (
          <div
            className={`mb-6 p-4 rounded-lg border text-sm font-medium ${
              startError
                ? 'bg-red-50 border-red-200 text-red-700'
                : 'bg-green-50 border-green-200 text-green-700'
            }`}
          >
            {startError ? startError : startMessage}
          </div>
        )}

        {/* Job Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-4">
              <CheckCircle2 className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{completedJobs}</span>
            </div>
            <h3 className="font-semibold text-green-50 mb-1">Completed Jobs</h3>
            <p className="text-sm text-green-100 opacity-90">Successfully published</p>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-4">
              <Activity className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{runningJobs}</span>
            </div>
            <h3 className="font-semibold text-blue-50 mb-1">Running Jobs</h3>
            <p className="text-sm text-blue-100 opacity-90">Currently processing</p>
          </div>

          <div className="bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{completedJobs + failedJobs}</span>
            </div>
            <h3 className="font-semibold text-slate-50 mb-1">Total Jobs</h3>
            <p className="text-sm text-slate-100 opacity-90">{failedJobs} failed attempts</p>
          </div>
        </div>

        {/* Recent Jobs */}
        <div className="mb-6">
          <h3 className="text-xl font-bold text-slate-900 mb-4">Recent Jobs</h3>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-16">
            <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
            <p className="text-slate-600 font-medium">Loading job statuses...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
            <p className="text-red-800 font-medium">Error loading jobs</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="bg-slate-50 border-2 border-dashed border-slate-300 rounded-2xl p-12 text-center">
            <div className="bg-slate-200 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Activity className="w-8 h-8 text-slate-400" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">No jobs yet</h3>
            <p className="text-slate-600">Your automated content jobs will appear here</p>
          </div>
        ) : (
          <div className="space-y-6">
            {jobs.map((job) => (
              <JobStatusCard key={job.id} job={job} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
