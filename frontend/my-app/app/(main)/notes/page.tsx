"use client";
import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../../../components/ui/table";
import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { createNote, getNotes, Note, Client, getClients } from '../../../lib/api';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../../../components/ui/dialog";
import { Textarea } from "../../../components/ui/textarea";

const NotesPage = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newNote, setNewNote] = useState({
    client_name: '',
    meeting_date: new Date().toISOString().split('T'),
    content: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [fetchedNotes, fetchedClients] = await Promise.all([
          getNotes(),
          getClients(),
        ]);
        setNotes(fetchedNotes);
        setClients(fetchedClients);
        if (fetchedClients.length > 0) {
          setNewNote((prev) => ({
            ...prev,
            client_name: fetchedClients.name,
          }));
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
  }, []);

  const filteredNotes = notes.filter((note) =>
    note.client_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCreateNote = async () => {
    try {
      await createNote({
        ...newNote,
        meeting_date: new Date(newNote.meeting_date).toISOString(),
      });
      setIsDialogOpen(false);
      const fetchedNotes = await getNotes();
      setNotes(fetchedNotes);
    } catch (error) {
      console.error('Failed to create note:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Meeting Notes</h1>
        <div className="flex items-center space-x-2">
          <Input
            type="text"
            placeholder="Search notes..."
            value={searchTerm}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchTerm(e.target.value)}
            className="max-w-sm"
          />
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>Create New Note</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Note</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <label>Client</label>
                  <select
                    value={newNote.client_name}
                    onChange={(e) => setNewNote({ ...newNote, client_name: e.target.value })}
                    className="w-full p-2 border rounded"
                  >
                    {clients.map(client => (
                      <option key={client.id} value={client.name}>{client.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label>Meeting Date</label>
                  <Input
                    type="date"
                    value={newNote.meeting_date}
                    onChange={(e) => setNewNote({ ...newNote, meeting_date: e.target.value })}
                  />
                </div>
                <div>
                  <label>Content</label>
                  <Textarea
                    value={newNote.content}
                    onChange={(e) => setNewNote({ ...newNote, content: e.target.value })}
                  />
                </div>
                <Button onClick={handleCreateNote}>Save Note</Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      <Table>
        <TableCaption>A list of your recent meeting notes.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Client</TableHead>
            <TableHead>Meeting Date</TableHead>
            <TableHead>Content</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredNotes.map((note) => (
            <TableRow key={note.id}>
              <TableCell>{note.client_name}</TableCell>
              <TableCell>{new Date(note.meeting_date).toLocaleDateString()}</TableCell>
              <TableCell>{note.content.substring(0, 100)}...</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default NotesPage;