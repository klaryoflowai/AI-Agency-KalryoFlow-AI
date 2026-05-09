import {
  ArrowUpRight,
  CheckCircle2,
  CircleAlert,
  Clock3,
  ShieldCheck,
  TerminalSquare,
  UsersRound,
  Workflow,
  type LucideIcon,
} from "lucide-react";
import Link from "next/link";
import { StatusBadge } from "@/components/status-badge";
import {
  getDashboardMetrics,
  operatorQueue,
  projects,
  type AgencyProject,
} from "@/lib/agency-data";

function MetricCard({
  label,
  value,
  detail,
  icon: Icon,
}: {
  label: string;
  value: string;
  detail: string;
  icon: LucideIcon;
}) {
  return (
    <article className="rounded-lg border border-[#dfe3dc] bg-white p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-[#697469]">{label}</p>
          <p className="mt-2 text-2xl font-semibold text-[#17211d]">{value}</p>
        </div>
        <span className="flex size-10 items-center justify-center rounded-lg bg-[#eef2ec] text-[#344036]">
          <Icon className="size-5" aria-hidden={true} />
        </span>
      </div>
      <p className="mt-3 text-sm text-[#697469]">{detail}</p>
    </article>
  );
}

function ProjectRow({ project }: { project: AgencyProject }) {
  return (
    <tr className="border-t border-[#edf0eb]">
      <td className="min-w-64 px-4 py-4">
        <Link href={`/projects/${project.id}`} className="group inline-flex items-center gap-2">
          <span>
            <span className="block text-sm font-semibold text-[#17211d]">
              {project.client}
            </span>
            <span className="mt-1 block font-mono text-xs text-[#697469]">
              {project.id}
            </span>
          </span>
          <ArrowUpRight
            className="size-4 text-[#697469] transition group-hover:text-[#0f766e]"
            aria-hidden="true"
          />
        </Link>
      </td>
      <td className="px-4 py-4">
        <StatusBadge status={project.status} label={project.statusLabel} />
      </td>
      <td className="px-4 py-4 text-sm font-semibold text-[#17211d]">
        {project.qaScore.toFixed(1)}
      </td>
      <td className="px-4 py-4 text-sm text-[#4e5a4f]">{project.nextAction}</td>
      <td className="px-4 py-4 text-sm text-[#697469]">{project.updatedAt}</td>
    </tr>
  );
}

export default function Home() {
  const metrics = getDashboardMetrics();
  const primaryProject = projects[0];

  return (
    <div className="grid gap-6">
      <section className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <p className="text-sm font-semibold text-[#0f766e]">Zero-API MVP</p>
          <h1 className="mt-2 text-3xl font-semibold text-[#17211d] sm:text-4xl">
            Agency operations
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-[#697469]">
            Codex owns backend, orchestration, Supabase, and QA. Claude Code owns
            frontend execution and simple sub-agent tasks. QA closes every client
            delivery.
          </p>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row">
          <Link
            href="/projects/new"
            className="inline-flex h-11 items-center justify-center gap-2 rounded-lg bg-[#17211d] px-4 text-sm font-semibold text-white transition hover:bg-[#263229]"
          >
            <UsersRound className="size-4" aria-hidden="true" />
            New project
          </Link>
          <a
            href="#operator-queue"
            className="inline-flex h-11 items-center justify-center gap-2 rounded-lg border border-[#cfd7cf] bg-white px-4 text-sm font-semibold text-[#344036] transition hover:bg-[#f8faf7]"
          >
            <TerminalSquare className="size-4" aria-hidden="true" />
            Operator queue
          </a>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Active projects"
          value={String(metrics.activeProjects)}
          detail="Local workspace projects tracked"
          icon={Workflow}
        />
        <MetricCard
          label="Ready"
          value={String(metrics.readyProjects)}
          detail="Delivery packets waiting for CEO"
          icon={CheckCircle2}
        />
        <MetricCard
          label="QA average"
          value={metrics.averageQa.toFixed(1)}
          detail="Minimum release gate is 7.0"
          icon={ShieldCheck}
        />
        <MetricCard
          label="Blocked runs"
          value={String(metrics.blockedRuns)}
          detail="No active blockers in demo pipeline"
          icon={CircleAlert}
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.4fr)_minmax(320px,0.6fr)]">
        <div>
          <div className="mb-3 flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-[#17211d]">Project pipeline</h2>
            <span className="text-sm text-[#697469]">{primaryProject.progress}% complete</span>
          </div>
          <div className="grid gap-3 md:grid-cols-2 2xl:grid-cols-3">
            {primaryProject.agents.map((agent) => (
              <article
                key={agent.slug}
                className="rounded-lg border border-[#dfe3dc] bg-white p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-semibold text-[#17211d]">
                      {agent.name}
                    </p>
                    <p className="mt-1 text-xs text-[#697469]">{agent.operator}</p>
                  </div>
                  <StatusBadge status={agent.status} />
                </div>
                <div className="mt-4 flex items-end justify-between gap-3">
                  <div>
                    <p className="text-xs text-[#697469]">Quality</p>
                    <p className="mt-1 text-xl font-semibold text-[#17211d]">
                      {agent.qualityScore?.toFixed(1) ?? "-"}
                    </p>
                  </div>
                  <p className="text-right text-xs text-[#697469]">{agent.updatedAt}</p>
                </div>
              </article>
            ))}
          </div>
        </div>

        <section id="operator-queue" className="rounded-lg border border-[#dfe3dc] bg-white p-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-[#17211d]">Operator queue</h2>
            <Clock3 className="size-5 text-[#b7791f]" aria-hidden="true" />
          </div>
          <div className="mt-4 grid gap-3">
            {operatorQueue.map((item) => (
              <article
                key={item.label}
                className="rounded-lg border border-[#edf0eb] bg-[#f8faf7] p-3"
              >
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-semibold text-[#17211d]">{item.label}</p>
                  <span className="rounded-md bg-white px-2 py-1 text-xs font-semibold text-[#4e5a4f]">
                    {item.owner}
                  </span>
                </div>
                <code className="mt-3 block overflow-x-auto rounded-lg bg-[#17211d] p-3 font-mono text-xs leading-6 text-[#e8f0e7]">
                  {item.command}
                </code>
              </article>
            ))}
          </div>
        </section>
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="text-lg font-semibold text-[#17211d]">Projects</h2>
          <Link
            href="/projects/new"
            className="text-sm font-semibold text-[#0f766e] hover:text-[#0f4f4a]"
          >
            Add project
          </Link>
        </div>
        <div className="overflow-x-auto rounded-lg border border-[#dfe3dc] bg-white">
          <table className="w-full border-collapse text-left">
            <thead className="bg-[#f8faf7] text-xs font-semibold text-[#697469]">
              <tr>
                <th className="px-4 py-3">Project</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">QA</th>
                <th className="px-4 py-3">Next action</th>
                <th className="px-4 py-3">Updated</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <ProjectRow key={project.id} project={project} />
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
