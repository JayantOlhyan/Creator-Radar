'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import AddCreatorModal from './add-modal';

interface Creator {
  id: string;
  name: string;
  username: string;
  platform: string;
  profile_url: string;
  is_active: bool;
  status: string;
  last_checked_at?: string;
  last_successful_check_at?: string;
  last_error_message?: string;
  check_interval_minutes: number;
}

export default function CreatorsWatchlistPage() {
  const [creators, setCreators] = useState<Creator[]>([]);
  const [loading, setLoading] = useState(true);
  const [checkingId, setCheckingId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchCreators = async () => {
    try {
      const res = await fetch('/api/v1/creators');
      const data = await res.json();
      if (data.success && Array.isArray(data.data)) {
        setCreators(data.data);
      }
    } catch (err) {
      console.error('Failed fetching creators:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCreators();
  }, []);

  const handleCheckNow = async (id: string) => {
    setCheckingId(id);
    try {
      await fetch(`/api/v1/creators/${id}/check`, { method: 'POST' });
      await fetchCreators();
    } catch (err) {
      console.error('Failed triggering creator check:', err);
    } finally {
      setCheckingId(null);
    }
  };

  const handleToggleStatus = async (creator: Creator) => {
    const nextStatus = creator.status === 'ACTIVE' ? 'INACTIVE' : 'ACTIVE';
    try {
      await fetch(`/api/v1/creators/${creator.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      });
      await fetchCreators();
    } catch (err) {
      console.error('Failed toggling creator status:', err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to remove this creator from your watchlist?')) return;
    try {
      await fetch(`/api/v1/creators/${id}`, { method: 'DELETE' });
      await fetchCreators();
    } catch (err) {
      console.error('Failed deleting creator:', err);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono">ACTIVE</span>;
      case 'INACTIVE':
        return <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700 font-mono">INACTIVE</span>;
      case 'ERROR':
        return <span className="text-xs px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 font-mono">ERROR</span>;
      case 'UNSUPPORTED':
        return <span className="text-xs px-2 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800 font-mono">UNSUPPORTED</span>;
      default:
        return <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">{status}</span>;
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      {/* Navigation & Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <Link href="/" className="text-slate-400 hover:text-slate-200 text-sm">
              ← Dashboard
            </Link>
            <span className="text-slate-600">/</span>
            <h1 className="text-2xl font-bold tracking-tight text-slate-100">
              Creator Watchlist
            </h1>
          </div>
          <p className="text-slate-400 text-xs mt-1">
            Monitor creators, configure check intervals, and trigger post acquisition.
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs shadow-lg shadow-blue-600/20 transition-all flex items-center gap-2"
        >
          <span>+ Add Creator</span>
        </button>
      </header>

      {/* Watchlist Table / Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-sm">Loading Watchlist...</div>
      ) : creators.length === 0 ? (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <p className="text-slate-400 text-sm">No creators are currently being monitored.</p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-semibold"
          >
            Add Your First Creator
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {creators.map((creator) => (
            <div
              key={creator.id}
              className="bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition-all rounded-2xl p-5 space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-slate-100 text-base flex items-center gap-2">
                      <Link href={`/creators/${creator.id}`} className="hover:text-blue-400 transition-colors">
                        {creator.name}
                      </Link>
                    </h3>
                    <p className="text-xs text-slate-400 font-mono">@{creator.username}</p>
                  </div>
                  {getStatusBadge(creator.status)}
                </div>

                <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                  <span className="capitalize px-2 py-0.5 rounded bg-slate-950 border border-slate-800">
                    {creator.platform}
                  </span>
                  <span>Interval: {creator.check_interval_minutes}m</span>
                </div>

                <div className="text-xs text-slate-500 space-y-1 font-mono pt-2 border-t border-slate-800/60">
                  <div>Last Check: {creator.last_checked_at ? new Date(creator.last_checked_at).toLocaleTimeString() : 'Never'}</div>
                  {creator.last_error_message && (
                    <div className="text-rose-400 truncate">Error: {creator.last_error_message}</div>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-800 text-xs">
                <button
                  onClick={() => handleCheckNow(creator.id)}
                  disabled={checkingId === creator.id}
                  className="px-3 py-1.5 rounded-lg bg-blue-950 hover:bg-blue-900 text-blue-300 border border-blue-800 font-semibold transition-colors disabled:opacity-50"
                >
                  {checkingId === creator.id ? 'Checking...' : 'Check Now'}
                </button>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleToggleStatus(creator)}
                    className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                  >
                    {creator.status === 'ACTIVE' ? 'Pause' : 'Activate'}
                  </button>
                  <button
                    onClick={() => handleDelete(creator.id)}
                    className="px-2.5 py-1.5 rounded-lg bg-rose-950/40 hover:bg-rose-950 text-rose-400 border border-rose-900 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Creator Modal */}
      <AddCreatorModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={fetchCreators}
      />
    </main>
  );
}
