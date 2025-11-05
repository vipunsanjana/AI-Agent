export interface User {
  id: string;
  email: string;
  access_token?: string;
}

// types.ts or hooks/useCronJobStatus.ts
export interface CronJobStatus {
  id: string;
  status: "completed" | "running" | "failed";
  created_at: string;
  updated_at: string;
  user_id?: string;           // optional if you want
  user_logged?: boolean;
  image_generated?: boolean;
  content_generated?: boolean;
  db_saved?: boolean;
  uploaded_to_linkedin?: boolean;
  linkedin_post_url?: string;
  error_message?: string;
}


export interface JobStep {
  key: keyof Pick<CronJobStatus, 'user_logged' | 'image_generated' | 'content_generated' | 'db_saved' | 'uploaded_to_linkedin'>;
  label: string;
  description: string;
}
