"use client";
import { useEffect, useState } from "react";
import { getUpcomingMeetings } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { CalendarDays, Clock, ExternalLink, Users, MapPin } from "lucide-react";

interface Meeting {
  id: string;
  summary: string;
  start: {
    dateTime: string;
  };
  htmlLink: string;
  attendees?: Array<{ email: string }>;
  location?: string;
  description?: string;
}

export default function DashboardPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMeetings = async () => {
      try {
        const upcomingMeetings = await getUpcomingMeetings();
        setMeetings(upcomingMeetings);
      } catch (error) {
        console.error("Error fetching upcoming meetings:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchMeetings();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    const isToday = date.toDateString() === today.toDateString();
    const isTomorrow = date.toDateString() === tomorrow.toDateString();

    if (isToday) {
      return `Today, ${date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })}`;
    } else if (isTomorrow) {
      return `Tomorrow, ${date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })}`;
    } else {
      return date.toLocaleDateString([], {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    }
  };

  const getTimeUntilMeeting = (dateString: string) => {
    const meetingTime = new Date(dateString);
    const now = new Date();
    const diffMs = meetingTime.getTime() - now.getTime();

    if (diffMs < 0) return "Past";

    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    if (diffHours < 1) {
      return `${diffMinutes}m`;
    } else if (diffHours < 24) {
      return `${diffHours}h ${diffMinutes}m`;
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays}d`;
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back! Here&apos;s what&apos;s coming up.
          </p>
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3 mb-6">
            <CalendarDays className="h-6 w-6 text-primary" />
            <h2 className="text-xl font-semibold">Upcoming Meetings</h2>
          </div>

          {/* Loading skeleton */}
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="bg-card border border-border rounded-lg p-6 animate-pulse"
              >
                <div className="h-4 bg-muted rounded w-3/4 mb-3"></div>
                <div className="h-3 bg-muted rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-muted rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back! Here&apos;s what&apos;s coming up.
        </p>
      </div>

      <div className="space-y-6">
        <div className="flex items-center gap-3 mb-6">
          <CalendarDays className="h-6 w-6 text-primary" />
          <h2 className="text-xl font-semibold">Upcoming Meetings</h2>
          <span className="bg-primary/10 text-primary text-xs font-medium px-2 py-1 rounded-full">
            {meetings.length} meeting{meetings.length !== 1 ? "s" : ""}
          </span>
        </div>

        {meetings.length === 0 ? (
          <div className="bg-card border border-border rounded-lg p-8 text-center">
            <CalendarDays className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">
              No upcoming meetings
            </h3>
            <p className="text-muted-foreground">
              You&apos;re all caught up! No meetings scheduled for now.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {meetings.map((meeting) => {
              const timeUntil = getTimeUntilMeeting(meeting.start.dateTime);
              const isUpcoming = timeUntil !== "Past";

              return (
                <div
                  key={meeting.id}
                  className={`bg-card border border-border rounded-lg p-6 transition-all hover:shadow-md hover:border-primary/20 ${
                    !isUpcoming ? "opacity-60" : ""
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="text-lg font-semibold text-foreground truncate">
                          {meeting.summary}
                        </h3>
                        {isUpcoming && (
                          <span className="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 text-xs font-medium px-2 py-1 rounded-full whitespace-nowrap">
                            in {timeUntil}
                          </span>
                        )}
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Clock className="h-4 w-4" />
                          <span>{formatDate(meeting.start.dateTime)}</span>
                        </div>

                        {meeting.attendees && meeting.attendees.length > 0 && (
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Users className="h-4 w-4" />
                            <span>
                              {meeting.attendees.length} attendee
                              {meeting.attendees.length !== 1 ? "s" : ""}
                            </span>
                          </div>
                        )}

                        {meeting.location && (
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <MapPin className="h-4 w-4" />
                            <span className="truncate">{meeting.location}</span>
                          </div>
                        )}
                      </div>

                      {meeting.description && (
                        <p className="text-sm text-muted-foreground mt-3 line-clamp-2">
                          {meeting.description}
                        </p>
                      )}
                    </div>

                    <div className="flex-shrink-0">
                      <Button
                        variant="outline"
                        size="sm"
                        asChild
                        className="gap-2"
                      >
                        <a
                          href={meeting.htmlLink}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <ExternalLink className="h-4 w-4" />
                          Join
                        </a>
                      </Button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
