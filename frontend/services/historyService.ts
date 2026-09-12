import type { HistoryItem } from "@/types/history";

const API_URL = process.env.API_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_URL;

export async function getHistory(): Promise<HistoryItem[]> {
  const response = await fetch(`${API_URL}/history`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Erreur API: ${response.status}`);
  }

  return response.json();
}