import { notifications } from "@mantine/notifications";
import { makeAutoObservable, runInAction } from "mobx";

import { abortJob, fetchJob, fetchJobs } from "../api";
import { IFetchJobsParams, IJobsInfo } from "../api/types";

import {
  AbortStatus,
  FilterJobs,
  Job,
  JobsTimeStatistics,
  PagedJobs,
  Statistics,
} from "./models";

export class RootStore {
  tableJobs: PagedJobs = new PagedJobs();
  isLoading: boolean = false;
  filterJobs: FilterJobs = new FilterJobs();
  functions: string[] = [];
  statistics: Statistics = new Statistics();
  statistics_hourly: JobsTimeStatistics[] = [];

  constructor() {
    makeAutoObservable(this);
  }

  async loadData() {
    this.isLoading = true;
    this.tableJobs.toggle_jobs = [];
    const params: IFetchJobsParams = {
      limit: this.tableJobs.limit,
      offset: this.tableJobs.offset,
      sortBy: this.tableJobs.sort_by,
      sortOrder: this.tableJobs.sort_order,
    };

    if (this.filterJobs.status.length) {
      params.statuses = this.filterJobs.status;
    }

    if (this.filterJobs.search) {
      params.search = this.filterJobs.search;
    }

    if (this.filterJobs.function) {
      params.functionName = this.filterJobs.function;
    }

    try {
      const jobsData: IJobsInfo = await fetchJobs(params);
      runInAction(() => {
        this.tableJobs.items = jobsData.paged_jobs.items.map(
          (jobData) => new Job(jobData),
        );
        this.tableJobs.count = jobsData.paged_jobs.count;
        this.tableJobs.limit = jobsData.paged_jobs.limit;
        this.functions = jobsData.functions;
        this.statistics = jobsData.statistics;
        this.statistics_hourly = jobsData.statistics_hourly;
      });
    } catch (error) {
      console.error("Failed to load data", error);

      const message = error instanceof Error ? error.message : "Unknown error";
      notifications.show({
        title: "Failed to load data",
        message: String(message),
        color: "red",
        autoClose: false,
      });
    } finally {
      this.isLoading = false;
    }
  }

  async loadJob(jobId: string) {
    const newJob = await fetchJob(jobId);
    const job = this.tableJobs.items.find((job) => job.id === jobId);
    if (job) {
      Object.assign(job, newJob);
    }
  }

  async abortJob(jobId: string) {
    const job = this.tableJobs.items.find((job) => job.id === jobId);
    if (!job) {
      return;
    }
    try {
      job.abort_status = AbortStatus.InProgress;
      await abortJob(jobId);
      job.abort_status = AbortStatus.Completed;
      this.loadJob(jobId);
    } catch (error) {
      console.error("Failed to abort job", error);
      job.abort_status = AbortStatus.Failed;
      const message = error instanceof Error ? error.message : "Unknown error";
      notifications.show({
        title: "Failed to abort job",
        message: String(message),
        color: "red",
        autoClose: false,
      });
    }
  }

  clearFilter() {
    this.filterJobs.function = null;
    this.filterJobs.status = [];
    this.filterJobs.search = "";
    this.tableJobs.offset = 0;
    this.tableJobs.sort_by = "enqueue_time";
    this.tableJobs.sort_order = "desc";
    this.loadData();
  }

  setPage(page: number) {
    this.tableJobs.offset = (page - 1) * this.tableJobs.limit;
    this.loadData();
  }

  setSortBy(sortBy: string) {
    if (this.tableJobs.sort_by === sortBy) {
      this.tableJobs.sort_order =
        this.tableJobs.sort_order === "asc" ? "desc" : "asc";
    } else {
      this.tableJobs.sort_order = "desc";
    }
    this.tableJobs.sort_by = sortBy;
    this.setPage(1);
    this.loadData();
  }

  get totalPages() {
    return Math.ceil(this.tableJobs.count / this.tableJobs.limit);
  }

  get currentPage() {
    return Math.ceil(this.tableJobs.offset / this.tableJobs.limit) + 1;
  }

  setFilterFunction(value: string | null) {
    this.filterJobs.function = value;
    this.loadData();
  }

  setFilterStatus(value: string[]) {
    this.filterJobs.status = value;
    this.loadData();
  }

  setFilterSearch(value: string) {
    this.filterJobs.search = value;
  }
}
