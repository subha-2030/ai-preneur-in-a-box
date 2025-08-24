"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { useRouter } from 'next/navigation';

// Define the type for a briefing object based on the backend model
interface Briefing {
  _id: string;
  client_name: string;
  meeting_date: string;
  summary: string;
  gaps: string[];
  external_research: { title: string; link: string; snippet: string }[];
  suggested_questions: string[];
  created_at: string;
}

export default function BriefingDetailPage() {
  const [briefing, setBriefing] = useState<Briefing | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const params = useParams();
  const briefingId = params.briefingId as string;
  const router = useRouter();

  useEffect(() => {
    if (briefingId) {
      const fetchBriefing = async () => {
        try {
          const response = await api.get(`/briefings/${briefingId}`);
          setBriefing(response);
        } catch (err) {
          setError('Failed to fetch briefing.');
          console.error(err);
        } finally {
          setLoading(false);
        }
      };

      fetchBriefing();
    }
  }, [briefingId]);

  const handleDelete = async () => {
    try {
      await api.delete(`/briefings/${briefingId}`);
      router.push('/briefings');
    } catch (err) {
      setError('Failed to delete briefing.');
      console.error(err);
    }
  };

  const handleFeedback = async (feedback: string) => {
    try {
      await api.post(`/briefings/${briefingId}/feedback`, { feedback });
      alert('Thank you for your feedback!');
    } catch (err) {
      alert('Failed to submit feedback.');
      console.error(err);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!briefing) {
    return <div>Briefing not found.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-3xl">{briefing.client_name}</CardTitle>
              <CardDescription>
                Meeting on {new Date(briefing.meeting_date).toLocaleDateString()}
              </CardDescription>
            </div>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive">Delete</Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete this briefing.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold mb-2">Summary</h2>
            <p className="text-gray-700">{briefing.summary}</p>
          </div>
          <div>
            <h2 className="text-xl font-semibold mb-2">Identified Gaps</h2>
            <ul className="list-disc list-inside space-y-1">
              {briefing.gaps.map((gap, index) => (
                <li key={index}>{gap}</li>
              ))}</ul>
          </div>
          <div>
            <h2 className="text-xl font-semibold mb-2">External Research</h2>
            <div className="space-y-4">
              {briefing.external_research.map((item, index) => (
                <div key={index} className="border p-4 rounded-lg">
                  <h3 className="font-semibold">
                    <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                      {item.title}
                    </a>
                  </h3>
                  <p className="text-sm text-gray-600">{item.snippet}</p>
                </div>
              ))}</div>
          </div>
          <div>
            <h2 className="text-xl font-semibold mb-2">Suggested Talking Points & Questions</h2>
            <ul className="list-disc list-inside space-y-1">
              {briefing.suggested_questions.map((question, index) => (
                <li key={index}>{question}</li>
              ))}</ul>
          </div>
          <div className="border-t pt-4 mt-6">
            <h2 className="text-lg font-semibold mb-2">Was this briefing helpful?</h2>
            <div className="flex space-x-2">
              <Button variant="outline" onClick={() => handleFeedback('helpful')}>👍 Helpful</Button>
              <Button variant="outline" onClick={() => handleFeedback('not_helpful')}>👎 Not Helpful</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}