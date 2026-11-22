import React, { useMemo, useRef, useState } from 'react';
import { Download, RefreshCw, StickyNote, Upload } from 'lucide-react';
import { api } from '../api/client';
import {
  HERO_TIER_CATALOG,
  HeroCompanionSprite,
} from '../components/HeroCompanion';
import {
  PixelBoltIcon,
  PixelCampfireIcon,
  PixelCheckIcon,
  PixelCoinIcon,
  PixelFlagIcon,
  PixelPythonIcon,
  PixelScrollIcon,
  PixelSkullIcon,
  PixelSwordIcon,
} from '../components/PixelIcons';
import { TopNav } from '../components/TopNav';
import type {
  CurriculumResponse,
  LessonStatus,
  LessonSummary,
  ModuleGroup,
} from '../types/api';

interface DashboardPageProps {
  curriculum: CurriculumResponse;
  onSelectModule: (moduleId: string) => void;
  onSelectLesson: (lessonId: string) => void;
  onNavigateRoadmap: () => void;
  onNavigateProjects: () => void;
  onProgressUpdated?: () => void;
  completedProjectsCount?: number;
  totalProjectsCount?: number;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  curriculum,
  onSelectModule,
  onSelectLesson,
  onNavigateRoadmap,
  onNavigateProjects,
  onProgressUpdated,
  completedProjectsCount = 0,
  totalProjectsCount = 1,
}) => {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | LessonStatus | 'FLAGGED' | 'REVIEW'>('ALL');
  const [backupNotice, setBackupNotice] = useState<string | null>(null);
  const [backupBusy, setBackupBusy] = useState(false);
  const importInputRef = useRef<HTMLInputElement | null>(null);

  const completionPercent = useMemo(() => {
    if (curriculum.totalLessons === 0) return 0;
    return Math.round((curriculum.completedLessons / curriculum.totalLessons) * 100);
  }, [curriculum]);

  const xpPercent = useMemo(() => {
    if (curriculum.totalXp === 0) return 0;
    return Math.round((curriculum.earnedXp / curriculum.totalXp) * 100);
  }, [curriculum]);

  const bossStats = useMemo(() => {
    let total = 0;
    let defeated = 0;
    for (const mod of curriculum.modules) {
      for (const l of mod.lessons) {
        if (l.kind === 'BOSS') {
          total++;
          if (l.status === 'COMPLETED') defeated++;
        }
      }
    }
    return { total, defeated };
  }, [curriculum.modules]);

  const nextRecommendedLesson = useMemo<LessonSummary | null>(() => {
    for (const mod of curriculum.modules) {
      for (const lesson of mod.lessons) {
        if (lesson.status === 'IN_PROGRESS') return lesson;
      }
    }
    for (const mod of curriculum.modules) {
      for (const lesson of mod.lessons) {
        if (lesson.status === 'NOT_STARTED') return lesson;
      }
    }
    return curriculum.modules[0]?.lessons[0] ?? null;
  }, [curriculum]);

  const isSearchingLessons = search.trim().length > 0;
  const isFlaggedQueue = statusFilter === 'FLAGGED';
  const isReviewQueue = statusFilter === 'REVIEW';
  const showLessonGrid = isSearchingLessons || isFlaggedQueue || isReviewQueue;

  const flaggedTotalCount = useMemo(() => {
    let count = 0;
    for (const mod of curriculum.modules) {
      for (const l of mod.lessons) {
        if (l.flagged) count++;
      }
    }
    return count;
  }, [curriculum.modules]);

  const reviewTotalCount = useMemo(() => {
    let count = 0;
    for (const mod of curriculum.modules) {
      for (const l of mod.lessons) {
        if (l.needsReview) count++;
      }
    }
    return count;
  }, [curriculum.modules]);

  const matchingLessons = useMemo<LessonSummary[]>(() => {
    if (!showLessonGrid) return [];
    const q = search.trim().toLowerCase();
    const results: LessonSummary[] = [];
    for (const mod of curriculum.modules) {
      for (const l of mod.lessons) {
        if (statusFilter === 'FLAGGED' && !l.flagged) continue;
        if (statusFilter === 'REVIEW' && !l.needsReview) continue;
        if (
          statusFilter !== 'ALL' &&
          statusFilter !== 'FLAGGED' &&
          statusFilter !== 'REVIEW' &&
          l.status !== statusFilter
        ) {
          continue;
        }
        if (
          !q ||
          l.id.toLowerCase().includes(q) ||
          l.title.toLowerCase().includes(q) ||
          l.objective.toLowerCase().includes(q) ||
          l.moduleTitle.toLowerCase().includes(q) ||
          l.tags.some((tag) => tag.toLowerCase().includes(q))
        ) {
          results.push(l);
        }
      }
    }
    return results;
  }, [curriculum.modules, search, showLessonGrid, statusFilter]);

  const filteredModules = useMemo<ModuleGroup[]>(() => {
    if (statusFilter === 'ALL' || statusFilter === 'FLAGGED' || statusFilter === 'REVIEW') {
      return curriculum.modules;
    }
    return curriculum.modules.filter((mod) => deriveModuleStatus(mod) === statusFilter);
  }, [curriculum.modules, statusFilter]);

  const handleExportBackup = async () => {
    if (backupBusy) return;
    setBackupBusy(true);
    setBackupNotice(null);
    try {
      const payload = await api.exportProgress();
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'pyquest-progress-backup.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setBackupNotice(`Exported ${payload.lessons.length} stage record(s).`);
    } catch (err) {
      setBackupNotice(`Export failed: ${(err as Error).message}`);
    } finally {
      setBackupBusy(false);
    }
  };

  const handleImportFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = '';
    if (!file || backupBusy) return;
    setBackupBusy(true);
    setBackupNotice(null);
    try {
      const text = await file.text();
      const parsed = JSON.parse(text);
      await api.importProgress(parsed);
      onProgressUpdated?.();
      setBackupNotice('Progress & notes backup restored.');
    } catch (err) {
      setBackupNotice(`Import failed: ${(err as Error).message}`);
    } finally {
      setBackupBusy(false);
    }
  };

  const hero = curriculum.hero;
  const nextTierPct = useMemo(() => {
    if (!hero.nextTier || hero.modulesForNextTier <= 0) return 100;
    return Math.min(100, Math.round((hero.completedModules / hero.modulesForNextTier) * 100));
  }, [hero]);

  return (
    <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC]">
      <TopNav
        activeSection="world-map"
        onNavigateWorldMap={() => {}}
        onNavigateRoadmap={onNavigateRoadmap}
        onNavigateProjects={onNavigateProjects}
        completedProjectsCount={completedProjectsCount}
        totalProjectsCount={totalProjectsCount}
        streak={curriculum.streak}
      />

      {/* Calm Ambient Hero & 5-Tier Character Sheet */}
      <header
        className="border-b border-white/[0.08]"
        style={{
          background:
            'radial-gradient(ellipse 65% 75% at 25% 0%, rgba(245, 185, 66, 0.06), transparent 70%), radial-gradient(ellipse 50% 60% at 85% 15%, rgba(56, 189, 248, 0.05), transparent 70%)',
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Left Hero Intro */}
          <div className="lg:col-span-6 space-y-4">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-white/[0.05] text-[#38BDF8] text-xs font-semibold">
              <PixelPythonIcon className="w-3.5 h-3.5 shrink-0" />
              <span>Python 3.13, Data Structures & AI Systems</span>
            </div>

            <h1 className="font-pixel text-2xl sm:text-3xl text-[#F8FAFC] leading-tight flex items-center gap-3">
              <PixelSwordIcon className="w-7 h-7 shrink-0" />
              <span>Python Terminal Quest</span>
            </h1>

            <p className="font-prose text-sm sm:text-[15px] text-slate-400 max-w-xl leading-relaxed">
              Master {curriculum.modules.length} engineering realms and {curriculum.totalLessons}{' '}
              hands-on coding trials graded locally with{' '}
              <code className="bg-slate-400/[0.14] text-[#BAE6FD] px-1.5 py-[1px] rounded-[4px] text-[13px] font-mono">
                pytest
              </code>{' '}
              in isolated temp workspaces—with progressive hints, markdown study notes, and a
              pluggable RAG Oracle.
            </p>
          </div>

          {/* Right 5-Tier Hero Companion Character Sheet */}
          <div className="lg:col-span-6 rpg-panel-gold p-5 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.08] pb-3.5">
              <div className="flex items-center gap-3.5">
                <div className="p-2 rounded-lg bg-[#0D1017] border border-[#F5B942]/35">
                  <HeroCompanionSprite tier={hero.tier} className="w-12 h-12" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-[#F8FAFC]">{hero.title}</span>
                    <span className="px-2 py-0.5 rounded bg-[#F5B942]/15 text-[#F5B942] text-[11px] font-semibold">
                      Tier {hero.tier}/5
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">{hero.subtitle}</div>
                </div>
              </div>

              <div className="flex items-center gap-3 text-xs font-medium">
                <span
                  title={`Longest streak: ${curriculum.streak?.longestStreakDays ?? 0} day(s)`}
                  className="inline-flex items-center gap-1.5 text-amber-300"
                >
                  <PixelCampfireIcon className="w-3.5 h-3.5" />
                  <span>{curriculum.streak?.currentStreakDays ?? 0}d streak</span>
                </span>
                <span className="text-slate-600">•</span>
                <span title="Bosses Defeated" className="inline-flex items-center gap-1.5 text-[#F45D78]">
                  <PixelSkullIcon className="w-3.5 h-3.5" />
                  <span>
                    {bossStats.defeated}/{bossStats.total} bosses
                  </span>
                </span>
              </div>
            </div>

            {/* Tier Evolution Strip */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400">
                  {hero.nextTierTitle
                    ? `Next evolution: Tier ${hero.nextTier} (${hero.nextTierTitle})`
                    : 'Maximum evolution unlocked'}
                </span>
                <span className="font-medium text-[#38BDF8]">
                  {hero.completedModules}/{hero.modulesForNextTier} modules
                </span>
              </div>
              <div className="flex items-center gap-1.5">
                {HERO_TIER_CATALOG.map((item) => {
                  const unlocked = hero.tier >= item.tier;
                  return (
                    <div
                      key={item.tier}
                      title={`Tier ${item.tier}: ${item.title} (${item.gearLabel})`}
                      className={`flex-1 h-1.5 rounded-full transition-all ${
                        unlocked ? 'bg-[#F5B942]' : 'bg-[#0B0E14] border border-white/[0.08]'
                      }`}
                    />
                  );
                })}
              </div>
              {hero.nextTierTitle && (
                <div className="text-[11px] text-slate-500">
                  {nextTierPct}% toward {hero.nextTierTitle}
                </div>
              )}
            </div>

            {/* Progress Bars */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Stage mastery</span>
                  <span className="font-medium text-[#2DD4A0]">
                    {curriculum.completedLessons}/{curriculum.totalLessons} ({completionPercent}%)
                  </span>
                </div>
                <div className="w-full h-2.5 rpg-bar-track">
                  <div
                    className="h-full rpg-bar-fill transition-all duration-300"
                    style={{ width: `${completionPercent}%` }}
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Experience</span>
                  <span className="font-medium text-[#F5B942]">
                    {curriculum.earnedXp} / {curriculum.totalXp} XP
                  </span>
                </div>
                <div className="w-full h-2.5 rpg-bar-track">
                  <div
                    className="h-full rpg-bar-fill-gold transition-all duration-300"
                    style={{ width: `${xpPercent}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Clean Inline Stats + 1-Click Flagged Filter + Resume CTA */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
              <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                <span>
                  <strong className="text-[#2DD4A0] font-semibold">
                    {curriculum.completedLessons}
                  </strong>{' '}
                  cleared
                </span>
                <span>•</span>
                <span>
                  <strong className="text-[#F5B942] font-semibold">
                    {curriculum.inProgressLessons}
                  </strong>{' '}
                  active
                </span>
                <span>•</span>
                <button
                  type="button"
                  onClick={() =>
                    setStatusFilter((prev) => (prev === 'FLAGGED' ? 'ALL' : 'FLAGGED'))
                  }
                  className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md cursor-pointer transition ${
                    statusFilter === 'FLAGGED'
                      ? 'bg-[#F45D78]/20 text-[#F45D78] font-medium'
                      : 'hover:bg-white/[0.06] text-slate-300'
                  }`}
                >
                  <PixelFlagIcon className="w-3 h-3" />
                  <span>{flaggedTotalCount} flagged</span>
                </button>
                <span>•</span>
                <button
                  type="button"
                  onClick={() =>
                    setStatusFilter((prev) => (prev === 'REVIEW' ? 'ALL' : 'REVIEW'))
                  }
                  className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md cursor-pointer transition ${
                    statusFilter === 'REVIEW'
                      ? 'bg-[#A78BFA]/20 text-[#A78BFA] font-medium'
                      : 'hover:bg-white/[0.06] text-slate-300'
                  }`}
                >
                  <RefreshCw className="w-3 h-3" />
                  <span>{reviewTotalCount} review</span>
                </button>
              </div>

              {nextRecommendedLesson && (
                <button
                  type="button"
                  onClick={() => onSelectLesson(nextRecommendedLesson.id)}
                  className="w-full sm:w-auto py-2 px-4 text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer rpg-btn-gold"
                >
                  <PixelSwordIcon className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate max-w-[260px]">
                    {nextRecommendedLesson.status === 'IN_PROGRESS'
                      ? 'Resume Quest'
                      : 'Start Next Quest'}
                    : #{nextRecommendedLesson.id}
                  </span>
                </button>
              )}
            </div>

            {/* Progress & Notes Backup Strip */}
            <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-white/[0.06] text-[11px]">
              <span className="text-slate-400">
                {backupNotice ?? 'Local SQLite state (progress, drafts, notes & guild checklists)'}
              </span>
              <div className="flex items-center gap-1.5">
                <input
                  ref={importInputRef}
                  type="file"
                  accept="application/json,.json"
                  onChange={handleImportFile}
                  className="hidden"
                />
                <button
                  type="button"
                  disabled={backupBusy}
                  onClick={handleExportBackup}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-[#0D1017] border border-white/[0.08] hover:border-[#F5B942]/50 text-slate-300 hover:text-white cursor-pointer transition disabled:opacity-40"
                >
                  <Download className="w-3 h-3 text-[#38BDF8]" />
                  <span>Export JSON</span>
                </button>
                <button
                  type="button"
                  disabled={backupBusy}
                  onClick={() => importInputRef.current?.click()}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-[#0D1017] border border-white/[0.08] hover:border-[#2DD4A0]/50 text-slate-300 hover:text-white cursor-pointer transition disabled:opacity-40"
                >
                  <Upload className="w-3 h-3 text-[#2DD4A0]" />
                  <span>Import JSON</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Search & Filter Toolbar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 pt-6">
        <div className="rpg-panel p-2.5 flex flex-col md:flex-row gap-2.5 items-stretch md:items-center justify-between">
          <div className="relative flex-1 flex items-center bg-[#0D1017] border border-white/[0.08] focus-within:border-[#F5B942]/60 rounded-md px-3 min-w-0">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={`Search all ${curriculum.totalLessons} quests (e.g. Decimal, deque, match/case, 02-08)...`}
              className="w-full py-2 bg-transparent text-[13px] text-[#F8FAFC] placeholder-slate-500 focus:outline-none min-w-0"
            />
            {isSearchingLessons && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="text-xs font-medium text-[#F5B942] hover:text-white ml-2 cursor-pointer shrink-0"
              >
                Clear
              </button>
            )}
          </div>

          <div className="inline-flex flex-wrap bg-[#0D1017] p-1 rounded-md border border-white/[0.06] gap-1 self-start md:self-auto">
            {(['ALL', 'NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'REVIEW', 'FLAGGED'] as const).map(
              (st) => (
                <button
                  key={st}
                  type="button"
                  onClick={() => setStatusFilter(st)}
                  className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium transition cursor-pointer ${
                    statusFilter === st
                      ? st === 'FLAGGED'
                        ? 'bg-[#F45D78] text-[#0D1017] font-semibold'
                        : st === 'REVIEW'
                          ? 'bg-[#A78BFA] text-[#0D1017] font-semibold'
                          : 'bg-[#F5B942] text-[#0D1017] font-semibold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {st === 'FLAGGED' && <PixelFlagIcon className="w-3 h-3" />}
                  {st === 'REVIEW' && <RefreshCw className="w-3 h-3" />}
                  <span>
                    {st === 'ALL'
                      ? 'All'
                      : st === 'NOT_STARTED'
                        ? 'Open'
                        : st === 'IN_PROGRESS'
                          ? 'Active'
                          : st === 'COMPLETED'
                            ? 'Cleared'
                            : st === 'REVIEW'
                              ? `Review${reviewTotalCount > 0 ? ` (${reviewTotalCount})` : ''}`
                              : `Flagged${flaggedTotalCount > 0 ? ` (${flaggedTotalCount})` : ''}`}
                  </span>
                </button>
              )
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 pb-12">
        {showLessonGrid ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-xs font-semibold text-slate-400 flex items-center gap-2">
                {isFlaggedQueue && !isSearchingLessons ? (
                  <PixelFlagIcon className="w-3.5 h-3.5" />
                ) : isReviewQueue && !isSearchingLessons ? (
                  <RefreshCw className="w-3.5 h-3.5 text-[#A78BFA]" />
                ) : (
                  <PixelScrollIcon className="w-3.5 h-3.5" />
                )}
                <span>
                  {isFlaggedQueue && !isSearchingLessons
                    ? 'Flagged for Review'
                    : isReviewQueue && !isSearchingLessons
                      ? 'Assisted / Spaced Review Queue'
                      : 'Quest Search Results'}{' '}
                  ({matchingLessons.length})
                </span>
              </h2>
            </div>

            {matchingLessons.length === 0 ? (
              <div className="rpg-panel text-center py-14 text-slate-400 text-sm px-4">
                {isFlaggedQueue && !isSearchingLessons
                  ? 'No quests flagged for review yet. Open any stage and click Flag in the workspace toolbar.'
                  : isReviewQueue && !isSearchingLessons
                    ? 'No quests in your review queue yet. Stages cleared with hints/solution or flagged appear here for a cold retry.'
                    : `No quests match "${search}".`}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {matchingLessons.map((lesson) => {
                  const isBoss = lesson.kind === 'BOSS';
                  const isWeb = lesson.runtime === 'WEB_INTEGRATION';
                  return (
                    <button
                      key={lesson.id}
                      type="button"
                      onClick={() => onSelectLesson(lesson.id)}
                      className="text-left group rpg-card p-4 flex flex-col justify-between gap-3 cursor-pointer"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between gap-2">
                          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-300">
                            {isBoss ? (
                              <PixelSkullIcon className="w-3.5 h-3.5" />
                            ) : isWeb ? (
                              <PixelBoltIcon className="w-3.5 h-3.5" />
                            ) : (
                              <PixelPythonIcon className="w-3.5 h-3.5" />
                            )}
                            <span>{isBoss ? `Boss #${lesson.id}` : `Stage #${lesson.id}`}</span>
                          </span>

                          <div className="flex items-center gap-1.5">
                            {lesson.flagged && <PixelFlagIcon className="w-3 h-3" />}
                            {lesson.hasNotes && (
                              <StickyNote className="w-3.5 h-3.5 text-[#38BDF8]" />
                            )}
                            {lesson.needsReview ? (
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-[#A78BFA]/15 text-[#A78BFA]">
                                Assisted
                              </span>
                            ) : (
                              lesson.status === 'COMPLETED' && (
                                <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-[#2DD4A0]/15 text-[#2DD4A0]">
                                  Cold Clear
                                </span>
                              )
                            )}
                            <StatusBadge status={lesson.status} />
                          </div>
                        </div>

                        <div className="text-xs text-[#38BDF8] truncate">{lesson.moduleTitle}</div>

                        <h3 className="text-[15px] font-semibold text-[#F8FAFC] group-hover:text-[#F5B942] transition line-clamp-2">
                          {lesson.title}
                        </h3>

                        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                          {lesson.objective}
                        </p>
                      </div>

                      <div className="pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs">
                        <span className="inline-flex items-center gap-1.5 text-[#F5B942] font-medium">
                          <PixelCoinIcon className="w-3.5 h-3.5" />
                          <span>+{lesson.xp} XP</span>
                        </span>
                        <span className="text-slate-300 group-hover:text-[#F5B942] transition font-medium">
                          Enter stage →
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-semibold text-slate-400 flex items-center gap-2">
                <PixelScrollIcon className="w-3.5 h-3.5" />
                <span>
                  Realms ({curriculum.modules.length} modules • {curriculum.totalLessons} stages)
                </span>
              </h2>
            </div>

            {filteredModules.length === 0 ? (
              <div className="rpg-panel text-center py-14 text-slate-400 text-sm">
                No realms match the selected status filter.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredModules.map((mod) => {
                  const modPercent =
                    mod.totalLessons === 0
                      ? 0
                      : Math.round((mod.completedLessons / mod.totalLessons) * 100);
                  const modStatus = deriveModuleStatus(mod);
                  const topTags = extractModuleTags(mod, 3);
                  const [modNumberLabel, modCleanTitle] = splitModuleTitle(mod.title);
                  const modFlaggedCount = mod.lessons.filter((l) => l.flagged).length;
                  const isWeb = mod.lessons.some((l) => l.runtime === 'WEB_INTEGRATION');

                  return (
                    <button
                      key={mod.id}
                      type="button"
                      onClick={() => onSelectModule(mod.id)}
                      className="text-left group rpg-card p-5 flex flex-col justify-between gap-4 cursor-pointer"
                    >
                      <div className="space-y-3">
                        <div className="flex items-center justify-between gap-2">
                          <div className="flex items-center gap-2 text-xs">
                            <span className="font-semibold text-[#F5B942]">{modNumberLabel}</span>
                            <span className="text-slate-600">•</span>
                            <span className="inline-flex items-center gap-1 text-slate-400">
                              {isWeb ? (
                                <PixelBoltIcon className="w-3 h-3" />
                              ) : (
                                <PixelPythonIcon className="w-3 h-3" />
                              )}
                              <span>{isWeb ? 'Web & AI' : 'Python 3.13'}</span>
                            </span>
                          </div>

                          <div className="flex items-center gap-2">
                            {modFlaggedCount > 0 && (
                              <span
                                title={`${modFlaggedCount} quest(s) flagged for review`}
                                className="inline-flex items-center gap-1 text-[11px] font-medium text-[#F45D78]"
                              >
                                <PixelFlagIcon className="w-3 h-3" />
                                <span>{modFlaggedCount}</span>
                              </span>
                            )}
                            <ModuleStatusBadge status={modStatus} />
                          </div>
                        </div>

                        <h3 className="text-[15px] font-semibold text-[#F8FAFC] group-hover:text-[#F5B942] transition leading-snug">
                          {modCleanTitle}
                        </h3>

                        {topTags.length > 0 && (
                          <div className="flex flex-wrap gap-1.5">
                            {topTags.map((tag) => (
                              <span
                                key={tag}
                                className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      <div className="pt-3 border-t border-white/[0.06] space-y-2.5">
                        <div className="space-y-1.5">
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-slate-400">
                              {mod.completedLessons}/{mod.totalLessons} stages
                            </span>
                            <span
                              className={`font-medium ${
                                modPercent === 100 ? 'text-[#2DD4A0]' : 'text-[#F5B942]'
                              }`}
                            >
                              {mod.earnedXp}/{mod.totalXp} XP ({modPercent}%)
                            </span>
                          </div>
                          <div className="w-full h-2 rpg-bar-track">
                            <div
                              className={`h-full transition-all duration-300 ${
                                modPercent === 100 ? 'rpg-bar-fill' : 'rpg-bar-fill-gold'
                              }`}
                              style={{ width: `${modPercent}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export function deriveModuleStatus(mod: ModuleGroup): LessonStatus {
  if (mod.totalLessons > 0 && mod.completedLessons === mod.totalLessons) {
    return 'COMPLETED';
  }
  if (mod.completedLessons > 0 || mod.lessons.some((l) => l.status === 'IN_PROGRESS')) {
    return 'IN_PROGRESS';
  }
  return 'NOT_STARTED';
}

export function extractModuleTags(mod: ModuleGroup, limit: number): string[] {
  const seen = new Set<string>();
  for (const lesson of mod.lessons) {
    for (const tag of lesson.tags) {
      seen.add(tag);
      if (seen.size >= limit) {
        return Array.from(seen);
      }
    }
  }
  return Array.from(seen);
}

export function splitModuleTitle(rawTitle: string): [string, string] {
  const idx = rawTitle.indexOf(':');
  if (idx > 0) {
    const label = rawTitle.slice(0, idx).trim();
    const formatted = label.charAt(0).toUpperCase() + label.slice(1).toLowerCase();
    return [formatted, rawTitle.slice(idx + 1).trim()];
  }
  return ['Module', rawTitle];
}

export const ModuleStatusBadge: React.FC<{ status: LessonStatus }> = ({ status }) => {
  if (status === 'COMPLETED') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-[#2DD4A0]/15 text-[#2DD4A0]">
        <PixelCheckIcon className="w-3 h-3" />
        <span>Cleared</span>
      </span>
    );
  }
  if (status === 'IN_PROGRESS') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-[#F5B942]/15 text-[#F5B942]">
        <span>Active</span>
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-white/[0.05] text-slate-400">
      <span>Open</span>
    </span>
  );
};

export const StatusBadge: React.FC<{ status: LessonStatus }> = ({ status }) => {
  if (status === 'COMPLETED') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-[#2DD4A0]/15 text-[#2DD4A0]">
        <PixelCheckIcon className="w-3 h-3" />
        <span>Done</span>
      </span>
    );
  }
  if (status === 'IN_PROGRESS') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-[#F5B942]/15 text-[#F5B942]">
        <span>WIP</span>
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-white/[0.05] text-slate-400">
      <span>Todo</span>
    </span>
  );
};
