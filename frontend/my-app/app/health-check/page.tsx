"use client";

import { useEffect, useState } from "react";

export default function HealthCheckPage() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/health`
        );
        const data = await res.json();
        setStatus(data.status);
      } catch (error) {
        console.error("Error fetching health check:", error);
        setStatus("error");
      }
    };

    fetchHealth();
  }, []);

  return (
    <div>
      <h1>Backend Health Check</h1>
      <p>
        Status: <span>{status}</span>
      </p>
    </div>
  );
}