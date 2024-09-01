import { scrapeData } from "@/actions/data_actions";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Find Your Job",
  description:
    "Single Platform to get job from all platform",
};

export default async function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  const data = scrapeData()
  // console.log(data)

  return (
    <>
        <div className="flex flex-wrap items-center justify-center">
          {children}
        </div>
    
    </>
  );
}
