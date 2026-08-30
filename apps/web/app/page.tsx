import React from 'react';
import Link from 'next/link';

export default function Home() {
  const pipelineSteps = [
    { title: 'WATCH', desc: 'Monitor creators across platform adapters' },
    { title: 'DETECT', desc: 'Deduplicate & capture new posts' },
    { title: 'INGEST', desc: 'Extract media, metadata & transcripts' },
    { title: 'ANALYZE', desc: 'Extract hooks, narrative & mechanisms' },
    { title: 'PATTERN', desc: 'Discover reusable content blueprints' },
    { title: 'PERSONALIZE', desc: 'Transform into original user opportunities' },
    { title: 'SCORE', desc: 'Prioritize by relevance, effort & originality' },
    { title: 'NOTIFY', desc: 'Deliver actionable alerts to Telegram' },
  ];

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-12">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <span className="h-4 w-4 rounded-full bg-blue-500 animate-pulse" />
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-slate-100 bg-clip-text text-transparent">
              CreatorRadar
            </h1>
            <span className="text-xs px-2.5 py-1 rounded-full bg-blue-950 text-blue-400 border border-blue-800 font-mono">
              Phase 1 — Watchlist & Acquisition Active
            </span>
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Open-Source Creator Intelligence & Original Opportunity Generation Platform
          </p>
        </div>

        <div className="flex items-center gap-4">
          <Link
            href="/creators"
            className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs shadow-lg shadow-blue-600/20 transition-all flex items-center gap-2"
          >
            <span>Open Creator Watchlist →</span>
          </Link>
        </div>
      </header>

      {/* Core Principle Banner */}
      <section className="bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950 border border-blue-900/50 rounded-2xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 font-mono text-8xl font-black select-none pointer-events-none">
          INSPIRATION ≠ REPLICATION
        </div>
        <h2 className="text-lg font-semibold text-blue-300 mb-2">Core Product Philosophy</h2>
        <div className="grid md:grid-cols-2 gap-6 text-sm text-slate-300">
          <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800">
            <span className="text-emerald-400 font-semibold block mb-1">What CreatorRadar Does (Inspiration):</span>
            Extracts underlying structural mechanisms — hook types, narrative pacing, emotional triggers, visual structure, and why the content succeeds.
          </div>
          <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800">
            <span className="text-rose-400 font-semibold block mb-1">What CreatorRadar Refuses To Do (Replication):</span>
            Does NOT copy script wording, jokes, framing, or auto-repost content. Translates mechanisms into original user opportunities based on user expertise.
          </div>
        </div>
      </section>

      {/* Core Pipeline Architecture */}
      <section className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-200">Asynchronous Job Pipeline</h2>
          <span className="text-xs text-blue-400 font-mono">Phase 1: WATCH & DETECT Active</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {pipelineSteps.map((step, idx) => (
            <div
              key={step.title}
              className={`bg-slate-900/80 border transition-all rounded-xl p-4 flex flex-col justify-between space-y-2 group ${
                idx < 2 ? 'border-blue-500/80 shadow-md shadow-blue-500/10' : 'border-slate-800'
              }`}
            >
              <div className="flex justify-between items-center text-xs text-slate-500 font-mono">
                <span>0{idx + 1}</span>
                <span className={idx < 2 ? 'text-blue-400 font-semibold' : 'group-hover:text-blue-400'}>
                  {idx < 2 ? 'Active Step' : 'Queue Job'}
                </span>
              </div>
              <div>
                <h3 className="font-bold text-slate-100 group-hover:text-blue-300 transition-colors">
                  {step.title}
                </h3>
                <p className="text-xs text-slate-400 mt-1">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture Abstractions Grid */}
      <section className="grid md:grid-cols-3 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="font-bold text-slate-200 flex items-center justify-between">
            <span>Source Acquisition</span>
            <span className="text-xs px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800 font-mono">
              Provider Capability
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Provider-capability architecture (OfficialMetaProvider, ExternalProvider, MockProvider).
          </p>
          <ul className="text-xs space-y-1.5 text-slate-300 font-mono">
            <li className="flex items-center justify-between">
              <span>OfficialMetaProvider</span>
              <span className="text-slate-500">Business Discovery</span>
            </li>
            <li className="flex items-center justify-between">
              <span>ExternalProvider</span>
              <span className="text-slate-500">Compliant Proxy</span>
            </li>
            <li className="flex items-center justify-between">
              <span>MockProvider</span>
              <span className="text-emerald-400">Deterministic</span>
            </li>
          </ul>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="font-bold text-slate-200 flex items-center justify-between">
            <span>Ingestion Engine</span>
            <span className="text-xs px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800 font-mono">
              Idempotent
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Rate-limit aware, idempotent acquisition pipeline emitting post.detected events.
          </p>
          <ul className="text-xs space-y-1.5 text-slate-300 font-mono">
            <li className="flex items-center justify-between">
              <span>DB Deduplication</span>
              <span className="text-emerald-400">Unique (creator, ext_id)</span>
            </li>
            <li className="flex items-center justify-between">
              <span>Token Bucket Rate Limit</span>
              <span className="text-emerald-400">Throttled</span>
            </li>
            <li className="flex items-center justify-between">
              <span>Event Emission</span>
              <span className="text-emerald-400">post.detected</span>
            </li>
          </ul>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="font-bold text-slate-200 flex items-center justify-between">
            <span>Watchlist Status</span>
            <span className="text-xs px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800 font-mono">
              Lifecycle
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Full lifecycle monitoring states (ACTIVE, INACTIVE, ERROR, UNSUPPORTED).
          </p>
          <ul className="text-xs space-y-1.5 text-slate-300 font-mono">
            <li className="flex items-center justify-between">
              <span>REST API CRUD</span>
              <span className="text-emerald-400">/api/v1/creators</span>
            </li>
            <li className="flex items-center justify-between">
              <span>Check Metadata</span>
              <span className="text-emerald-400">Tracked</span>
            </li>
            <li className="flex items-center justify-between">
              <span>Sanitized Error Trace</span>
              <span className="text-emerald-400">Redacted</span>
            </li>
          </ul>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 pt-6 flex flex-col md:flex-row justify-between items-center text-xs text-slate-500 gap-4">
        <div>
          CreatorRadar — Open-Source Creator Intelligence Platform (Phase 1 Watchlist Complete)
        </div>
        <div className="flex gap-4">
          <Link href="/creators" className="hover:text-blue-400 transition-colors">
            Creator Watchlist
          </Link>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="hover:text-blue-400 transition-colors">
            API OpenAPI Docs
          </a>
        </div>
      </footer>
    </main>
  );
}
