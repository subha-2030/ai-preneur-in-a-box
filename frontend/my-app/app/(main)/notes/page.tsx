"use client";
import React, { useState } from 'react';
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
import { createNote } from '../../../lib/api';

const notes = [
  { id: 1, title: "Meeting with Team A", createdAt: "2023-01-10" },
  { id: 2, title: "Project Kickoff", createdAt: "2023-01-12" },
  { id: 3, title: "Design Review", createdAt: "2023-01-15" },
];

const NotesPage = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCreateNote = async () => {
    try {
      const newNote = await createNote({ title: 'New Note', content: 'This is a new note.' });
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
              <TableCell>{note.createdAt}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default NotesPage;