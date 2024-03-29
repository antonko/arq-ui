import { IFetchJobsParams, IJob, IJobsInfo } from "./types";

function joinPathsSafely(basePath: string, relativePath: string): string {
  const trimmedBasePath = basePath.endsWith('/') ? basePath.slice(0, -1) : basePath;
  const trimmedRelativePath = relativePath.startsWith('/') ? relativePath.slice(1) : relativePath;
  return `${trimmedBasePath}/${trimmedRelativePath}`;
}

/**
 * Fetches jobs from the API based on the specified parameters.
 */
export function fetchJobs(params: IFetchJobsParams = {}): Promise<IJobsInfo> {
  
  const jobsUrl = joinPathsSafely(import.meta.env.VITE_API_HOST, "jobs");

  const queryParams = new URLSearchParams();

  if (params.limit !== undefined)
    queryParams.append("limit", params.limit.toString());
  if (params.offset !== undefined)
    queryParams.append("offset", params.offset.toString());
  if (params.sortBy !== undefined && params.sortBy !== "")
    queryParams.append("sort_by", params.sortBy);
  if (params.sortOrder !== undefined && params.sortOrder !== "")
    queryParams.append("sort_order", params.sortOrder);
  if (params.statuses?.length) {
    for (const status of params.statuses) {
      queryParams.append("statuses", status);
    }
  }
  if (params.success !== undefined)
    queryParams.append("success", params.success.toString());
  if (params.functionName !== undefined && params.functionName !== "")
    queryParams.append("function", params.functionName);
  if (params.search !== undefined && params.search !== "")
    queryParams.append("search", params.search);

  const url = `${jobsUrl}?${queryParams.toString()}`;

  return fetch(url).then(async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.text || "Unknown error");
    }
    return data as IJobsInfo;
  });
}

export function abortJob(jobId: string): Promise<void> {
  const jobsUrl = joinPathsSafely(import.meta.env.VITE_API_HOST, "jobs");
  const url = `${jobsUrl}/${jobId}`;

  return fetch(url, { method: "DELETE" }).then(async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.text || "Unknown error");
    }
  });
}

export function fetchJob(jobId: string): Promise<IJob> {
  const jobsUrl = joinPathsSafely(import.meta.env.VITE_API_HOST, "jobs");
  const url = `${jobsUrl}/${jobId}`;

  return fetch(url).then(async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.text || "Unknown error");
    }
    return data;
  });
}
