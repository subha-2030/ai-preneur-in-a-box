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
import { createNote, getNotes, Note } from '../../../lib/api';

const NotesPage = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const fetchedNotes = await getNotes();
        setNotes(fetchedNotes);
      } catch (error) {
        console.error('Failed to fetch notes:', error);
      }
    };

    fetchNotes();
  }, []);

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCreateNote = async () => {
    try {
      const newNote = await createNote({ title: 'New Note', content: 'This is a new note.', createdAt: new Date().toISOString() });
      console.log('Note created successfully:', newNote);
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
          <Button onClick={handleCreateNote}>Create New Note</Button>
        </div>
      </div>
      <Table>
        <TableCaption>A list of your recent meeting notes.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Created At</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredNotes.map((note) => (
            <TableRow key={note.id}>
              <TableCell>{note.title}</TableCell>
              <TableCell>{new Date(note.createdAt).toLocaleDateString()}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default NotesPage;