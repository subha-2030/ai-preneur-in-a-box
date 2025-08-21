"use client";
import { useEffect, useState } from "react";
import { getUpcomingMeetings } from "@/lib/api";

export default function DashboardPage() {
  const [meetings, setMeetings] = useState<any[]>([]);

  useEffect(() => {
    const fetchMeetings = async () => {
      try {
        const upcomingMeetings = await getUpcomingMeetings();
        setMeetings(upcomingMeetings);
      } catch (error) {
        console.error("Error fetching upcoming meetings:", error);
      }
    };

    fetchMeetings();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Upcoming Meetings</h1>
      <ul>
        {meetings.map((meeting: any) => (
          <li key={meeting.id} className="mb-2">
            <a href={meeting.htmlLink} target="_blank" rel="noopener noreferrer">
              {meeting.summary} - {new Date(meeting.start.dateTime).toLocaleString()}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}