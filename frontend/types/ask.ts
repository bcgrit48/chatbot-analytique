export type AskResponse = {
  question: string;
  generated_sql: string;
  is_valid: boolean;
  rejection_reason: string | null;
  result: Record<string, unknown>[] | null;
  chart: Record<string, unknown> | null;
  answer: string | null;
};