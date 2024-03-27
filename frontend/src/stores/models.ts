import { makeAutoObservable } from "mobx";

export enum AbortStatus {
  NotStarted = "not_started",
  InProgress = "in_progress",
  Completed = "completed",
  Failed = "failed", // Если нужно отслеживать неудачные попытки отмены
}

export class Job {
  id: string = "";
  status: string = "";
  success: boolean = false;
  enqueue_time: Date = new Date(-8640000000000000);
  result: string = "";
  start_time: Date | null = null;
  finish_time: Date | null = null;
  queue_name: string = "";
  execution_duration: number = 0;
  function: string = "";
  args: string = "";
  kwargs: string = "";
  job_try: number = 0;
  abort_status: AbortStatus = AbortStatus.NotStarted;

  constructor(jobData?: Partial<Job>) {
    if (jobData) {
      Object.assign(this, jobData);
    }
    makeAutoObservable(this);
  }

  is_abortable(): boolean {
    return ["queued", "deferred", "in_progress"].includes(this.status);
  }
}

export class PagedJobs {
  items: Array<Job> = [];
  limit: number = 50;
  count: number = 0;
  offset: number = 0;
  sort_by: string = "enqueue_time";
  sort_order: string = "desc";
  toggle_jobs: string[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  setToggleJob(jobId: string) {
    if (this.toggle_jobs.includes(jobId)) {
      this.toggle_jobs = this.toggle_jobs.filter((id) => id !== jobId);
    } else {
      this.toggle_jobs = [...this.toggle_jobs, jobId];
    }
  }
}

export class JobsInfo {
  functions: string[] = [];
  statistics: Statistics = new Statistics();
  paged_jobs: PagedJobs = new PagedJobs();

  constructor() {
    makeAutoObservable(this);
  }
}

export class FilterJobs {
  function: string[] = [];
  status: string[] = [];
  search: string = "";

  constructor() {
    makeAutoObservable(this);
  }
}

export class Statistics {
  total: number = 0;
  completed: number = 0;
  in_progress: number = 0;
  queued: number = 0;
  failed: number = 0;

  constructor() {
    makeAutoObservable(this);
  }
}
