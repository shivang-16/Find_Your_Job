export const scrapeData = async() => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/scrape`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        //   credentials: "include",
          cache: "force-cache",
          next: {
            tags: ["userData"],
          },
        }
      );
  
      const data = await res.json();
  
      return data;
    } catch (error: unknown) {
      if (error instanceof Error) {
        throw new Error(`Error Scraping: ${error.message}`);
      } else {
        throw new Error(
          "An unknown error occurred while scraping"
        );
      }
    }
}


export const getJobData = async(page: number, portal: string, title: string) => {
    console.log("hitting this", page)
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/jobs/get?page=${page}&source=${portal}&title=${title}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        //   credentials: "include",
          cache: "no-cache",
          next: {
            tags: ["userData"],
          },
        }
      );
  
      console.log('here')
      const data = await res.json();
      console.log("here is the jobs" ,data)
  
      return data;
    } catch (error: unknown) {
      if (error instanceof Error) {
        throw new Error(`Error in fetching job data: ${error.message}`);
      } else {
        throw new Error(
          "An unknown error occurred while fetching job data"
        );
      }
    }
}