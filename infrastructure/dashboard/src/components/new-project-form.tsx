"use client";

import {
  Check,
  Clipboard,
  FileText,
  LayoutDashboard,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";
import { useMemo, useState } from "react";

const defaultAgents = [
  "orchestrator",
  "eval-agent",
  "bd-agent",
  "backend-agent",
  "frontend-agent",
  "ops-agent",
  "qa-agent",
];

const projectTypes = [
  { id: "automation", label: "Automation", icon: Workflow },
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "audit", label: "Audit", icon: FileText },
];

function slugify(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function NewProjectForm() {
  const [clientName, setClientName] = useState("Restaurant Demo");
  const [industry, setIndustry] = useState("Hospitality");
  const [priority, setPriority] = useState("Normal");
  const [projectType, setProjectType] = useState("automation");
  const [brief, setBrief] = useState(
    "Automate order intake, daily operational reports, and client follow-up.",
  );
  const [enabledAgents, setEnabledAgents] = useState(defaultAgents);
  const [copied, setCopied] = useState(false);

  const projectId = useMemo(() => {
    const month = new Date().toISOString().slice(0, 7);
    const slug = slugify(clientName) || "client";
    return `${month}_${slug}`;
  }, [clientName]);

  const operatorPacket = useMemo(
    () =>
      [
        `./new-project.sh ${projectId}`,
        `python3 execution/agency.py prepare ${projectId} orchestrator`,
        `python3 execution/agency.py next ${projectId}`,
        `python3 execution/agency.py sync-supabase ${projectId}`,
      ].join("\n"),
    [projectId],
  );

  async function copyPacket() {
    await navigator.clipboard.writeText(operatorPacket);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  function toggleAgent(agent: string) {
    setEnabledAgents((current) =>
      current.includes(agent)
        ? current.filter((item) => item !== agent)
        : [...current, agent],
    );
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1.15fr)_minmax(360px,0.85fr)]">
      <section className="rounded-lg border border-[#dfe3dc] bg-white p-4 sm:p-6">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="grid gap-2 text-sm font-medium text-[#344036]">
            Client name
            <input
              value={clientName}
              onChange={(event) => setClientName(event.target.value)}
              className="h-11 rounded-lg border border-[#cfd7cf] bg-white px-3 text-sm outline-none transition focus:border-[#0f766e] focus:ring-2 focus:ring-[#99f6e4]"
            />
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#344036]">
            Industry
            <input
              value={industry}
              onChange={(event) => setIndustry(event.target.value)}
              className="h-11 rounded-lg border border-[#cfd7cf] bg-white px-3 text-sm outline-none transition focus:border-[#0f766e] focus:ring-2 focus:ring-[#99f6e4]"
            />
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#344036]">
            Priority
            <select
              value={priority}
              onChange={(event) => setPriority(event.target.value)}
              className="h-11 rounded-lg border border-[#cfd7cf] bg-white px-3 text-sm outline-none transition focus:border-[#0f766e] focus:ring-2 focus:ring-[#99f6e4]"
            >
              <option>Normal</option>
              <option>Fast pilot</option>
              <option>CEO review</option>
            </select>
          </label>
          <label className="grid gap-2 text-sm font-medium text-[#344036]">
            Project ID
            <input
              value={projectId}
              readOnly
              className="h-11 rounded-lg border border-[#dfe3dc] bg-[#f8faf7] px-3 font-mono text-sm text-[#344036]"
            />
          </label>
        </div>

        <div className="mt-5">
          <div className="text-sm font-medium text-[#344036]">Project type</div>
          <div className="mt-2 grid gap-2 sm:grid-cols-3">
            {projectTypes.map((type) => (
              <button
                key={type.id}
                type="button"
                onClick={() => setProjectType(type.id)}
                className={`flex h-12 items-center justify-center gap-2 rounded-lg border px-3 text-sm font-semibold transition ${
                  projectType === type.id
                    ? "border-[#0f766e] bg-[#ecfdf5] text-[#0f4f4a]"
                    : "border-[#dfe3dc] bg-white text-[#4e5a4f] hover:bg-[#f8faf7]"
                }`}
              >
                <type.icon className="size-4" aria-hidden="true" />
                {type.label}
              </button>
            ))}
          </div>
        </div>

        <label className="mt-5 grid gap-2 text-sm font-medium text-[#344036]">
          Brief
          <textarea
            value={brief}
            onChange={(event) => setBrief(event.target.value)}
            rows={8}
            className="min-h-44 resize-y rounded-lg border border-[#cfd7cf] bg-white p-3 text-sm leading-6 outline-none transition focus:border-[#0f766e] focus:ring-2 focus:ring-[#99f6e4]"
          />
        </label>

        <div className="mt-5">
          <div className="flex items-center justify-between gap-3">
            <div className="text-sm font-medium text-[#344036]">Enabled agents</div>
            <span className="text-xs font-medium text-[#697469]">
              {enabledAgents.length} selected
            </span>
          </div>
          <div className="mt-2 grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
            {defaultAgents.map((agent) => {
              const selected = enabledAgents.includes(agent);
              return (
                <button
                  key={agent}
                  type="button"
                  onClick={() => toggleAgent(agent)}
                  className={`flex h-11 items-center justify-between rounded-lg border px-3 text-left text-sm transition ${
                    selected
                      ? "border-[#0f766e] bg-[#ecfdf5] text-[#0f4f4a]"
                      : "border-[#dfe3dc] bg-white text-[#4e5a4f] hover:bg-[#f8faf7]"
                  }`}
                >
                  <span className="truncate font-medium">{agent}</span>
                  {selected ? <Check className="size-4" aria-hidden="true" /> : null}
                </button>
              );
            })}
          </div>
        </div>
      </section>

      <aside className="grid content-start gap-4">
        <section className="rounded-lg border border-[#dfe3dc] bg-[#17211d] p-4 text-white sm:p-5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-sm font-semibold">Operator packet</p>
              <p className="mt-1 text-xs text-[#c9d5ca]">Codex local handoff</p>
            </div>
            <Sparkles className="size-5 text-[#f2c94c]" aria-hidden="true" />
          </div>
          <pre className="mt-4 overflow-x-auto rounded-lg border border-white/10 bg-black/22 p-3 font-mono text-xs leading-6 text-[#e8f0e7]">
            {operatorPacket}
          </pre>
          <button
            type="button"
            onClick={copyPacket}
            className="mt-4 inline-flex h-11 w-full items-center justify-center gap-2 rounded-lg bg-white px-4 text-sm font-semibold text-[#17211d] transition hover:bg-[#eef2ec]"
          >
            {copied ? (
              <Check className="size-4" aria-hidden="true" />
            ) : (
              <Clipboard className="size-4" aria-hidden="true" />
            )}
            {copied ? "Copied" : "Copy commands"}
          </button>
        </section>

        <section className="rounded-lg border border-[#dfe3dc] bg-white p-4 sm:p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
            <ShieldCheck className="size-4 text-[#0f766e]" aria-hidden="true" />
            QA gate
          </div>
          <dl className="mt-4 grid gap-3 text-sm">
            <div className="flex items-center justify-between gap-3">
              <dt className="text-[#697469]">Minimum score</dt>
              <dd className="font-semibold text-[#17211d]">7.0/10</dd>
            </div>
            <div className="flex items-center justify-between gap-3">
              <dt className="text-[#697469]">Priority</dt>
              <dd className="font-semibold text-[#17211d]">{priority}</dd>
            </div>
            <div className="flex items-center justify-between gap-3">
              <dt className="text-[#697469]">Industry</dt>
              <dd className="font-semibold text-[#17211d]">{industry || "TBD"}</dd>
            </div>
          </dl>
        </section>
      </aside>
    </div>
  );
}
