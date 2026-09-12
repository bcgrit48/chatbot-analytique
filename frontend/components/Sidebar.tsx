import { getHistory } from "@/services/historyService";

export default async function Sidebar() {
  const history = await getHistory();

  return (
    <aside className="w-64 h-full border-r border-black/10 flex flex-col p-4">
      <h1 className="font-heading font-bold text-lg text-accent mb-6">
        Chatbot Analytique
      </h1>

      <button className="bg-accent text-white rounded-lg py-2 px-4 font-medium mb-6 hover:opacity-90 transition">
        + Nouvelle question
      </button>

      <div className="flex-1 overflow-y-auto">
        <h2 className="text-xs font-semibold text-black/40 uppercase mb-2">
          Récents
        </h2>
        <ul className="flex flex-col gap-1">
          {history.length === 0 && (
            <li className="text-sm text-black/40 py-2 px-2">
              Aucune question pour le moment. Posez une question pour commencer.
            </li>
          )}
          {history.map((item, index) => (
            <li
              key={index}
              className="text-sm text-black/70 py-2 px-2 rounded hover:bg-black/5 cursor-pointer truncate"
            >
              {item.question}
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}