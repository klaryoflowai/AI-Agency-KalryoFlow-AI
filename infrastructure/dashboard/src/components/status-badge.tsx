import type { AgentStatus } from "@/lib/agency-data";

const statusStyles: Record<AgentStatus, string> = {
  approved: "border-emerald-200 bg-emerald-50 text-emerald-800",
  ready: "border-teal-200 bg-teal-50 text-teal-800",
  prepared: "border-violet-200 bg-violet-50 text-violet-800",
  running: "border-amber-200 bg-amber-50 text-amber-800",
  waiting: "border-stone-200 bg-stone-50 text-stone-700",
  blocked: "border-red-200 bg-red-50 text-red-800",
};

export function StatusBadge({
  status,
  label,
}: {
  status: AgentStatus;
  label?: string;
}) {
  return (
    <span
      className={`inline-flex h-7 items-center rounded-md border px-2.5 text-xs font-medium ${statusStyles[status]}`}
    >
      {label ?? status}
    </span>
  );
}
