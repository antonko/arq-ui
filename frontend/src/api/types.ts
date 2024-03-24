export interface IFetchJobsParams {
  limit?: number;
  offset?: number;
  sortBy?: string;
  sortOrder?: string;
  statuses?: string[];
  success?: boolean;
  functionName?: string;
  search?: string;
}

export interface IJob {
  id: string;
  status: string;
  success: boolean;
  enqueue_time: string;
  result: string;
  start_time: string;
  finish_time: string;
  queue_name: string;
  execution_duration: number;
  function: string;
  args: string;
  kwargs: string;
  job_try: number;
}

export interface IStatistics {
  total: number;
  completed: number;
  in_progress: number;
  queued: number;
  failed: number;
}

export interface IPagedJobs {
  items: IJob[];
  count: number;
  limit: number;
  offset: number;
}

export interface IJobsInfo {
  paged_jobs: IPagedJobs;
  functions: string[];
  statistics: IStatistics;
}

export interface IDetailItem {
  [key: string]: unknown;
}

export interface IProblemDetail {
  type: string;
  title: string;
  text?: string;
  status: number;
  detail?: IDetailItem[];
}
