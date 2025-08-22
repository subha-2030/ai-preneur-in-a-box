'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
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
} from '@/components/ui/alert-dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import { getNoteById, updateNote, deleteNote, Note } from '@/lib/api';
 
const formSchema = z.object({
  content: z.string().min(1, {
    message: 'Note content cannot be empty.',
  }),
});
 
const NoteDetailPage = () => {
  const { noteId } = useParams();
  const router = useRouter();
  const [note, setNote] = useState<Note | null>(null);
 
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      content: '',
    },
  });
 
  useEffect(() => {
    const fetchNote = async () => {
      if (noteId) {
        try {
          const fetchedNote = await getNoteById(Number(noteId));
          setNote(fetchedNote);
          form.reset({ content: fetchedNote.content });
        } catch (error) {
          console.error('Failed to fetch note', error);
        }
      }
    };
    fetchNote();
  }, [noteId, form]);
 
  async function onSubmit(values: z.infer<typeof formSchema>) {
    if (note) {
      try {
        await updateNote(note.id, { content: values.content });
        router.push('/notes');
      } catch (error) {
        console.error('Failed to update note', error);
      }
    }
  }
 
  async function handleDelete() {
    if (note) {
      try {
        await deleteNote(note.id);
        router.push('/notes');
      } catch (error) {
        console.error('Failed to delete note', error);
      }
    }
  }
 
  if (!note) {
    return <div>Loading...</div>;
  }
 
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Edit Note</h1>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="content"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Note Content</FormLabel>
                <FormControl>
                  <Textarea placeholder="Write your note here..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="flex space-x-2">
            <Button type="submit">Save Changes</Button>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive">Delete Note</Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete
                    your note.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete}>
                    Continue
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </form>
      </Form>
    </div>
  );
};
 
export default NoteDetailPage;