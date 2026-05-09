import {
  Database,
  LayoutDashboard,
  PlusCircle,
  ShieldCheck,
  Workflow,
} from "lucide-react";
import Link from "next/link";

const navItems = [
  { href: "/", label: "Projects", icon: LayoutDashboard },
  { href: "/projects/new", label: "New project", icon: PlusCircle },
  { href: "/#operator-queue", label: "Operator queue", icon: Workflow },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#f6f7f4] text-[#17211d]">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-[#dfe3dc] bg-white/88 px-4 py-5 xl:block">
        <Link href="/" className="flex h-11 items-center gap-3 rounded-lg px-2">
          <span className="flex size-9 items-center justify-center rounded-lg bg-[#17211d] text-white">
            <ShieldCheck className="size-5" aria-hidden="true" />
          </span>
          <span>
            <span className="block text-sm font-semibold">KlaryoFlow AI</span>
            <span className="block text-xs text-[#697469]">Agency cockpit</span>
          </span>
        </Link>

        <nav className="mt-8 grid gap-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex h-10 items-center gap-3 rounded-lg px-3 text-sm font-medium text-[#4e5a4f] transition hover:bg-[#eef2ec] hover:text-[#17211d]"
            >
              <item.icon className="size-4" aria-hidden="true" />
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="absolute bottom-5 left-4 right-4 rounded-lg border border-[#dfe3dc] bg-[#f8faf7] p-4">
          <div className="flex items-center gap-2 text-xs font-semibold text-[#697469]">
            <Database className="size-4" aria-hidden="true" />
            Data mode
          </div>
          <p className="mt-2 text-sm font-medium text-[#17211d]">Local demo data</p>
          <p className="mt-1 text-xs leading-5 text-[#697469]">
            Supabase-ready, no live write until service keys are configured.
          </p>
        </div>
      </aside>

      <header className="sticky top-0 z-20 border-b border-[#dfe3dc] bg-white/92 px-4 py-3 backdrop-blur xl:hidden">
        <div className="flex items-center justify-between gap-3">
          <Link href="/" className="flex min-w-0 items-center gap-2">
            <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-[#17211d] text-white">
              <ShieldCheck className="size-5" aria-hidden="true" />
            </span>
            <span className="min-w-0 truncate text-sm font-semibold">KlaryoFlow AI</span>
          </Link>
          <Link
            href="/projects/new"
            className="inline-flex h-10 items-center justify-center rounded-lg bg-[#17211d] px-3 text-sm font-semibold text-white"
          >
            <PlusCircle className="mr-2 size-4" aria-hidden="true" />
            New
          </Link>
        </div>
      </header>

      <main className="xl:pl-64">
        <div className="mx-auto min-h-screen w-full max-w-[1500px] px-4 py-5 sm:px-6 lg:px-8 xl:py-8">
          {children}
        </div>
      </main>
    </div>
  );
}
