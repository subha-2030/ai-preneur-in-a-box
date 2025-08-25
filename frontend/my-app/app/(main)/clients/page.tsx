"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { getClients, getClientById, updateClient, deleteClient, Client } from "../../../lib/api";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

// A simple pencil icon component
const PencilIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
    <path d="m15 5 4 4" />
  </svg>
);

const TrashIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M3 6h18" />
    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </svg>
);

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [editingClient, setEditingClient] = useState<Client | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteConfirmOpen, setIsDeleteConfirmOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchClients = async () => {
    try {
      console.log("Fetching clients...");
      const data = await getClients();
      console.log("Clients data:", data);
      setClients(data);
    } catch (error) {
      console.error("Error fetching clients:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  const handleEditClick = async (client: Client) => {
    try {
      const fullClient = await getClientById(client.id);
      setEditingClient(fullClient);
      setIsModalOpen(true);
    } catch (error) {
      console.error("Error fetching client details:", error);
    }
  };

  const handleDeleteClick = (client: Client) => {
    setEditingClient(client);
    setIsDeleteConfirmOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!editingClient) return;
    try {
      await deleteClient(editingClient.id);
      setIsDeleteConfirmOpen(false);
      setEditingClient(null);
      fetchClients();
    } catch (error) {
      console.error("Failed to delete client:", error);
    }
  };

  const handleSaveChanges = async () => {
    if (!editingClient) return;

    try {
      await updateClient(editingClient.id, {
        name: editingClient.name,
        description: editingClient.description,
        meetingNotes: editingClient.meetingNotes,
      });
      setIsModalOpen(false);
      setEditingClient(null);
      fetchClients(); // Refresh the client list
    } catch (error) {
      console.error("Failed to update client:", error);
      // Optionally, show an error message to the user
    }
  };

  const handleModalChange = (isOpen: boolean) => {
    setIsModalOpen(isOpen);
    if (!isOpen) {
      setEditingClient(null);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Clients</h1>
        <Link href="/clients/create">
          <Button>Create Client</Button>
        </Link>
      </div>
      <p className="text-center text-gray-500 my-4">
        Coming soon: Lightweight CRM to acquire new clients and notes integration
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {clients.map((client) => (
          <div
            key={client.id}
            className="border p-4 rounded-lg shadow-sm relative"
          >
            <div className="absolute top-2 right-2 flex space-x-2">
              <button
                onClick={() => handleEditClick(client)}
                className="p-1 text-gray-500 hover:text-gray-800"
                aria-label={`Edit ${client.name}`}
              >
                <PencilIcon className="w-5 h-5" />
              </button>
              <button
                onClick={() => handleDeleteClick(client)}
                className="p-1 text-red-500 hover:text-red-800"
                aria-label={`Delete ${client.name}`}
              >
                <TrashIcon className="w-5 h-5" />
              </button>
            </div>
            <h2 className="text-xl font-semibold pr-8">{client.name}</h2>
            <p className="text-gray-600 mt-2">{client.description}</p>
          </div>
        ))}
      </div>

      {editingClient && (
        <Dialog open={isModalOpen} onOpenChange={handleModalChange}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Client</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="name" className="text-right">
                  Name
                </Label>
                <Input
                  id="name"
                  value={editingClient.name}
                  onChange={(e) =>
                    setEditingClient({ ...editingClient, name: e.target.value })
                  }
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="description" className="text-right">
                  Description
                </Label>
                <Textarea
                  id="description"
                  value={editingClient.description}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      description: e.target.value,
                    })
                  }
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="meetingNotes" className="text-right">
                  Meeting Notes
                </Label>
                <Textarea
                  id="meetingNotes"
                  value={editingClient.meetingNotes || ''}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      meetingNotes: e.target.value,
                    })
                  }
                  className="col-span-3"
                  rows={6}
                />
              </div>
            </div>
            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline">Cancel</Button>
              </DialogClose>
              <Button onClick={handleSaveChanges}>Save Changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}

      {editingClient && (
        <Dialog open={isDeleteConfirmOpen} onOpenChange={setIsDeleteConfirmOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Delete Client</DialogTitle>
            </DialogHeader>
            <p>Are you sure you want to delete {editingClient.name}?</p>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsDeleteConfirmOpen(false)}>
                Cancel
              </Button>
              <Button variant="destructive" onClick={handleConfirmDelete}>
                Delete
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}