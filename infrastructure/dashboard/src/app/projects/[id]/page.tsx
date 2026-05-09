import {
  ArrowLeft,
  CheckCircle2,
  FileText,
  Gauge,
  ShieldCheck,
  TerminalSquare,
  Workflow,
} from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { StatusBadge } from "@/components/status-badge";
import { getProject } from "@/lib/agency-data";

type ProjectPageProps = {
  params: Promise<{ id: string }>;
};

export default async function ProjectPage({ params }: ProjectPageProps) {
  const { id } = await params;
  const project = getProject(id);

  if (!project) {
    notFound();
  }

  return (
    <div className="grid gap-6">
      <section className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <Link
            href="/"
            className="inline-flex h-9 items-center gap-2 rounded-lg border border-[#cfd7cf] bg-white px-3 text-sm font-semibold text-[#344036] hover:bg-[#f8faf7]"
          >
            <ArrowLeft className="size-4" aria-hidden="true" />
            Projects
          </Link>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <h1 className="text-3xl font-semibold text-[#17211d] sm:text-4xl">
              {project.client}
            </h1>
            <StatusBadge status={project.status} label={project.statusLabel} />
          </div>
          <p className="mt-2 font-mono text-sm text-[#697469]">{project.id}</p>
        </div>
        <div className="rounded-lg border border-[#dfe3dc] bg-white px-4 py-3">
          <p className="text-sm text-[#697469]">Next action</p>
          <p className="mt-1 text-sm font-semibold text-[#17211d]">{project.nextAction}</p>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <article className="rounded-lg border border-[#dfe3dc] bg-white p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
            <Gauge className="size-4 text-[#0f766e]" aria-hidden="true" />
            Progress
          </div>
          <p className="mt-3 text-2xl font-semibold text-[#17211d]">{project.progress}%</p>
          <div className="mt-3 h-2 rounded-full bg-[#edf0eb]">
            <div
              className="h-2 rounded-full bg-[#0f766e]"
              style={{ width: `${project.progress}%` }}
            />
          </div>
        </article>
        <article className="rounded-lg border border-[#dfe3dc] bg-white p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
            <ShieldCheck className="size-4 text-[#0f766e]" aria-hidden="true" />
            QA score
          </div>
          <p className="mt-3 text-2xl font-semibold text-[#17211d]">
            {project.qaScore.toFixed(1)}
          </p>
          <p className="mt-2 text-sm text-[#697469]">Release gate passed</p>
        </article>
        <article className="rounded-lg border border-[#dfe3dc] bg-white p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
            <Workflow className="size-4 text-[#7c3aed]" aria-hidden="true" />
            n8n event
          </div>
          <p className="mt-3 font-mono text-sm font-semibold text-[#17211d]">
            {project.n8nEvent}
          </p>
          <p className="mt-2 text-sm text-[#697469]">Webhook-safe state</p>
        </article>
        <article className="rounded-lg border border-[#dfe3dc] bg-white p-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
            <CheckCircle2 className="size-4 text-[#b7791f]" aria-hidden="true" />
            Agents
          </div>
          <p className="mt-3 text-2xl font-semibold text-[#17211d]">
            {project.activeAgents}
          </p>
          <p className="mt-2 text-sm text-[#697469]">Validated outputs</p>
        </article>
      </section>

      <section className="grid gap-4 xl:grid-cols-[minmax(0,1.25fr)_minmax(340px,0.75fr)]">
        <div>
          <h2 className="mb-3 text-lg font-semibold text-[#17211d]">Agent runs</h2>
          <div className="overflow-x-auto rounded-lg border border-[#dfe3dc] bg-white">
            <table className="w-full border-collapse text-left">
              <thead className="bg-[#f8faf7] text-xs font-semibold text-[#697469]">
                <tr>
                  <th className="px-4 py-3">Agent</th>
                  <th className="px-4 py-3">Operator</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Score</th>
                  <th className="px-4 py-3">Output</th>
                </tr>
              </thead>
              <tbody>
                {project.agents.map((agent) => (
                  <tr key={agent.slug} className="border-t border-[#edf0eb]">
                    <td className="px-4 py-4 text-sm font-semibold text-[#17211d]">
                      {agent.name}
                    </td>
                    <td className="px-4 py-4 text-sm text-[#4e5a4f]">{agent.operator}</td>
                    <td className="px-4 py-4">
                      <StatusBadge status={agent.status} />
                    </td>
                    <td className="px-4 py-4 text-sm font-semibold text-[#17211d]">
                      {agent.qualityScore?.toFixed(1) ?? "-"}
                    </td>
                    <td className="min-w-80 px-4 py-4">
                      <code className="block overflow-x-auto rounded-md bg-[#f8faf7] px-2 py-1 font-mono text-xs text-[#4e5a4f]">
                        {agent.outputPath}
                      </code>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="grid content-start gap-4">
          <section className="rounded-lg border border-[#dfe3dc] bg-white p-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-[#344036]">
              <FileText className="size-4 text-[#0f766e]" aria-hidden="true" />
              Delivery files
            </div>
            <div className="mt-4 grid gap-3">
              {project.deliverables.map((deliverable) => (
                <article
                  key={deliverable.path}
                  className="rounded-lg border border-[#edf0eb] bg-[#f8faf7] p-3"
                >
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-semibold text-[#17211d]">
                      {deliverable.label}
                    </p>
                    <span className="rounded-md bg-white px-2 py-1 text-xs font-semibold text-[#4e5a4f]">
                      {deliverable.owner}
                    </span>
                  </div>
                  <code className="mt-3 block overflow-x-auto font-mono text-xs leading-5 text-[#697469]">
                    {deliverable.path}
                  </code>
                </article>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-[#dfe3dc] bg-[#17211d] p-4 text-white">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <TerminalSquare className="size-4 text-[#f2c94c]" aria-hidden="true" />
              Next command
            </div>
            <code className="mt-4 block overflow-x-auto rounded-lg border border-white/10 bg-black/22 p-3 font-mono text-xs leading-6 text-[#e8f0e7]">
              python3 execution/agency.py sync-supabase {project.id}
            </code>
          </section>
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-[#17211d]">Timeline</h2>
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {project.timeline.map((item) => (
            <article
              key={`${item.label}-${item.at}`}
              className="rounded-lg border border-[#dfe3dc] bg-white p-4"
            >
              <StatusBadge status={item.status} />
              <p className="mt-3 text-sm font-semibold text-[#17211d]">{item.label}</p>
              <p className="mt-2 text-sm text-[#697469]">{item.at}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
