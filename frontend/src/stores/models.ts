import { makeAutoObservable } from "mobx";

export class Job {
  id: string = "";
  status: string = "";
  success: boolean = false;
  enqueue_time: string = "";
  result: string = "";
  start_time: string = "";
  finish_time: string = "";
  queue_name: string = "";
  execution_duration: number = 0;
  function: string = "";
  args: string = "";
  kwargs: string = "";
  job_try: number = 0;

  constructor() {
    makeAutoObservable(this);
  }
}

export class PagedJobs {
  items: Array<Job> = [];
  limit: number = 50;
  count: number = 0;
  offset: number = 0;
  sort_by: string = "enqueue_time";
  sort_order: string = "desc";

  constructor() {
    makeAutoObservable(this);
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
