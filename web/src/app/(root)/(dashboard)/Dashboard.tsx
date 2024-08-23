"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/shared/CustomCard";
import { getJobData } from "@/actions/data_actions";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import debounce from 'lodash.debounce';
import { Input } from "@/components/ui/input";
import Loader from "@/components/shared/Loader";

// Array of job portal names
const jobPortals = [
  "simplyhired",
  "indeed",
  "foundit",
  "linkedin",
  "naukri",
  "internshala",
  "ycombinator",
  "upwork",
  "freelancer",
  "glassdoor"
];

export default function Dashboard() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [selectedPortal, setSelectedPortal] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const fetchJobs = async (page: number, portal: string, query: string) => {
    setLoading(true);
    try {
      console.log(portal, "Fetching jobs from portal with query:", query);
      const data = await getJobData(page, portal, query);
      setJobs((prevJobs) => page === 1 ? data : [...prevJobs, ...data]);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedFetchJobs = useCallback(debounce((page: number, portal: string, query: string) => {
    fetchJobs(page, portal, query);
  }, 300), []);

  useEffect(() => {
    debouncedFetchJobs(page, selectedPortal, searchQuery);
  }, [page, selectedPortal, searchQuery, debouncedFetchJobs]);

  const loadMoreJobs = () => {
    setPage((prevPage) => prevPage + 1);
  };

  return (
    <div className="p-4">
      {loading && (
        <div className="flex justify-center items-center h-32">
          <Loader />
        </div>
      )}

      <Tabs defaultValue="" onValueChange={(value) => {
        setSelectedPortal(value);
        setPage(1);
        setJobs([]);
      }}>
        <TabsList>
          <TabsTrigger value="">All</TabsTrigger>
          {jobPortals.map((portal) => (
            <TabsTrigger key={portal} value={portal}>
              {portal.charAt(0).toUpperCase() + portal.slice(1)}
            </TabsTrigger>
          ))}
        </TabsList>

        <div className="m-4">
          <Input
            type="text"
            placeholder="Search by job title..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setPage(1);
              setJobs([]);
            }}
            className="w-full max-w-md mx-auto"
          />
        </div>

        <div>
          <TabsContent value="">
            {jobs.length > 0 ? (
              jobs.map((job: any) => (
                <Card key={job._id}>
                  <CardHeader>
                    <CardTitle>{job.title || "No Title Available"}</CardTitle>
                    <CardDescription>
                      {job.company_name || "No Company Name Available"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p>Location: {job.job_location || "Location Not Available"}</p>
                    <p>Salary: {job.job_salary || "Salary Not Available"}</p>
                  </CardContent>
                  <CardFooter>
                    <a href={job.job_link} target="_blank" rel="noopener noreferrer">
                      <button className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                        View Job
                      </button>
                    </a>
                    <p className="ml-4">Source: {job.source || "Source Not Available"}</p>
                  </CardFooter>
                </Card>
              ))
            ) : (
              <p>No jobs available.</p>
            )}
          </TabsContent>

          {jobPortals.map((portal) => (
            <TabsContent key={portal} value={portal}>
              {selectedPortal === portal && jobs.length > 0 ? (
                jobs.map((job: any) => (
                  <Card key={job._id}>
                    <CardHeader>
                      <CardTitle>{job.title || "No Title Available"}</CardTitle>
                      <CardDescription>
                        {job.company_name || "No Company Name Available"}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <p>Location: {job.job_location || "Location Not Available"}</p>
                      <p>Salary: {job.job_salary || "Salary Not Available"}</p>
                    </CardContent>
                    <CardFooter>
                      <a href={job.job_link} target="_blank" rel="noopener noreferrer">
                        <button className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                          View Job
                        </button>
                      </a>
                      <p className="ml-4">Source: {job.source || "Source Not Available"}</p>
                    </CardFooter>
                  </Card>
                ))
              ) : (
                <p>No jobs available.</p>
              )}
            </TabsContent>
          ))}
        </div>
      </Tabs>

      <div className="mt-4 text-center">
        <button
          onClick={loadMoreJobs}
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Loading..." : "Next"}
        </button>
      </div>
    </div>
  );
}
