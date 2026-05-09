export type AgentStatus =
  | "approved"
  | "ready"
  | "prepared"
  | "running"
  | "waiting"
  | "blocked";

export type OperatorName = "Codex" | "Claude Code" | "CEO";

export type AgentRun = {
  slug: string;
  name: string;
  operator: OperatorName;
  status: AgentStatus;
  qualityScore?: number;
  updatedAt: string;
  outputPath: string;
  nextCommand?: string;
};

export type Deliverable = {
  label: string;
  path: string;
  owner: OperatorName;
};

export type TimelineItem = {
  label: string;
  at: string;
  status: AgentStatus;
};

export type AgencyProject = {
  id: string;
  client: string;
  industry: string;
  status: AgentStatus;
  statusLabel: string;
  qaScore: number;
  progress: number;
  startedAt: string;
  updatedAt: string;
  n8nEvent: string;
  nextAction: string;
  budgetRange: string;
  activeAgents: number;
  agents: AgentRun[];
  deliverables: Deliverable[];
  timeline: TimelineItem[];
};

export const projects: AgencyProject[] = [
  {
    id: "2026-05_Restaurant_Demo",
    client: "Restaurant Demo",
    industry: "Hospitality operations",
    status: "ready",
    statusLabel: "Ready for delivery",
    qaScore: 8.4,
    progress: 100,
    startedAt: "2026-05-09",
    updatedAt: "2026-05-09",
    n8nEvent: "delivery.ready",
    nextAction: "CEO delivery review",
    budgetRange: "EUR 3k-5k MVP",
    activeAgents: 8,
    agents: [
      {
        slug: "orchestrator",
        name: "Orchestrator",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.2,
        updatedAt: "2026-05-09 12:02",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/orchestrator",
        nextCommand: "python3 execution/agency.py next 2026-05_Restaurant_Demo",
      },
      {
        slug: "eval-agent",
        name: "Eval Agent",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.7,
        updatedAt: "2026-05-09 12:18",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/eval-agent/evaluation.json",
      },
      {
        slug: "bd-agent",
        name: "BD Agent",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.5,
        updatedAt: "2026-05-09 12:30",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/bd-agent/proposal.md",
      },
      {
        slug: "backend-agent",
        name: "Backend Agent",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.1,
        updatedAt: "2026-05-09 12:44",
        outputPath:
          "projects/2026-05_Restaurant_Demo/outputs/backend-agent/implementation-report.json",
      },
      {
        slug: "frontend-agent",
        name: "Frontend Agent",
        operator: "Claude Code",
        status: "approved",
        qualityScore: 8.0,
        updatedAt: "2026-05-09 13:05",
        outputPath:
          "projects/2026-05_Restaurant_Demo/outputs/frontend-agent/implementation-report.json",
      },
      {
        slug: "ops-agent",
        name: "Ops Agent",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.6,
        updatedAt: "2026-05-09 13:21",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/ops-agent/sop.md",
      },
      {
        slug: "marketing-agent",
        name: "Marketing Agent",
        operator: "Claude Code",
        status: "approved",
        qualityScore: 8.4,
        updatedAt: "2026-05-09 13:40",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/marketing-agent/content.json",
      },
      {
        slug: "client-success-agent",
        name: "Client Success",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.8,
        updatedAt: "2026-05-09 13:55",
        outputPath:
          "projects/2026-05_Restaurant_Demo/outputs/client-success-agent/client-success.json",
      },
      {
        slug: "qa-agent",
        name: "QA Agent",
        operator: "Codex",
        status: "approved",
        qualityScore: 8.4,
        updatedAt: "2026-05-09 14:10",
        outputPath: "projects/2026-05_Restaurant_Demo/outputs/qa-agent/qa-report.json",
      },
    ],
    deliverables: [
      {
        label: "Client handover",
        path: "projects/2026-05_Restaurant_Demo/delivery/handover.md",
        owner: "Codex",
      },
      {
        label: "QA evidence",
        path: "projects/2026-05_Restaurant_Demo/delivery/qa-evidence.md",
        owner: "Codex",
      },
      {
        label: "Proposal",
        path: "projects/2026-05_Restaurant_Demo/outputs/bd-agent/proposal.md",
        owner: "Codex",
      },
    ],
    timeline: [
      { label: "Project created", at: "2026-05-09 11:50", status: "approved" },
      { label: "Agent outputs validated", at: "2026-05-09 13:55", status: "approved" },
      { label: "QA approved with notes", at: "2026-05-09 14:10", status: "approved" },
      { label: "Delivery packet ready", at: "2026-05-09 14:16", status: "ready" },
    ],
  },
];

export const operatorQueue = [
  {
    label: "Import n8n webhook",
    owner: "CEO" as OperatorName,
    command:
      "Import infrastructure/n8n/workflows/agency-orchestrator-webhook.json in n8n Cloud",
  },
  {
    label: "Dry-run Supabase sync",
    owner: "Codex" as OperatorName,
    command: "python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo",
  },
  {
    label: "Live Supabase apply",
    owner: "Codex" as OperatorName,
    command:
      "SUPABASE_URL=... SUPABASE_SCHEMA=agency SUPABASE_SERVICE_KEY=... python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo --apply",
  },
];

export function getProject(projectId: string) {
  return projects.find((project) => project.id === projectId);
}

export function getDashboardMetrics() {
  const activeProjects = projects.length;
  const readyProjects = projects.filter((project) => project.status === "ready").length;
  const averageQa =
    projects.reduce((total, project) => total + project.qaScore, 0) /
    Math.max(projects.length, 1);
  const blockedRuns = projects.reduce(
    (total, project) =>
      total + project.agents.filter((agent) => agent.status === "blocked").length,
    0,
  );

  return {
    activeProjects,
    readyProjects,
    averageQa,
    blockedRuns,
  };
}
