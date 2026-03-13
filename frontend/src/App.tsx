import './index.css'

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/80">
              <span className="text-sm font-semibold">AI</span>
            </div>
            <div>
              <h1 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-300">
                CI/CD Monitor
              </h1>
              <p className="text-xs text-slate-500">
                AI-powered pipeline insights
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8 space-y-6">
        <section className="grid gap-4 md:grid-cols-3">
          <div className="col-span-2 rounded-xl border border-slate-800 bg-slate-900/40 p-4">
            <h2 className="text-sm font-medium text-slate-200">
              Overview
            </h2>
            <p className="mt-1 text-xs text-slate-400">
              Connect your CI/CD pipelines to see real-time status, historical
              performance, and AI-detected anomalies.
            </p>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-3">
                <p className="text-[11px] uppercase tracking-wide text-slate-500">
                  Total runs
                </p>
                <p className="mt-1 text-2xl font-semibold text-slate-50">0</p>
              </div>
              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-3">
                <p className="text-[11px] uppercase tracking-wide text-slate-500">
                  Success rate
                </p>
                <p className="mt-1 text-2xl font-semibold text-emerald-400">
                  0%
                </p>
              </div>
              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-3">
                <p className="text-[11px] uppercase tracking-wide text-slate-500">
                  Active anomalies
                </p>
                <p className="mt-1 text-2xl font-semibold text-amber-400">0</p>
              </div>
            </div>
          </div>

          <aside className="space-y-3">
            <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
              <h2 className="text-sm font-medium text-slate-200">
                Getting started
              </h2>
              <ol className="mt-3 space-y-2 text-xs text-slate-400">
                <li>1. Run the backend and frontend via Docker.</li>
                <li>2. Create a pipeline in the dashboard.</li>
                <li>3. Point your CI/CD webhook to the events endpoint.</li>
              </ol>
            </div>
          </aside>
        </section>
      </main>
    </div>
  )
}

export default App
