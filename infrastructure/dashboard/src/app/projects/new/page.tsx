import { NewProjectForm } from "@/components/new-project-form";

export default function NewProjectPage() {
  return (
    <div className="grid gap-5">
      <section>
        <p className="text-sm font-semibold text-[#0f766e]">Project intake</p>
        <h1 className="mt-2 text-3xl font-semibold text-[#17211d] sm:text-4xl">
          New client project
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-[#697469]">
          Capture the first brief, select the agent set, and prepare the local
          operator commands for Codex.
        </p>
      </section>
      <NewProjectForm />
    </div>
  );
}
