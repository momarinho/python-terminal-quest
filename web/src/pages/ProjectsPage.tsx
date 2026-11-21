import React, { useEffect, useState } from 'react';
import {
  Check,
  Copy,
  ExternalLink,
  FolderGit2,
  Loader2,
  Lock,
  ShieldCheck,
  Unlock,
} from 'lucide-react';
import { api } from '../api/client';
import {
  PixelBotIcon,
  PixelCheckIcon,
  PixelGateIcon,
  PixelPythonIcon,
  PixelScrollIcon,
  PixelTrophyIcon,
} from '../components/PixelIcons';
import { TopNav } from '../components/TopNav';
import type { PortfolioProject, ProjectsResponse, StreakStats } from '../types/api';

interface ProjectsPageProps {
  onNavigateWorldMap: () => void;
  onNavigateRoadmap: () => void;
  onProjectsLoaded?: (summary: { completed: number; total: number }) => void;
  streak?: StreakStats | null;
}

export const ProjectsPage: React.FC<ProjectsPageProps> = ({
  onNavigateWorldMap,
  onNavigateRoadmap,
  onProjectsLoaded,
  streak = null,
}) => {
  const [data, setData] = useState<ProjectsResponse | null>(null);
  const [repoInputs, setRepoInputs] = useState<Record<string, string>>({});
  const [busyProjectId, setBusyProjectId] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [statusBanner, setStatusBanner] = useState<string | null>(null);
  const [copiedPromptKey, setCopiedPromptKey] = useState<string | null>(null);

  const handleCopyPrompt = async (key: string, prompt: string) => {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopiedPromptKey(key);
      window.setTimeout(() => {
        setCopiedPromptKey((prev) => (prev === key ? null : prev));
      }, 1800);
    } catch {
      setErrorMsg('Clipboard unavailable in this browser context.');
    }
  };

  useEffect(() => {
    api
      .getProjects()
      .then((res) => {
        setData(res);
        const initialInputs: Record<string, string> = {};
        for (const p of res.projects) {
          initialInputs[p.id] = p.progress.repoUrl ?? '';
        }
        setRepoInputs(initialInputs);
        onProjectsLoaded?.({ completed: res.completedProjects, total: res.totalProjects });
      })
      .catch((err: Error) => setErrorMsg(err.message));
  }, [onProjectsLoaded]);

  const applyProjectUpdate = (updated: PortfolioProject) => {
    setData((prev) => {
      if (!prev) return prev;
      const nextProjects = prev.projects.map((p) => (p.id === updated.id ? updated : p));
      const completedCount = nextProjects.filter((p) => p.progress.status === 'COMPLETED').length;
      const unlockedCount = nextProjects.filter((p) => p.milestoneUnlocked).length;
      onProjectsLoaded?.({ completed: completedCount, total: nextProjects.length });
      return {
        ...prev,
        completedProjects: completedCount,
        unlockedProjects: unlockedCount,
        projects: nextProjects,
      };
    });
  };

  const handleToggleChecklist = async (
    project: PortfolioProject,
    itemId: string,
    checked: boolean
  ) => {
    setErrorMsg(null);
    setStatusBanner(null);
    setBusyProjectId(project.id);
    try {
      const updated = await api.updateProjectChecklist(project.id, itemId, checked);
      applyProjectUpdate(updated);
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : 'Failed to update sprint checklist item');
    } finally {
      setBusyProjectId(null);
    }
  };

  const handleSaveRepo = async (project: PortfolioProject, markCompleted?: boolean) => {
    setErrorMsg(null);
    setStatusBanner(null);
    setBusyProjectId(project.id);
    const repoUrl = repoInputs[project.id] ?? '';
    try {
      const updated = await api.updateProjectRepo(project.id, repoUrl, markCompleted);
      applyProjectUpdate(updated);
      setRepoInputs((prev) => ({ ...prev, [project.id]: updated.progress.repoUrl }));
      setStatusBanner(
        markCompleted
          ? `Capstone "${updated.title}" shipped and logged to Guild Ledger.`
          : `Repository link saved for "${updated.title}".`
      );
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : 'Failed to save repository');
    } finally {
      setBusyProjectId(null);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC]">
      <TopNav
        activeSection="projects"
        onNavigateWorldMap={onNavigateWorldMap}
        onNavigateRoadmap={onNavigateRoadmap}
        onNavigateProjects={() => {}}
        completedProjectsCount={data?.completedProjects ?? 0}
        totalProjectsCount={data?.totalProjects ?? 1}
        streak={streak}
      />

      <header
        className="border-b border-white/[0.08]"
        style={{
          background:
            'radial-gradient(ellipse 60% 75% at 25% 0%, rgba(167, 139, 250, 0.08), transparent 70%)',
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-white/[0.05] text-[#A78BFA] text-xs font-semibold">
              <PixelGateIcon className="w-3.5 h-3.5" />
              <span>Guild Notice Board • Capstone PRDs</span>
            </div>

            <h1 className="font-pixel text-2xl sm:text-3xl text-[#F8FAFC] flex items-center gap-3">
              <PixelTrophyIcon className="w-7 h-7 shrink-0" />
              <span>Portfolio Guild</span>
            </h1>

            <p className="font-prose text-sm text-slate-400 leading-relaxed">
              Production-grade Python engineering PRDs designed to be built in your local IDE and
              GitHub with <code className="bg-slate-400/[0.14] text-[#BAE6FD] px-1.5 py-[1px] rounded-[4px] text-[13px] font-mono">uv</code>,{' '}
              <code className="bg-slate-400/[0.14] text-[#BAE6FD] px-1.5 py-[1px] rounded-[4px] text-[13px] font-mono">pytest</code>,
              and GitHub Actions CI. Sprint progress persists in SQLite.
            </p>
          </div>

          {data && (
            <div className="rpg-panel-amethyst p-4 w-full lg:w-auto lg:min-w-[330px] grid grid-cols-3 gap-2.5 text-center">
              <div className="bg-[#0D1017] border border-white/[0.06] rounded-md py-2.5 px-2">
                <div className="text-lg font-bold text-[#2DD4A0]">{data.completedProjects}</div>
                <div className="text-[11px] text-slate-400">Shipped</div>
              </div>
              <div className="bg-[#0D1017] border border-white/[0.06] rounded-md py-2.5 px-2">
                <div className="text-lg font-bold text-[#F5B942]">{data.unlockedProjects}</div>
                <div className="text-[11px] text-slate-400">Unlocked</div>
              </div>
              <div className="bg-[#0D1017] border border-white/[0.06] rounded-md py-2.5 px-2">
                <div className="text-lg font-bold text-[#A78BFA]">{data.totalProjects}</div>
                <div className="text-[11px] text-slate-400">Total PRDs</div>
              </div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
        {errorMsg && (
          <div className="rpg-panel border-[#F45D78]/40 bg-[#231219] px-4 py-3 text-xs text-[#FDA4AF]">
            {errorMsg}
          </div>
        )}
        {statusBanner && (
          <div className="rpg-panel border-[#2DD4A0]/40 bg-[#0F241F] px-4 py-3 text-xs text-[#2DD4A0]">
            {statusBanner}
          </div>
        )}

        {!data ? (
          <div className="py-16 flex items-center justify-center gap-3 text-slate-300">
            <Loader2 className="w-5 h-5 animate-spin text-[#F5B942]" />
            <span className="text-sm font-medium">Loading Guild Notice Board...</span>
          </div>
        ) : (
          <div className="space-y-8">
            {data.projects.map((project) => {
              const checkedSet = new Set(project.progress.completedChecklistIds);
              const allItems = project.sprints.flatMap((s) => s.items);
              const doneCount = allItems.filter((i) => checkedSet.has(i.id)).length;
              const totalCount = allItems.length;
              const percentDone =
                totalCount === 0 ? 0 : Math.round((doneCount / totalCount) * 100);
              const isCompleted = project.progress.status === 'COMPLETED';
              const isBusy = busyProjectId === project.id;

              return (
                <article
                  key={project.id}
                  className={`p-5 sm:p-6 space-y-6 ${
                    isCompleted
                      ? 'rpg-panel border-[#2DD4A0]/45'
                      : project.milestoneUnlocked
                        ? 'rpg-panel-gold'
                        : 'rpg-panel'
                  }`}
                >
                  <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4 border-b border-white/[0.08] pb-4">
                    <div className="space-y-2.5">
                      <div className="flex flex-wrap items-center gap-2 text-xs">
                        <span className="inline-flex items-center gap-1.5 font-semibold px-2.5 py-0.5 rounded-md bg-[#A78BFA]/15 text-[#A78BFA]">
                          <PixelGateIcon className="w-3.5 h-3.5" />
                          <span>Gate #{project.order}</span>
                        </span>
                        <span className="text-slate-400">{project.milestoneLabel}</span>

                        {project.milestoneUnlocked ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
                            <Unlock className="w-3 h-3" />
                            <span>Unlocked</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F5B942]/12 text-[#F5B942] font-medium">
                            <Lock className="w-3 h-3" />
                            <span>
                              Preview ({project.completedPrerequisiteModules}/
                              {project.requiredModulesCompleted} modules)
                            </span>
                          </span>
                        )}

                        {isCompleted && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
                            <PixelCheckIcon className="w-3 h-3" />
                            <span>Shipped</span>
                          </span>
                        )}
                      </div>

                      <h2 className="text-lg font-semibold text-[#F8FAFC]">{project.title}</h2>

                      <div className="flex flex-wrap gap-1.5">
                        {project.techStack.map((tech) => (
                          <span
                            key={tech}
                            className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-[#BAE6FD]"
                          >
                            <PixelPythonIcon className="w-3 h-3" />
                            <span>{tech}</span>
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="w-full lg:w-64 shrink-0 space-y-1.5 bg-[#0D1017] border border-white/[0.08] rounded-lg p-3">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-400">Sprint Checklist</span>
                        <span className="font-semibold text-[#2DD4A0]">
                          {doneCount}/{totalCount} ({percentDone}%)
                        </span>
                      </div>
                      <div className="w-full h-2 rpg-bar-track">
                        <div
                          className="h-full rpg-bar-fill transition-all duration-300"
                          style={{ width: `${percentDone}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <div className="lg:col-span-5 space-y-4">
                      <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-2">
                        <div className="text-xs font-semibold text-[#F5B942] flex items-center gap-2">
                          <PixelScrollIcon className="w-3.5 h-3.5" />
                          <span>Business Context</span>
                        </div>
                        <p className="text-xs sm:text-[13px] text-slate-300 leading-relaxed">
                          {project.businessContext}
                        </p>
                      </div>

                      {project.packageLayout && (
                        <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-2">
                          <div className="text-xs font-semibold text-[#38BDF8]">
                            Target Package Layout
                          </div>
                          <pre className="text-xs font-mono text-slate-200 overflow-x-auto leading-relaxed">
                            {project.packageLayout}
                          </pre>
                        </div>
                      )}

                      {project.reviewCriteria.length > 0 && (
                        <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-2">
                          <div className="text-xs font-semibold text-[#2DD4A0] flex items-center gap-1.5">
                            <ShieldCheck className="w-3.5 h-3.5" />
                            <span>Staff Engineer Review Rubric</span>
                          </div>
                          <ul className="space-y-1.5 text-xs text-slate-300 leading-relaxed list-disc pl-4">
                            {project.reviewCriteria.map((criterion, idx) => (
                              <li key={idx}>{criterion}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    <div className="lg:col-span-7 space-y-4">
                      <div className="space-y-3">
                        {project.sprints.map((sprint) => (
                          <div
                            key={sprint.id}
                            className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-2.5"
                          >
                            <div className="text-xs font-semibold text-[#F8FAFC]">
                              {sprint.title}
                            </div>
                            <div className="space-y-2">
                              {sprint.items.map((item) => {
                                const checked = checkedSet.has(item.id);
                                return (
                                  <label
                                    key={item.id}
                                    className="flex items-start gap-2.5 text-xs text-slate-300 cursor-pointer hover:text-white"
                                  >
                                    <input
                                      type="checkbox"
                                      checked={checked}
                                      disabled={isBusy}
                                      onChange={(e) =>
                                        handleToggleChecklist(project, item.id, e.target.checked)
                                      }
                                      className="mt-0.5 accent-[#2DD4A0] cursor-pointer"
                                    />
                                    <span className={checked ? 'line-through text-slate-500' : ''}>
                                      {item.text}
                                    </span>
                                  </label>
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>

                      {project.aiReviewPrompts.length > 0 && (
                        <div className="bg-[#0D1017] border border-[#A78BFA]/30 rounded-lg p-4 space-y-3">
                          <div className="text-xs font-semibold text-[#A78BFA] flex items-center gap-2">
                            <PixelBotIcon className="w-4 h-4" />
                            <span>1-Click AI Staff Review Prompts</span>
                          </div>
                          <div className="space-y-2">
                            {project.aiReviewPrompts.map((prompt, idx) => {
                              const promptKey = `${project.id}-prompt-${idx}`;
                              const isCopied = copiedPromptKey === promptKey;
                              return (
                                <div
                                  key={promptKey}
                                  className="p-3 rounded-md bg-[#151923] border border-white/[0.06] flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                                >
                                  <p className="text-xs text-slate-300 leading-relaxed">{prompt}</p>
                                  <button
                                    type="button"
                                    onClick={() => handleCopyPrompt(promptKey, prompt)}
                                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold shrink-0 cursor-pointer ${
                                      isCopied ? 'rpg-btn-emerald' : 'rpg-btn-gold'
                                    }`}
                                  >
                                    {isCopied ? (
                                      <>
                                        <Check className="w-3.5 h-3.5" />
                                        <span>Copied</span>
                                      </>
                                    ) : (
                                      <>
                                        <Copy className="w-3.5 h-3.5" />
                                        <span>Copy Prompt</span>
                                      </>
                                    )}
                                  </button>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-3">
                        <div className="text-xs font-semibold text-[#F5B942] flex items-center gap-2">
                          <FolderGit2 className="w-3.5 h-3.5" />
                          <span>Shipped GitHub Repository</span>
                        </div>
                        <div className="flex flex-col sm:flex-row gap-2">
                          <input
                            type="url"
                            value={repoInputs[project.id] ?? ''}
                            onChange={(e) =>
                              setRepoInputs((prev) => ({
                                ...prev,
                                [project.id]: e.target.value,
                              }))
                            }
                            placeholder="https://github.com/you/ledger-reconciler"
                            className="flex-1 bg-[#151923] border border-white/[0.08] focus:border-[#F5B942]/60 rounded-md px-3 py-2 text-xs text-[#F8FAFC] placeholder-slate-500 focus:outline-none"
                          />
                          <button
                            type="button"
                            disabled={isBusy}
                            onClick={() => handleSaveRepo(project)}
                            className="px-3.5 py-2 rounded-md bg-[#1C2230] hover:bg-[#252D40] text-slate-200 text-xs font-medium cursor-pointer transition"
                          >
                            Save URL
                          </button>
                          <button
                            type="button"
                            disabled={isBusy}
                            onClick={() => handleSaveRepo(project, !isCompleted)}
                            className={`px-3.5 py-2 text-xs font-semibold cursor-pointer ${
                              isCompleted
                                ? 'bg-[#1C2230] text-slate-300 rounded-md'
                                : 'rpg-btn-emerald'
                            }`}
                          >
                            {isCompleted ? 'Reopen' : 'Mark Shipped'}
                          </button>
                        </div>
                        {project.progress.repoUrl && (
                          <a
                            href={project.progress.repoUrl}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1.5 text-xs text-[#38BDF8] hover:underline"
                          >
                            <span>Open Repository</span>
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
};
