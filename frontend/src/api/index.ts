import { IFetchJobsParams, IJobsInfo } from "./types";

/**
 * Fetches jobs from the API based on the specified parameters.
 */
export function fetchJobs(params: IFetchJobsParams = {}): Promise<IJobsInfo> {
  const jobsUrl = new URL("jobs", import.meta.env.VITE_API_HOST).toString();

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
