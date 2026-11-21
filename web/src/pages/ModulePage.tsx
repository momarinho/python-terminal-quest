import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  Copy,
  Share2,
  StickyNote,
} from 'lucide-react';
import {
  PixelBoltIcon,
  PixelCampfireIcon,
  PixelCheckIcon,
  PixelCoinIcon,
  PixelCrownIcon,
  PixelFlagIcon,
  PixelPythonIcon,
  PixelScrollIcon,
  PixelSkullIcon,
  PixelSwordIcon,
  PixelTrophyIcon,
} from '../components/PixelIcons';
import { TopNav } from '../components/TopNav';
import {
  deriveModuleStatus,
  extractModuleTags,
  ModuleStatusBadge,
  splitModuleTitle,
  StatusBadge,
} from './DashboardPage';
import type {
  CurriculumResponse,
  LessonSummary,
  LinkedinAngle,
  ModuleInsight,
} from '../types/api';

interface ModulePageProps {
  curriculum: CurriculumResponse;
  moduleId: string;
  initialOpenCampfire?: boolean;
  onBackToDashboard: () => void;
  onNavigateRoadmap: () => void;
  onNavigateProjects: () => void;
  onSelectModule: (moduleId: string) => void;
  onSelectLesson: (lessonId: string) => void;
  completedProjectsCount?: number;
  totalProjectsCount?: number;
}

function buildLinkedInDraft(
  modNumberLabel: string,
  modCleanTitle: string,
  angle: LinkedinAngle,
  reflectionPrompts: string[],
  tags: string[],
  isBossPost: boolean
): string {
  const tagsLine = tags.length > 0 ? tags.slice(0, 4).join(' • ') : 'Python 3.13';
  const reflections = reflectionPrompts.map((p, i) => `${i + 1}. ${p}`).join('\n');
  const contextLine = isBossPost
    ? `I just tackled the ${modNumberLabel} Boss Fight (${modCleanTitle}) in Python 3.13—here is the engineering lesson that stood out:`
    : `While working through ${modNumberLabel} (${modCleanTitle}) in Python 3.13, here is the mental model shift that clicked:`;

  return [
    angle.hook,
    '',
    contextLine,
    '',
    isBossPost ? 'Engineering Takeaway:' : 'What Modern Python Solves:',
    angle.pythonInsight,
    '',
    'Before vs. After:',
    '```python',
    angle.codeComparison.trim(),
    '```',
    '',
    reflections ? `Questions I tested myself on:\n${reflections}\n` : '',
    `Topics: ${tagsLine}`,
    '#Python #BackendEngineering #SoftwareArchitecture #LearningInPublic',
  ]
    .filter((line, idx, arr) => !(line === '' && arr[idx - 1] === ''))
    .join('\n');
}

