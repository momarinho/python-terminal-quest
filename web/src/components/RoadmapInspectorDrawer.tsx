import React, { useEffect } from 'react';
import { ArrowRight, CheckCircle2, Lock, Sparkles, Unlock, X } from 'lucide-react';
import {
  PixelBoltIcon,
  PixelCheckIcon,
  PixelCoinIcon,
  PixelCrownIcon,
  PixelFlagIcon,
  PixelGateIcon,
  PixelPythonIcon,
  PixelSkullIcon,
} from './PixelIcons';
import { splitModuleTitle } from '../pages/DashboardPage';
import type { LessonSummary, ModuleGroup, PortfolioProject } from '../types/api';

export type SelectedRoadmapNode =
  | { kind: 'lesson'; lesson: LessonSummary; module: ModuleGroup }
  | { kind: 'module'; module: ModuleGroup }
  | { kind: 'gate'; project: PortfolioProject };

interface RoadmapInspectorDrawerProps {
  selected: SelectedRoadmapNode | null;
  onClose: () => void;
  onSelectLesson: (lessonId: string) => void;
  onSelectModule: (moduleId: string) => void;
  onNavigateProjects: () => void;
}

export const RoadmapInspectorDrawer: React.FC<RoadmapInspectorDrawerProps> = ({
  selected,
  onClose,
  onSelectLesson,
  onSelectModule,
  onNavigateProjects,
}) => {
  useEffect(() => {
    if (!selected) {
      return;
    }
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selected, onClose]);

  if (!selected) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end"
      role="dialog"
      aria-modal="true"
      aria-label="Roadmap Node Inspector"
    >
      <button
        type="button"
        aria-label="Close inspector"
        onClick={onClose}
        className="flex-1 bg-black/60 backdrop-blur-[2px] cursor-pointer focus-visible:outline-none"
      />

      <aside className="w-full max-w-md bg-[#121620] border-l border-white/[0.1] shadow-2xl flex flex-col h-full overflow-hidden">
        <div className="px-5 py-3.5 border-b border-white/[0.08] bg-[#0D1017] flex items-center justify-between gap-2 shrink-0">
          <div className="flex items-center gap-2 text-xs font-semibold text-[#F5B942]">
            <Sparkles className="w-3.5 h-3.5" />
            <span>
              {selected.kind === 'lesson'
                ? 'Stage Inspector'
                : selected.kind === 'module'
                  ? 'Realm Inspector'
                  : 'Portfolio Gate'}
            </span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-slate-400 hover:text-white hover:bg-[#1C2230] text-xs font-medium cursor-pointer transition"
          >
            <span>Esc</span>
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {selected.kind === 'lesson' && (
            <LessonInspectorBody
              lesson={selected.lesson}
              module={selected.module}
              onSelectLesson={onSelectLesson}
              onSelectModule={onSelectModule}
            />
          )}

          {selected.kind === 'module' && (
            <ModuleInspectorBody
              module={selected.module}
              onSelectLesson={onSelectLesson}
              onSelectModule={onSelectModule}
            />
          )}

          {selected.kind === 'gate' && (
            <GateInspectorBody
              project={selected.project}
              onNavigateProjects={onNavigateProjects}
            />
          )}
        </div>
      </aside>
    </div>
  );
};

