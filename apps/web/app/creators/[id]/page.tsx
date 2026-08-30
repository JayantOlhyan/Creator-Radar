'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface PostMedia {
  id: string;
  media_type: string;
  media_url: string;
  thumbnail_url?: string;
  position: number;
}

interface Post {
  id: string;
  external_id: string;
  url: string;
  content_type: string;
  caption?: string;
  published_at?: string;
  detected_at: string;
  status: string;
  media: PostMedia[];
}

interface CreatorDetail {
  id: string;
  name: string;
  username: string;
  platform: string;
  profile_url: string;
  is_active: boolean;
  status: string;
  last_checked_at?: string;
  last_successful_check_at?: string;
  last_error_at?: string;
  last_error_message?: string;
  check_interval_minutes: number;
  posts_count: number;
  recent_posts: Post[];
}

export default function CreatorDetailPage({ params }: { params: { id: string } }) {
  const [creator, setCreator] = useState<CreatorDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);

  const fetchDetail = async () => {
    try {
      const res = await fetch(`/api/v1/creators/${params.id}`);
      const data = await res.json();
      if (data.success) {
        setCreator(data.data);
      }
    } catch (err) {
      console.error('Failed fetching creator detail:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [params.id]);

  const handleCheckNow = async () => {
    setChecking(true);
    try {
      await fetch(`/api/v1/creators/${params.id}/check`, { method: 'POST' });
      await fetchDetail();
    } catch (err) {
      console.error('Check failed:', err);
    } finally {
      setChecking(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500 font-mono text-sm">Loading Creator Details...</div>;
  }

  if (!creator) {
    return (
      <div className="p-8 max-w-4xl mx-auto text-center space-y-4">
        <p className="text-slate-400">Creator not found.</p>
        <Link href="/creators" className="text-blue-400 text-xs font-mono">
          ← Back to Watchlist
        </Link>
      </div>
    );
  }

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <Link href="/creators" className="text-slate-400 hover:text-slate-200 text-xs font-mono mb-2 inline-block">
            ← Watchlist
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight text-slate-100">{creator.name}</h1>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
              @{creator.username}
            </span>
          </div>
          <p className="text-slate-400 text-xs mt-1">
            Platform: <span className="capitalize text-slate-200">{creator.platform}</span> • Check Interval: {creator.check_interval_minutes}m
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleCheckNow}
            disabled={checking}
            className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold text-xs transition-colors"
          >
            {checking ? 'Checking...' : 'Check Posts Now'}
          </button>
          <a
            href={creator.profile_url}
            target="_blank"
            rel="noreferrer"
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors"
          >
            Open External Profile ↗
          </a>
        </div>
      </header>

      {/* Diagnostics Banner if ERROR state */}
      {creator.status === 'ERROR' && creator.last_error_message && (
        <section className="bg-rose-950/60 border border-rose-800 rounded-2xl p-4 space-y-1">
          <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">
            Acquisition Diagnostics Alert
          </span>
          <p className="text-xs text-rose-200 font-mono">{creator.last_error_message}</p>
        </section>
      )}

      {/* Monitoring Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-500 block">Status</span>
          <span className="text-lg font-bold text-emerald-400">{creator.status}</span>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-500 block">Detected Posts</span>
          <span className="text-lg font-bold text-slate-100">{creator.posts_count}</span>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-500 block">Last Check</span>
          <span className="text-sm font-bold text-slate-300 font-mono">
            {creator.last_checked_at ? new Date(creator.last_checked_at).toLocaleTimeString() : 'Never'}
          </span>
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
          <span className="text-xs text-slate-500 block">Last Successful Check</span>
          <span className="text-sm font-bold text-slate-300 font-mono">
            {creator.last_successful_check_at ? new Date(creator.last_successful_check_at).toLocaleTimeString() : 'Never'}
          </span>
        </div>
      </section>

      {/* Detected Posts Feed */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-slate-200">Acquired Posts Feed</h2>

        {creator.recent_posts.length === 0 ? (
          <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-8 text-center text-slate-500 text-xs">
            No posts detected yet for @{creator.username}. Click "Check Posts Now" to trigger acquisition.
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {creator.recent_posts.map((post) => (
              <div
                key={post.id}
                className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 space-y-3 flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-mono">
                    <span className="px-2 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-900 uppercase">
                      {post.content_type}
                    </span>
                    <span className="text-slate-500">
                      {post.published_at ? new Date(post.published_at).toLocaleDateString() : 'Recent'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 line-clamp-4 leading-relaxed">
                    {post.caption || 'No caption available.'}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-800 flex justify-between items-center text-xs font-mono text-slate-500">
                  <span>Ext ID: {post.external_id}</span>
                  <a
                    href={post.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-400 hover:underline"
                  >
                    View Post ↗
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
