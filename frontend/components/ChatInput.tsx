"use client";

import { useState } from "react";

type ChatInputProps = {
  onSend: (question: string) => void;
};

const SUGGESTIONS = [
  "Ventes totales par région",
  "Top 5 des produits les plus rentables",
  "Évolution des ventes en 2023",
  "Quelle catégorie génère le plus de pertes ?",
];

export default function ChatInput({ onSend }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (question.trim() === "") return;

    onSend(question);
    setQuestion("");
  }

  function handleSuggestionClick(suggestion: string) {
    onSend(suggestion);
  }

  return (
    <div className="border-t border-black/10 p-4">
      <div className="flex gap-2 flex-wrap mb-3">
        {SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => handleSuggestionClick(suggestion)}
            className="text-sm border border-black/10 rounded-full px-3 py-1.5 text-black/70 hover:bg-black/5 transition"
          >
            {suggestion}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Posez une question sur vos données de ventes..."
          rows={1}
          className="flex-1 resize-none rounded-lg border border-black/10 p-3 outline-none focus:border-accent"
        />
        <button
          type="submit"
          className="bg-accent text-white rounded-lg px-5 font-medium hover:opacity-90 transition"
        >
          Envoyer
        </button>
      </form>
    </div>
  );
}