import type { Message } from "@/components/ChatArea";
import ChartRenderer from "@/components/ChartRenderer";

type MessageListProps = {
  messages: Message[];
  isLoading: boolean;
};

export default function MessageList({ messages, isLoading }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-4">
      {messages.length === 0 && (
        <p className="text-black/40 text-center mt-20">
          Posez une question sur vos données de ventes pour commencer.
        </p>
      )}

      {messages.map((message, index) => (
        <div
          key={index}
          className={
            message.role === "user"
              ? "self-end bg-accent text-white rounded-lg px-4 py-2 max-w-lg"
              : "self-start bg-black/5 text-foreground rounded-lg px-4 py-2 max-w-2xl w-full"
          }
        >
          {message.content}
          {message.chart && <ChartRenderer chart={message.chart} />}
        </div>
      ))}

      {isLoading && (
        <div className="self-start bg-black/5 text-black/50 rounded-lg px-4 py-2 max-w-lg">
          En train de réfléchir...
        </div>
      )}
    </div>
  );
}