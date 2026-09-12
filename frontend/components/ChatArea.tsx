"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import MessageList from "@/components/MessageList";
import ChatInput from "@/components/ChatInput";
import { askQuestion } from "@/services/askService";

export type Message = {
  role: "user" | "assistant";
  content: string;
  chart?: Record<string, unknown> | null;
};

export default function ChatArea() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  async function handleSend(question: string) {
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setIsLoading(true);

    try {
      const response = await askQuestion(question);

      const assistantContent = response.is_valid
        ? response.answer ?? "Aucune réponse générée."
        : `Requête rejetée : ${response.rejection_reason}`;

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: assistantContent, chart: response.chart },
      ]);

      if (response.is_valid) {
        router.refresh();
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Une erreur est survenue. Réessaie." },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex flex-col flex-1 h-full">
      <MessageList messages={messages} isLoading={isLoading} />
      <ChatInput onSend={handleSend} />
    </div>
  );
}