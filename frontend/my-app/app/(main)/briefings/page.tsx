"use client";

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import Link from 'next/link';
import { Input } from '@/components/ui/input';
import { Trash2 } from 'lucide-react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

// Define the type for a briefing object based on the backend model
interface Briefing {
  _id: string;
  client_name: string;
  meeting_date: string;
  summary: string;
  created_at: string;
}

export default function BriefingsPage() {
  const [briefings, setBriefings] = useState<Briefing[]>([]);
  const [filteredBriefings, setFilteredBriefings] = useState<Briefing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [briefingToDelete, setBriefingToDelete] = useState<Briefing | null>(null);

  const handleUpdateBriefings = async () => {
    try {
      await api.post('/briefings/update', {});
      fetchBriefings(); // Refresh the list
    } catch (err) {
      setError('Failed to update briefings.');
      console.error(err);
    }
  };

  const fetchBriefings = async () => {
    try {
      setLoading(true);
      const response = await api.get('/briefings');
      const data = response || [];
      setBriefings(data);
      setFilteredBriefings(data);
    } catch (err) {
      setError('Failed to fetch briefings.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBriefings();
  }, []);

  useEffect(() => {
    const results = briefings.filter(briefing =>
      briefing.client_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredBriefings(results);
  }, [searchTerm, briefings]);

  const handleDelete = async () => {
    if (!briefingToDelete) return;

    try {
      await api.delete(`/briefings/${briefingToDelete._id}`);
      const updatedBriefings = briefings.filter(b => b._id !== briefingToDelete._id);
      setBriefings(updatedBriefings);
      setFilteredBriefings(updatedBriefings);
      setBriefingToDelete(null); // Close the dialog
    } catch (err) {
      setError('Failed to delete briefing.');
      console.error(err);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Research Briefings</CardTitle>
            <Button onClick={handleUpdateBriefings}>Update Research Briefings</Button>
          </div>
          <p className="text-sm text-gray-500">
            Here are the AI-generated briefings for your upcoming meetings.
          </p>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <Input
              placeholder="Search by client name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Client Name</TableHead>
                <TableHead>Meeting Date</TableHead>
                <TableHead>Generated On</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredBriefings.length > 0 ? (
                filteredBriefings.map((briefing) => (
                  <TableRow key={briefing._id}>
                    <TableCell>
                      <Link href={`/briefings/${briefing._id}`} target="_blank">
                        {briefing.client_name}
                      </Link>
                    </TableCell>
                    <TableCell>
                      {new Date(briefing.meeting_date).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      {new Date(briefing.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Button variant="outline" size="sm" onClick={() => window.open(`/briefings/${briefing._id}`, "_blank")}>
                          View
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button variant="destructive" size="sm" onClick={() => setBriefingToDelete(briefing)}>
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                              <AlertDialogDescription>
                                This action cannot be undone. This will permanently delete the briefing.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel onClick={() => setBriefingToDelete(null)}>Cancel</AlertDialogCancel>
                              <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="text-center">
                    No briefings found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}