"use client";
import { getGoogleAuthorizationUrl } from "@/lib/api";

export default function SettingsPage() {
  const handleConnectGoogleCalendar = async () => {
    try {
      const { authorization_url } = await getGoogleAuthorizationUrl();
      window.open(authorization_url, "_blank");
    } catch (error) {
      console.error("Error connecting to Google Calendar:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <button
        onClick={handleConnectGoogleCalendar}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Connect Google Calendar
      </button>
    </div>
  );
}