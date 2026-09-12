import type { AskResponse } from "@/types/ask";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function askQuestion(question: string): Promise<AskResponse> {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error(`Erreur API: ${response.status}`);
  }

  const data: AskResponse = await response.json();
  return data;
}