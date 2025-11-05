import {
  CheckCircle2,
  Circle,
  XCircle,
  Loader2,
  ExternalLink,
  Clock,
} from 'lucide-react';
import { CronJobStatus, JobStep } from '../types';

interface JobStatusCardProps {
  job: CronJobStatus;
}

const jobSteps: JobStep[] = [
  { key: 'user_logged', label: 'User Logged In', description: 'User authentication successful' },
  { key: 'image_generated', label: 'Image Generated', description: 'AI image created successfully' },
  { key: 'content_generated', label: 'Content Generated', description: 'Post content created' },
  { key: 'db_saved', label: 'Database Saved', description: 'Details saved to database' },
  { key: 'uploaded_to_linkedin', label: 'Uploaded to LinkedIn', description: 'Published to LinkedIn profile' },
];

export const JobStatusCard = ({ job }: JobStatusCardProps) => {
  const getStepIcon = (completed: boolean, isRunning: boolean, hasFailed: boolean) => {
    if (hasFailed) return <XCircle className="w-6 h-6 text-red-500" />;
    if (completed) return <CheckCircle2 className="w-6 h-6 text-green-500" />;
    if (isRunning) return <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />;
    return <Circle className="w-6 h-6 text-slate-300" />;
  };

  const getStepStatus = (completed: boolean, isRunning: boolean, hasFailed: boolean) => {
    if (hasFailed) return { text: 'Failed', color: 'text-red-600 bg-red-50 border-red-200' };
    if (completed) return { text: 'Success', color: 'text-green-600 bg-green-50 border-green-200' };
    if (isRunning) return { text: 'Running', color: 'text-blue-600 bg-blue-50 border-blue-200' };
    return { text: 'Pending', color: 'text-slate-600 bg-slate-50 border-slate-200' };
  };

  const getStatusColor = (status: CronJobStatus['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500/10 text-green-600 border-green-500/20';
      case 'running':
        return 'bg-blue-500/10 text-blue-600 border-blue-500/20';
      case 'failed':
        return 'bg-red-500/10 text-red-600 border-red-500/20';
      default:
        return 'bg-slate-500/10 text-slate-600 border-slate-500/20';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const currentStepIndex = jobSteps.findIndex((step) => !job[step.key]);
  const isJobRunning = job.status === 'running';
  const hasFailed = job.status === 'failed';

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden transition-all duration-200 hover:shadow-md">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-50 to-slate-100 px-6 py-4 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-slate-600" />
            <div>
              <h3 className="font-semibold text-slate-900">
                Job #{job.id.slice(0, 8)}
              </h3>
              <p className="text-sm text-slate-600">{formatDate(job.created_at)}</p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(job.status)}`}
          >
            {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
          </span>
        </div>
      </div>

      {/* Steps */}
      <div className="p-6">
        <div className="space-y-4">
          {jobSteps.map((step, index) => {
            const isCompleted = !!job[step.key];
            const isCurrentStep = isJobRunning && index === currentStepIndex;
            const isStepFailed = hasFailed && index === currentStepIndex;
            const stepStatus = getStepStatus(isCompleted, isCurrentStep, isStepFailed);

            return (
              <div
                key={step.key}
                className="flex items-center gap-4 p-4 rounded-xl bg-slate-50 border border-slate-200"
              >
                <div className="flex-shrink-0">
                  {getStepIcon(isCompleted, isCurrentStep, isStepFailed)}
                </div>
                <div className="flex-1 min-w-0">
                  <p
                    className={`font-semibold text-lg ${
                      isCompleted ? 'text-slate-900' : 'text-slate-700'
                    }`}
                  >
                    {step.label}
                  </p>
                  <p className="text-sm text-slate-600 mt-0.5">
                    {step.description}
                  </p>
                </div>
                <div className="flex-shrink-0">
                  <span
                    className={`px-3 py-1.5 rounded-lg text-sm font-semibold border ${stepStatus.color}`}
                  >
                    {stepStatus.text}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Error message */}
        {job.error_message && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm font-medium text-red-800">Error Message:</p>
            <p className="text-sm text-red-600 mt-1">{job.error_message}</p>
          </div>
        )}

        {/* LinkedIn link */}
        {job.linkedin_post_url && job.uploaded_to_linkedin && (
          <div className="mt-4 pt-4 border-t border-slate-200">
            <a
              href={job.linkedin_post_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium transition-colors"
            >
              View LinkedIn Post
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        )}
      </div>
    </div>
  );
};