export const ModulePage: React.FC<ModulePageProps> = ({
  curriculum,
  moduleId,
  initialOpenCampfire = false,
  onBackToDashboard,
  onNavigateRoadmap,
  onNavigateProjects,
  onSelectModule,
  onSelectLesson,
  completedProjectsCount = 0,
  totalProjectsCount = 1,
}) => {
  const [copiedAngle, setCopiedAngle] = useState<'concept' | 'boss' | null>(null);
  const [insightExpanded, setInsightExpanded] = useState(initialOpenCampfire);
  const [selectedAngleTab, setSelectedAngleTab] = useState<'concept' | 'boss'>('concept');
  const campfireRef = useRef<HTMLDivElement | null>(null);

  const moduleIndex = useMemo(
    () => curriculum.modules.findIndex((m) => m.id === moduleId),
    [curriculum.modules, moduleId]
  );

  const moduleGroup = moduleIndex >= 0 ? curriculum.modules[moduleIndex] : null;
  const hasBossInsightForModule = Boolean(moduleGroup?.insight?.bossLinkedinAngle);

  useEffect(() => {
    setInsightExpanded(initialOpenCampfire);
    setCopiedAngle(null);
    setSelectedAngleTab(initialOpenCampfire && hasBossInsightForModule ? 'boss' : 'concept');
    if (initialOpenCampfire) {
      window.setTimeout(() => {
        campfireRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 80);
    }
  }, [moduleId, initialOpenCampfire, hasBossInsightForModule]);

  const prevModule = moduleIndex > 0 ? curriculum.modules[moduleIndex - 1] : null;
  const nextModule =
    moduleIndex >= 0 && moduleIndex + 1 < curriculum.modules.length
      ? curriculum.modules[moduleIndex + 1]
      : null;

  const continueLesson = useMemo<LessonSummary | null>(() => {
    if (!moduleGroup) return null;
    return (
      moduleGroup.lessons.find((l) => l.status === 'IN_PROGRESS') ??
      moduleGroup.lessons.find((l) => l.status === 'NOT_STARTED') ??
      moduleGroup.lessons[0] ??
      null
    );
  }, [moduleGroup]);

  if (!moduleGroup) {
    return (
      <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC] flex flex-col">
        <TopNav
          activeSection="module"
          onNavigateWorldMap={onBackToDashboard}
          onNavigateRoadmap={onNavigateRoadmap}
          onNavigateProjects={onNavigateProjects}
          completedProjectsCount={completedProjectsCount}
          totalProjectsCount={totalProjectsCount}
          streak={curriculum.streak}
        />
        <div className="flex-1 flex flex-col items-center justify-center gap-4">
          <p className="text-sm text-[#F45D78]">Realm &quot;{moduleId}&quot; not found.</p>
          <button
            type="button"
            onClick={onBackToDashboard}
            className="px-4 py-2 bg-[#151923] border border-white/[0.08] hover:bg-[#1C2230] text-[#F5B942] text-xs font-medium cursor-pointer rounded-md"
          >
            ← Back to World Map
          </button>
        </div>
      </div>
    );
  }

  const modPercent =
    moduleGroup.totalLessons === 0
      ? 0
      : Math.round((moduleGroup.completedLessons / moduleGroup.totalLessons) * 100);
  const modStatus = deriveModuleStatus(moduleGroup);
  const isModuleCleared = modStatus === 'COMPLETED';
  const [modNumberLabel, modCleanTitle] = splitModuleTitle(moduleGroup.title);
  const moduleTags = extractModuleTags(moduleGroup, 6);
  const isWebRealm = moduleGroup.lessons.some((l) => l.runtime === 'WEB_INTEGRATION');
  const insight: ModuleInsight | null | undefined = moduleGroup.insight;
  const hasBossAngle = Boolean(insight?.bossLinkedinAngle);
  const activeAngle: LinkedinAngle | null =
    selectedAngleTab === 'boss' && insight?.bossLinkedinAngle
      ? insight.bossLinkedinAngle
      : (insight?.linkedinAngle ?? null);

  const handleCopyOutline = async (
    e: React.MouseEvent,
    angleToCopy: LinkedinAngle,
    kind: 'concept' | 'boss'
  ) => {
    e.stopPropagation();
    if (!insight) return;
    const outline = buildLinkedInDraft(
      modNumberLabel,
      modCleanTitle,
      angleToCopy,
      insight.reflectionPrompts,
      moduleTags,
      kind === 'boss'
    );
    try {
      await navigator.clipboard.writeText(outline);
      setCopiedAngle(kind);
      window.setTimeout(() => setCopiedAngle(null), 2000);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = outline;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopiedAngle(kind);
      window.setTimeout(() => setCopiedAngle(null), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC]">
      <TopNav
        activeSection="module"
        onNavigateWorldMap={onBackToDashboard}
        onNavigateRoadmap={onNavigateRoadmap}
        onNavigateProjects={onNavigateProjects}
        completedProjectsCount={completedProjectsCount}
        totalProjectsCount={totalProjectsCount}
        streak={curriculum.streak}
      />

      <header className="border-b border-white/[0.08]">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex flex-wrap items-center justify-between gap-4">
          <nav className="flex items-center gap-2 text-xs">
            <button
              type="button"
              onClick={onBackToDashboard}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-300 hover:text-white hover:bg-[#1C2230] font-medium cursor-pointer transition"
            >
              <span>← World Map</span>
            </button>
            <span className="text-slate-600">/</span>
            <span className="text-slate-200 font-medium">{moduleGroup.title}</span>
          </nav>

          <div className="inline-flex items-center rounded-md border border-white/[0.08] bg-[#151923]">
            <button
              type="button"
              disabled={!prevModule}
              onClick={() => prevModule && onSelectModule(prevModule.id)}
              title={prevModule ? prevModule.title : 'First Realm'}
              className="px-2.5 py-1.5 text-xs text-slate-400 hover:text-white disabled:opacity-30 inline-flex items-center gap-1 cursor-pointer disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Prev</span>
            </button>
            <span className="px-3 py-1.5 text-xs font-semibold text-[#F5B942] border-x border-white/[0.08]">
              {modNumberLabel}
            </span>
            <button
              type="button"
              disabled={!nextModule}
              onClick={() => nextModule && onSelectModule(nextModule.id)}
              title={nextModule ? nextModule.title : 'Final Realm'}
              className="px-2.5 py-1.5 text-xs text-slate-400 hover:text-white disabled:opacity-30 inline-flex items-center gap-1 cursor-pointer disabled:cursor-not-allowed"
            >
              <span>Next</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="max-w-6xl mx-auto px-4 sm:px-6 pb-7 pt-2">
          <div className="rpg-panel-gold p-6 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div className="space-y-3 max-w-2xl">
              <div className="flex flex-wrap items-center gap-2.5 text-xs">
                <span className="font-semibold text-[#F5B942]">{modNumberLabel}</span>
                <span className="text-slate-600">•</span>
                <span className="inline-flex items-center gap-1.5 text-slate-300">
                  {isWebRealm ? (
                    <PixelBoltIcon className="w-3.5 h-3.5" />
                  ) : (
                    <PixelPythonIcon className="w-3.5 h-3.5" />
                  )}
                  <span>{isWebRealm ? 'Web & AI' : 'Python 3.13'}</span>
                </span>
                <ModuleStatusBadge status={modStatus} />
                <span className="inline-flex items-center gap-1 text-[#2DD4A0] font-medium">
                  <PixelCoinIcon className="w-3.5 h-3.5" />
                  <span>+{moduleGroup.totalXp} XP pool</span>
                </span>
              </div>

              <h1 className="font-pixel text-xl sm:text-2xl text-[#F8FAFC] leading-snug flex items-center gap-3">
                <PixelScrollIcon className="w-6 h-6 shrink-0" />
                <span>{modCleanTitle}</span>
              </h1>

              <div className="flex flex-wrap gap-1.5 pt-1">
                {moduleTags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 w-full lg:w-auto lg:min-w-[320px] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 flex items-center gap-1.5">
                  <PixelTrophyIcon className="w-4 h-4 shrink-0" />
                  <span>Realm Progress</span>
                </span>
                <span className="text-[#2DD4A0] font-semibold">
                  {moduleGroup.completedLessons} / {moduleGroup.totalLessons} ({modPercent}%)
                </span>
              </div>

              <div className="w-full h-2.5 rpg-bar-track">
                <div
                  className={`h-full transition-all duration-300 ${
                    modPercent === 100 ? 'rpg-bar-fill' : 'rpg-bar-fill-gold'
                  }`}
                  style={{ width: `${modPercent}%` }}
                />
              </div>

              {continueLesson && (
                <button
                  type="button"
                  onClick={() => onSelectLesson(continueLesson.id)}
                  className="w-full py-2 px-3 text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer rpg-btn-gold"
                >
                  <PixelSwordIcon className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">
                    {isModuleCleared
                      ? `Replay Stage #${continueLesson.id}`
                      : `Continue Stage #${continueLesson.id}`}
                  </span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-xs font-semibold text-slate-400">
            Stage Select ({moduleGroup.lessons.length} stages
            {insight ? ' • 1 rest campfire' : ''})
          </h2>
          <span className="text-xs text-slate-500">Select a stage to launch the workspace</span>
        </div>

        <div className="space-y-3">
          {moduleGroup.lessons.map((lesson, idx) => {
            const isBoss = lesson.kind === 'BOSS';
            const isDone = lesson.status === 'COMPLETED';
            const isWeb = lesson.runtime === 'WEB_INTEGRATION';

            return (
              <button
                key={lesson.id}
                type="button"
                onClick={() => onSelectLesson(lesson.id)}
                className={`w-full text-left group p-4 sm:p-5 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer transition ${
                  isBoss
                    ? 'bg-[#21131C] hover:bg-[#2A1723] border border-[#F45D78]/45 hover:border-[#F45D78]'
                    : 'rpg-card'
                }`}
              >
                <div className="space-y-2 flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2.5 text-xs">
                    {isBoss ? (
                      <span className="inline-flex items-center gap-1.5 font-semibold px-2 py-0.5 rounded-md bg-[#F45D78]/15 text-[#F45D78]">
                        {isDone ? (
                          <PixelCrownIcon className="w-3.5 h-3.5" />
                        ) : (
                          <PixelSkullIcon className="w-3.5 h-3.5" />
                        )}
                        <span>Boss Stage #{lesson.id}</span>
                      </span>
                    ) : (
                      <span className="font-semibold text-[#F5B942]">
                        Stage {String(idx + 1).padStart(2, '0')} · #{lesson.id}
                      </span>
                    )}

                    <StatusBadge status={lesson.status} />

                    <span className="inline-flex items-center gap-1 text-slate-400">
                      {isWeb ? (
                        <PixelBoltIcon className="w-3 h-3" />
                      ) : (
                        <PixelPythonIcon className="w-3 h-3" />
                      )}
                      <span>{isWeb ? 'Web & AI' : 'Python 3.13'}</span>
                    </span>

                    {lesson.flagged && (
                      <span className="inline-flex items-center gap-1 text-[#F45D78] font-medium">
                        <PixelFlagIcon className="w-3 h-3" />
                        <span>Flagged</span>
                      </span>
                    )}

                    {lesson.hasNotes && (
                      <span className="inline-flex items-center gap-1 text-[#38BDF8] font-medium">
                        <StickyNote className="w-3 h-3" />
                        <span>Notes</span>
                      </span>
                    )}
                  </div>

                  <h3
                    className={`text-base font-semibold transition ${
                      isBoss
                        ? 'text-[#F5B942] group-hover:text-amber-200'
                        : 'text-[#F8FAFC] group-hover:text-[#F5B942]'
                    }`}
                  >
                    {lesson.title}
                  </h3>

                  <p className="text-xs sm:text-[13px] text-slate-400 leading-relaxed">
                    {lesson.objective}
                  </p>
                </div>

                <div className="flex md:flex-col items-center md:items-end justify-between gap-2 shrink-0 border-t md:border-t-0 border-white/[0.06] pt-3 md:pt-0">
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-semibold ${
                      isBoss ? 'text-[#F5B942]' : 'text-[#2DD4A0]'
                    }`}
                  >
                    <PixelCoinIcon className="w-3.5 h-3.5" />
                    <span>+{lesson.xp} XP</span>
                  </span>
                  <span
                    className={`px-3 py-1.5 rounded-md text-xs font-semibold transition ${
                      isBoss
                        ? 'bg-[#F45D78] group-hover:bg-[#F5B942] text-[#0D1017]'
                        : 'bg-[#1C2230] group-hover:bg-[#F5B942] text-slate-200 group-hover:text-[#0D1017]'
                    }`}
                  >
                    {lesson.status === 'COMPLETED'
                      ? 'Replay →'
                      : lesson.status === 'IN_PROGRESS'
                        ? 'Resume →'
                        : isBoss
                          ? 'Challenge Boss →'
                          : 'Play →'}
                  </span>
                </div>
              </button>
            );
          })}

          {/* Campfire [INSIGHT] Rest-Site Card */}
          {insight && (
            <div id="module-campfire" ref={campfireRef} className="rpg-panel-amethyst transition">
              <button
                type="button"
                onClick={() => setInsightExpanded((prev) => !prev)}
                aria-expanded={insightExpanded}
                className="w-full text-left p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer hover:bg-white/[0.02] transition rounded-lg"
              >
                <div className="space-y-2 flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-2.5 text-xs">
                    <span className="inline-flex items-center gap-1.5 font-semibold px-2.5 py-0.5 rounded-md bg-[#F5B942]/15 text-[#F5B942]">
                      <PixelCampfireIcon className="w-3.5 h-3.5" />
                      <span>Campfire [Insight]</span>
                    </span>
                    <span className="inline-flex items-center gap-1 text-[#A78BFA] font-medium">
                      <Share2 className="w-3.5 h-3.5" />
                      <span>Reflect &amp; Share {hasBossAngle ? '• 2 Post Angles' : ''}</span>
                    </span>
                    {isModuleCleared && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
                        <PixelCheckIcon className="w-3 h-3" />
                        <span>Ready to post</span>
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-semibold text-[#F8FAFC] leading-snug">
                    {insight.linkedinAngle.hook}
                  </h3>

                  <p className="text-xs sm:text-[13px] text-slate-400 leading-relaxed">
                    Rest at the Realm Campfire: review {modNumberLabel} prompts
                    {hasBossAngle ? ', compare Concept vs. Boss Fight post angles,' : ''} and copy
                    a clean LinkedIn post outline.
                  </p>
                </div>

                <div className="flex md:flex-col items-center md:items-end justify-between gap-2 shrink-0">
                  <span className="text-[11px] font-medium text-[#A78BFA]">Rest Site</span>
                  <span
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition ${
                      insightExpanded
                        ? 'bg-[#F5B942] text-[#0D1017]'
                        : 'bg-[#1C2230] text-[#F5B942]'
                    }`}
                  >
                    <span>{insightExpanded ? 'Close Campfire' : 'Open Campfire'}</span>
                    {insightExpanded ? (
                      <ChevronUp className="w-3.5 h-3.5" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5" />
                    )}
                  </span>
                </div>
              </button>

              {insightExpanded && activeAngle && (
                <div className="px-4 sm:px-5 pb-5 pt-4 border-t border-white/[0.08] space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    {hasBossAngle ? (
                      <div className="inline-flex bg-[#0D1017] p-1 rounded-md border border-white/[0.08] gap-1 self-start">
                        <button
                          type="button"
                          onClick={() => setSelectedAngleTab('concept')}
                          className={`px-3 py-1.5 rounded text-xs font-medium cursor-pointer transition ${
                            selectedAngleTab === 'concept'
                              ? 'bg-[#38BDF8] text-[#0D1017] font-semibold'
                              : 'text-slate-400 hover:text-white'
                          }`}
                        >
                          1. Module Concept Post
                        </button>
                        <button
                          type="button"
                          onClick={() => setSelectedAngleTab('boss')}
                          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium cursor-pointer transition ${
                            selectedAngleTab === 'boss'
                              ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                              : 'text-slate-300 hover:text-white'
                          }`}
                        >
                          <PixelSkullIcon className="w-3 h-3" />
                          <span>2. Boss Fight Post</span>
                        </button>
                      </div>
                    ) : (
                      <div className="text-xs text-slate-400">
                        Share a concrete Python 3.13 insight from this realm.
                      </div>
                    )}

                    <button
                      type="button"
                      onClick={(e) =>
                        handleCopyOutline(
                          e,
                          activeAngle,
                          selectedAngleTab === 'boss' && hasBossAngle ? 'boss' : 'concept'
                        )
                      }
                      className={`inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold cursor-pointer shrink-0 ${
                        copiedAngle ===
                        (selectedAngleTab === 'boss' && hasBossAngle ? 'boss' : 'concept')
                          ? 'rpg-btn-emerald'
                          : 'rpg-btn-gold'
                      }`}
                    >
                      {copiedAngle ===
                      (selectedAngleTab === 'boss' && hasBossAngle ? 'boss' : 'concept') ? (
                        <>
                          <Check className="w-3.5 h-3.5" />
                          <span>Copied Outline!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>
                            Copy {selectedAngleTab === 'boss' && hasBossAngle ? 'Boss ' : ''}Post
                            Outline
                          </span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-1.5">
                        <div className="text-xs font-semibold text-[#38BDF8]">
                          {selectedAngleTab === 'boss' && hasBossAngle
                            ? 'Boss Build Hook'
                            : 'LinkedIn Hook / Common Mistake'}
                        </div>
                        <p className="text-xs sm:text-[13px] text-[#F8FAFC] leading-relaxed font-medium">
                          {activeAngle.hook}
                        </p>
                      </div>

                      <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-1.5">
                        <div className="text-xs font-semibold text-[#2DD4A0]">
                          {selectedAngleTab === 'boss' && hasBossAngle
                            ? 'Engineering Takeaway'
                            : 'What Modern Python Solves'}
                        </div>
                        <p className="text-xs sm:text-[13px] text-slate-300 leading-relaxed">
                          {activeAngle.pythonInsight}
                        </p>
                      </div>

                      <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 space-y-2">
                        <div className="text-xs font-semibold text-[#F5B942]">Reflection Check</div>
                        <ul className="space-y-1.5">
                          {insight.reflectionPrompts.map((prompt, idx) => (
                            <li
                              key={idx}
                              className="text-xs sm:text-[13px] text-slate-300 leading-relaxed flex items-start gap-2"
                            >
                              <span className="font-semibold text-[#F5B942] shrink-0">
                                {idx + 1}.
                              </span>
                              <span>{prompt}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-4 flex flex-col justify-between">
                      <div className="space-y-2">
                        <div className="text-xs font-semibold text-[#F5B942]">
                          Code Comparison (Before / After)
                        </div>
                        <pre className="text-[13px] leading-[1.6] font-mono text-[#E2E8F0] overflow-x-auto whitespace-pre-wrap bg-[#0B0E14] border border-white/[0.07] rounded-lg p-3.5">
                          {activeAngle.codeComparison.trim()}
                        </pre>
                      </div>
                      <div className="pt-3 mt-3 border-t border-white/[0.06] text-xs text-slate-400">
                        Tip: pair this snippet with one real bug you fixed in this realm.
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};