const LessonInspectorBody: React.FC<{
  lesson: LessonSummary;
  module: ModuleGroup;
  onSelectLesson: (lessonId: string) => void;
  onSelectModule: (moduleId: string) => void;
}> = ({ lesson, module, onSelectLesson, onSelectModule }) => {
  const [modNum, modTitle] = splitModuleTitle(module.title);
  const isBoss = lesson.kind === 'BOSS';
  const isWeb = lesson.runtime === 'WEB_INTEGRATION';
  const isDone = lesson.status === 'COMPLETED';
  const isInProgress = lesson.status === 'IN_PROGRESS';

  return (
    <>
      <div className="space-y-1.5">
        <div className="text-xs font-medium text-[#38BDF8]">
          {modNum} · {modTitle}
        </div>
        <h2 className="text-lg font-semibold text-[#F8FAFC] leading-snug">{lesson.title}</h2>
      </div>

      <div className="flex flex-wrap gap-2 text-xs">
        <span
          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md font-medium ${
            isBoss ? 'bg-[#F45D78]/15 text-[#F45D78]' : 'bg-white/[0.05] text-slate-300'
          }`}
        >
          {isBoss &&
            (isDone ? (
              <PixelCrownIcon className="w-3.5 h-3.5" />
            ) : (
              <PixelSkullIcon className="w-3.5 h-3.5" />
            ))}
          <span>{isBoss ? 'Boss Fight' : 'Standard'}</span>
        </span>

        <span
          className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium ${
            isWeb ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]' : 'bg-[#38BDF8]/12 text-[#38BDF8]'
          }`}
        >
          {isWeb ? (
            <PixelBoltIcon className="w-3.5 h-3.5" />
          ) : (
            <PixelPythonIcon className="w-3.5 h-3.5" />
          )}
          <span>{isWeb ? 'Web & AI' : 'Python 3.13'}</span>
        </span>

        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium bg-[#F5B942]/15 text-[#F5B942]">
          <PixelCoinIcon className="w-3.5 h-3.5" />
          <span>+{lesson.xp} XP</span>
        </span>

        <span
          className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium ${
            isDone
              ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]'
              : isInProgress
                ? 'bg-[#F5B942]/15 text-[#F5B942]'
                : 'bg-white/[0.05] text-slate-400'
          }`}
        >
          {isDone && <PixelCheckIcon className="w-3 h-3" />}
          <span>{isDone ? 'Completed' : isInProgress ? 'In Progress' : 'Not Started'}</span>
        </span>

        {lesson.flagged && (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium bg-[#F45D78]/15 text-[#F45D78]">
            <PixelFlagIcon className="w-3 h-3" />
            <span>Flagged</span>
          </span>
        )}
      </div>

      <div className="rpg-panel p-4 space-y-2.5">
        <div className="text-xs font-semibold text-slate-400">Stage Objective</div>
        <p className="text-sm text-slate-200 leading-relaxed">{lesson.objective}</p>
        {lesson.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {lesson.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-[#BAE6FD]"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3 text-center">
        <div className="rpg-panel p-3 bg-[#0D1017]">
          <div className="text-base font-bold text-[#F8FAFC]">{lesson.attempts}</div>
          <div className="text-xs text-slate-400 mt-0.5">Run attempts</div>
        </div>
        <div className="rpg-panel p-3 bg-[#0D1017]">
          <div className="text-base font-bold text-[#F5B942]">
            {lesson.hintsRevealed}/{lesson.totalHints}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">Hints used</div>
        </div>
      </div>

      <div className="space-y-2 pt-2">
        <button
          type="button"
          onClick={() => onSelectLesson(lesson.id)}
          className="w-full py-2.5 px-4 text-xs font-semibold rpg-btn-gold flex items-center justify-center gap-2 cursor-pointer"
        >
          <span>Play Stage</span>
          <ArrowRight className="w-4 h-4" />
        </button>

        <button
          type="button"
          onClick={() => onSelectModule(module.id)}
          className="w-full py-2.5 px-4 rounded-md bg-[#1C2230] hover:bg-[#252D40] text-slate-200 text-xs font-medium flex items-center justify-center gap-2 cursor-pointer transition"
        >
          <span>Open Realm ({modNum})</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </>
  );
};

const ModuleInspectorBody: React.FC<{
  module: ModuleGroup;
  onSelectLesson: (lessonId: string) => void;
  onSelectModule: (moduleId: string) => void;
}> = ({ module, onSelectLesson, onSelectModule }) => {
  const [modNum, modTitle] = splitModuleTitle(module.title);
  const pct =
    module.totalLessons === 0
      ? 0
      : Math.round((module.completedLessons / module.totalLessons) * 100);
  const isDone = module.totalLessons > 0 && module.completedLessons === module.totalLessons;
  const isWeb = module.lessons.some((l) => l.runtime === 'WEB_INTEGRATION');
  const boss = module.lessons.find((l) => l.kind === 'BOSS');

  return (
    <>
      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="font-semibold text-[#F5B942]">{modNum}</span>
          <span
            className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-medium ${
              isWeb ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]' : 'bg-[#38BDF8]/12 text-[#38BDF8]'
            }`}
          >
            {isWeb ? (
              <PixelBoltIcon className="w-3 h-3" />
            ) : (
              <PixelPythonIcon className="w-3 h-3" />
            )}
            <span>{isWeb ? 'Web & AI' : 'Python 3.13'}</span>
          </span>
          {boss && (
            <span
              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md font-medium ${
                boss.status === 'COMPLETED'
                  ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]'
                  : 'bg-[#F45D78]/15 text-[#F45D78]'
              }`}
            >
              {boss.status === 'COMPLETED' ? (
                <PixelCrownIcon className="w-3 h-3" />
              ) : (
                <PixelSkullIcon className="w-3 h-3" />
              )}
              <span>{boss.status === 'COMPLETED' ? 'Boss Slain' : 'Boss Active'}</span>
            </span>
          )}
        </div>
        <h2 className="text-lg font-semibold text-[#F8FAFC] leading-snug">{modTitle}</h2>
      </div>

      <div className="rpg-panel p-4 bg-[#151923] space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400">
            {module.completedLessons}/{module.totalLessons} stages cleared
          </span>
          <span className={`font-semibold ${isDone ? 'text-[#2DD4A0]' : 'text-[#F5B942]'}`}>
            {pct}% · {module.earnedXp}/{module.totalXp} XP
          </span>
        </div>
        <div className="w-full h-2 rpg-bar-track">
          <div
            className={`h-full ${isDone ? 'rpg-bar-fill' : 'rpg-bar-fill-gold'}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      <div className="space-y-2">
        <div className="text-xs font-semibold text-slate-400">Stages in Realm</div>
        <div className="space-y-1.5">
          {module.lessons.map((lesson) => {
            const done = lesson.status === 'COMPLETED';
            const bossItem = lesson.kind === 'BOSS';
            return (
              <button
                key={lesson.id}
                type="button"
                onClick={() => onSelectLesson(lesson.id)}
                className="w-full text-left px-3 py-2 rounded-md bg-[#0D1017] hover:bg-[#1C2230] border border-white/[0.06] flex items-center justify-between gap-2 text-xs cursor-pointer transition"
              >
                <span className="flex items-center gap-2 min-w-0">
                  {done ? (
                    <PixelCheckIcon className="w-3.5 h-3.5 shrink-0" />
                  ) : bossItem ? (
                    <PixelSkullIcon className="w-3.5 h-3.5 shrink-0" />
                  ) : (
                    <PixelPythonIcon className="w-3.5 h-3.5 shrink-0" />
                  )}
                  <span className="truncate text-slate-200">{lesson.title}</span>
                </span>
                <span className="text-[#F5B942] font-medium shrink-0">+{lesson.xp} XP</span>
              </button>
            );
          })}
        </div>
      </div>

      <button
        type="button"
        onClick={() => onSelectModule(module.id)}
        className="w-full py-2.5 px-4 text-xs font-semibold rpg-btn-gold flex items-center justify-center gap-2 cursor-pointer"
      >
        <span>Open Realm Overview</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </>
  );
};

