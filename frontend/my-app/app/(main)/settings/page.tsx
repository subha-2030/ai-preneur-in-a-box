"use client";
import { getGoogleAuthorizationUrl, handleGoogleCallback } from "@/lib/api";
import { useEffect } from "react";

export default function SettingsPage() {
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const state = urlParams.get("state");

    if (code && state) {
      handleGoogleCallback(code, state)
        .then(() => {
          // Redirect to a success page or show a success message
          window.location.href = "/settings";
        })
        .catch((error) => {
          console.error("Error handling Google callback:", error);
        });
    }
  }, []);

  const handleConnectGoogleCalendar = async () => {
    try {
      const { authorization_url } = await getGoogleAuthorizationUrl();
      window.location.href = authorization_url;
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