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
  enqueue_time: Date;
  result: string;
  start_time: Date | null;
  finish_time: Date | null;
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
  statistics_hourly: IJobsTimeStatistics[];
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

export enum ColorStatistics {
  red = "red",
  green = "green",
  gray = "gray",
  orange = "orange",
}

export interface IJobsTimeStatistics {
  date: Date;
  total_created: number;
  total_completed_successfully: number;
  total_failed: number;
  total_in_progress: number;
  color: ColorStatistics;
  color_intensity: number;
}