const GateInspectorBody: React.FC<{
  project: PortfolioProject;
  onNavigateProjects: () => void;
}> = ({ project, onNavigateProjects }) => {
  const isShipped = project.progress.status === 'COMPLETED';
  const isUnlocked = project.milestoneUnlocked;
  const totalTasks = project.sprints.reduce((acc, s) => acc + s.items.length, 0);
  const doneTasks = project.progress.completedChecklistIds.length;

  return (
    <>
      <div className="space-y-2">
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="inline-flex items-center gap-1.5 font-semibold text-[#A78BFA]">
            <PixelGateIcon className="w-3.5 h-3.5" />
            <span>Portfolio Gate #{project.order}</span>
          </span>
          {isShipped ? (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
              <CheckCircle2 className="w-3 h-3" />
              <span>Shipped</span>
            </span>
          ) : isUnlocked ? (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
              <Unlock className="w-3 h-3" />
              <span>Unlocked</span>
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F5B942]/15 text-[#F5B942] font-medium">
              <Lock className="w-3 h-3" />
              <span>
                Preview ({project.completedPrerequisiteModules}/{project.requiredModulesCompleted})
              </span>
            </span>
          )}
        </div>
        <h2 className="text-lg font-semibold text-[#F8FAFC] leading-snug">{project.title}</h2>
        <div className="text-xs text-slate-400">{project.milestoneLabel}</div>
      </div>

      <div className="rpg-panel p-4 space-y-2">
        <div className="text-xs font-semibold text-slate-400">Business Context</div>
        <p className="text-sm text-slate-200 leading-relaxed">{project.businessContext}</p>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {project.techStack.map((tech) => (
          <span
            key={tech}
            className="px-2.5 py-1 rounded-md text-xs bg-white/[0.05] text-[#BAE6FD]"
          >
            {tech}
          </span>
        ))}
      </div>

      <div className="rpg-panel p-3.5 flex items-center justify-between text-xs">
        <span className="text-slate-400">Sprint checklist progress</span>
        <span className="font-semibold text-[#2DD4A0]">
          {doneTasks}/{totalTasks} tasks
        </span>
      </div>

      <button
        type="button"
        onClick={onNavigateProjects}
        className="w-full py-2.5 px-4 text-xs font-semibold rpg-btn-emerald flex items-center justify-center gap-2 cursor-pointer"
      >
        <span>Open Portfolio Guild</span>
        <ArrowRight className="w-4 h-4" />
      </button>
    </>
  );
};
