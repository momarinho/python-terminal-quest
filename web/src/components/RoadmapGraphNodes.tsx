import React, { useCallback, useLayoutEffect, useRef, useState } from 'react';
import { Lock, Unlock } from 'lucide-react';
import { HeroCompanionSprite } from './HeroCompanion';
import {
  PixelBoltIcon,
  PixelCheckIcon,
  PixelCrownIcon,
  PixelFlagIcon,
  PixelGateIcon,
  PixelPythonIcon,
  PixelSkullIcon,
} from './PixelIcons';
import { splitModuleTitle } from '../pages/DashboardPage';
import type { LessonSummary, ModuleGroup, PortfolioProject } from '../types/api';

interface MeasuredEdge {
  id: string;
  path: string;
  completed: boolean;
  isBoss: boolean;
  ex: number;
  ey: number;
}

interface SvgGeometry {
  width: number;
  height: number;
  edges: MeasuredEdge[];
}

interface ModuleBranchBandProps {
  module: ModuleGroup;
  moduleOrder: number;
  lessons: LessonSummary[];
  compact: boolean;
  isActiveMarker: boolean;
  heroTier: number;
  hoveredLessonId: string | null;
  selectedLessonId: string | null;
  selectedModuleId: string | null;
  onHoverLesson: (lessonId: string | null) => void;
  onClickLesson: (lesson: LessonSummary, module: ModuleGroup) => void;
  onClickModule: (module: ModuleGroup) => void;
}

function splitLeftRight(
  lessons: LessonSummary[],
  moduleOrder: number
): { left: LessonSummary[]; right: LessonSummary[] } {
  if (lessons.length === 1) {
    return moduleOrder % 2 === 1 ? { left: lessons, right: [] } : { left: [], right: lessons };
  }
  const left: LessonSummary[] = [];
  const right: LessonSummary[] = [];
  lessons.forEach((lesson, idx) => {
    if (idx % 2 === 0) {
      left.push(lesson);
    } else {
      right.push(lesson);
    }
  });
  return { left, right };
}

function buildCurvePath(
  containerRect: DOMRect,
  hubRect: DOMRect,
  leafRect: DOMRect
): { path: string; ex: number; ey: number } {
  const leafCenterY = leafRect.top - containerRect.top + leafRect.height / 2;
  const hubCenterY = hubRect.top - containerRect.top + hubRect.height / 2;

  if (leafRect.right <= hubRect.left + 8) {
    const sx = hubRect.left - containerRect.left;
    const sy = hubCenterY;
    const ex = leafRect.right - containerRect.left;
    const ey = leafCenterY;
    const bend = Math.max(24, Math.abs(sx - ex) * 0.55);
    return {
      path: `M ${sx} ${sy} C ${sx - bend} ${sy}, ${ex + bend} ${ey}, ${ex} ${ey}`,
      ex,
      ey,
    };
  }

  if (leafRect.left >= hubRect.right - 8) {
    const sx = hubRect.right - containerRect.left;
    const sy = hubCenterY;
    const ex = leafRect.left - containerRect.left;
    const ey = leafCenterY;
    const bend = Math.max(24, Math.abs(ex - sx) * 0.55);
    return {
      path: `M ${sx} ${sy} C ${sx + bend} ${sy}, ${ex - bend} ${ey}, ${ex} ${ey}`,
      ex,
      ey,
    };
  }

  const sx = hubRect.left - containerRect.left + 16;
  const sy = hubRect.bottom - containerRect.top;
  const ex = leafRect.left - containerRect.left;
  const ey = leafCenterY;
  const midX = sx + Math.max(16, (ex - sx) * 0.45);
  return {
    path: `M ${sx} ${sy} C ${sx} ${ey}, ${midX} ${ey}, ${ex} ${ey}`,
    ex,
    ey,
  };
}

export const ModuleBranchBand: React.FC<ModuleBranchBandProps> = ({
  module,
  moduleOrder,
  lessons,
  compact,
  isActiveMarker,
  heroTier,
  hoveredLessonId,
  selectedLessonId,
  selectedModuleId,
  onHoverLesson,
  onClickLesson,
  onClickModule,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const hubRef = useRef<HTMLButtonElement>(null);
  const desktopLeafRefs = useRef<Map<string, HTMLButtonElement>>(new Map());
  const mobileLeafRefs = useRef<Map<string, HTMLButtonElement>>(new Map());
  const [geometry, setGeometry] = useState<SvgGeometry>({ width: 0, height: 0, edges: [] });

  const [modNumLabel, modCleanTitle] = splitModuleTitle(module.title);
  const isDone = module.totalLessons > 0 && module.completedLessons === module.totalLessons;
  const isActive = !isDone && module.completedLessons > 0;
  const isWeb = module.lessons.some((l) => l.runtime === 'WEB_INTEGRATION');
  const isHubSelected = selectedModuleId === module.id;

  const { left: leftLessons, right: rightLessons } = splitLeftRight(lessons, moduleOrder);

  const setLeafRef = useCallback(
    (targetMap: React.MutableRefObject<Map<string, HTMLButtonElement>>, lessonId: string) => {
      return (el: HTMLButtonElement | null) => {
        if (el) {
          targetMap.current.set(lessonId, el);
        } else {
          targetMap.current.delete(lessonId);
        }
      };
    },
    []
  );

  const measureEdges = useCallback(() => {
    const container = containerRef.current;
    const hub = hubRef.current;
    if (!container || !hub || compact || lessons.length === 0) {
      setGeometry((prev) => (prev.edges.length === 0 ? prev : { width: 0, height: 0, edges: [] }));
      return;
    }

    const containerRect = container.getBoundingClientRect();
    const hubRect = hub.getBoundingClientRect();
    const nextEdges: MeasuredEdge[] = [];

    for (const lesson of lessons) {
      const desktopEl = desktopLeafRefs.current.get(lesson.id);
      const mobileEl = mobileLeafRefs.current.get(lesson.id);
      const desktopRect = desktopEl?.getBoundingClientRect();
      const mobileRect = mobileEl?.getBoundingClientRect();
      const leafRect =
        desktopRect && desktopRect.width > 0
          ? desktopRect
          : mobileRect && mobileRect.width > 0
            ? mobileRect
            : null;
      if (!leafRect) {
        continue;
      }
      const { path, ex, ey } = buildCurvePath(containerRect, hubRect, leafRect);
      nextEdges.push({
        id: lesson.id,
        path,
        completed: lesson.status === 'COMPLETED',
        isBoss: lesson.kind === 'BOSS',
        ex,
        ey,
      });
    }

    setGeometry({
      width: containerRect.width,
      height: containerRect.height,
      edges: nextEdges,
    });
  }, [compact, lessons]);

  useLayoutEffect(() => {
    measureEdges();
    const container = containerRef.current;
    if (!container || compact) {
      return;
    }

    let cancelled = false;
    const observer = new ResizeObserver(() => {
      if (!cancelled) {
        measureEdges();
      }
    });
    observer.observe(container);
    if (hubRef.current) {
      observer.observe(hubRef.current);
    }

    if (typeof document !== 'undefined' && 'fonts' in document) {
      document.fonts.ready.then(() => {
        if (!cancelled) {
          measureEdges();
        }
      });
    }

    return () => {
      cancelled = true;
      observer.disconnect();
    };
  }, [measureEdges, compact]);

  return (
    <div ref={containerRef} className="relative py-2">
      {/* Real SVG Curved Dashed Edges Overlay */}
      {!compact && geometry.width > 0 && geometry.edges.length > 0 && (
        <svg
          width={geometry.width}
          height={geometry.height}
          viewBox={`0 0 ${geometry.width} ${geometry.height}`}
          className="pointer-events-none absolute inset-0 z-[1] overflow-visible"
          aria-hidden="true"
        >
          {geometry.edges.map((edge) => {
            const isHighlighted = hoveredLessonId === edge.id || selectedLessonId === edge.id;
            const stroke = isHighlighted
              ? '#F5B942'
              : edge.completed
                ? '#2DD4A0'
                : edge.isBoss
                  ? '#F45D78'
                  : '#64748B';

            return (
              <g key={edge.id}>
                <path
                  d={edge.path}
                  fill="none"
                  stroke={stroke}
                  strokeOpacity={
                    isHighlighted ? 0.95 : edge.completed ? 0.65 : edge.isBoss ? 0.55 : 0.45
                  }
                  strokeWidth={isHighlighted ? 2.25 : 1.5}
                  strokeDasharray="5 5"
                />
                <circle
                  cx={edge.ex}
                  cy={edge.ey}
                  r={isHighlighted ? 3.5 : 2.5}
                  fill={stroke}
                  fillOpacity={isHighlighted ? 1 : 0.75}
                />
              </g>
            );
          })}
        </svg>
      )}

      {compact ? (
        <div className="relative z-10 flex justify-start pl-10 sm:pl-14 lg:justify-center lg:pl-0">
          <ModuleSpineNode
            ref={hubRef}
            modNumLabel={modNumLabel}
            modCleanTitle={modCleanTitle}
            completedLessons={module.completedLessons}
            totalLessons={module.totalLessons}
            isDone={isDone}
            isActive={isActive}
            isWeb={isWeb}
            isActiveMarker={isActiveMarker}
            heroTier={heroTier}
            isSelected={isHubSelected}
            showPorts={false}
            onClick={() => onClickModule(module)}
          />
        </div>
      ) : (
        <div className="relative z-10 flex flex-col gap-3 pl-10 sm:pl-14 lg:pl-0 lg:grid lg:grid-cols-[1fr_264px_1fr] lg:items-center lg:gap-x-10">
          {/* Desktop Left Branch Column */}
          <div className="hidden lg:flex flex-col items-end gap-2.5">
            {leftLessons.map((lesson) => (
              <LessonLeafButton
                key={lesson.id}
                ref={setLeafRef(desktopLeafRefs, lesson.id)}
                lesson={lesson}
                highlighted={hoveredLessonId === lesson.id || selectedLessonId === lesson.id}
                onMouseEnter={() => onHoverLesson(lesson.id)}
                onMouseLeave={() => onHoverLesson(null)}
                onClick={() => onClickLesson(lesson, module)}
              />
            ))}
          </div>

          {/* Central Spine Module Node */}
          <div className="flex justify-start lg:justify-center">
            <ModuleSpineNode
              ref={hubRef}
              modNumLabel={modNumLabel}
              modCleanTitle={modCleanTitle}
              completedLessons={module.completedLessons}
              totalLessons={module.totalLessons}
              isDone={isDone}
              isActive={isActive}
              isWeb={isWeb}
              isActiveMarker={isActiveMarker}
              heroTier={heroTier}
              isSelected={isHubSelected}
              showPorts
              onClick={() => onClickModule(module)}
            />
          </div>

          {/* Desktop Right Branch Column */}
          <div className="hidden lg:flex flex-col items-start gap-2.5">
            {rightLessons.map((lesson) => (
              <LessonLeafButton
                key={lesson.id}
                ref={setLeafRef(desktopLeafRefs, lesson.id)}
                lesson={lesson}
                highlighted={hoveredLessonId === lesson.id || selectedLessonId === lesson.id}
                onMouseEnter={() => onHoverLesson(lesson.id)}
                onMouseLeave={() => onHoverLesson(null)}
                onClick={() => onClickLesson(lesson, module)}
              />
            ))}
          </div>

          {/* Mobile/Tablet Unified Right-Side Branch Column */}
          <div className="flex flex-col items-start gap-2 pl-6 sm:pl-10 lg:hidden">
            {lessons.map((lesson) => (
              <LessonLeafButton
                key={`mobile-${lesson.id}`}
                ref={setLeafRef(mobileLeafRefs, lesson.id)}
                lesson={lesson}
                highlighted={hoveredLessonId === lesson.id || selectedLessonId === lesson.id}
                onMouseEnter={() => onHoverLesson(lesson.id)}
                onMouseLeave={() => onHoverLesson(null)}
                onClick={() => onClickLesson(lesson, module)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

interface ModuleSpineNodeProps {
  modNumLabel: string;
  modCleanTitle: string;
  completedLessons: number;
  totalLessons: number;
  isDone: boolean;
  isActive: boolean;
  isWeb: boolean;
  isActiveMarker: boolean;
  heroTier: number;
  isSelected: boolean;
  showPorts: boolean;
  onClick: () => void;
}

const ModuleSpineNode = React.forwardRef<HTMLButtonElement, ModuleSpineNodeProps>(
  (
    {
      modNumLabel,
      modCleanTitle,
      completedLessons,
      totalLessons,
      isDone,
      isActive,
      isWeb,
      isActiveMarker,
      heroTier,
      isSelected,
      showPorts,
      onClick,
    },
    ref
  ) => (
    <button
      ref={ref}
      type="button"
      onClick={onClick}
      className={`relative w-full max-w-[264px] px-4 py-3 text-left rounded-lg border transition cursor-pointer focus-visible:outline-none ${
        isDone
          ? 'bg-[#0F241F] border-[#2DD4A0]/55 text-[#F8FAFC] hover:bg-[#132E27]'
          : isActive || isActiveMarker || isSelected
            ? 'bg-[#231D11] border-[#F5B942]/70 text-[#F8FAFC] hover:bg-[#2B2415]'
            : 'bg-[#151923] border-white/[0.1] text-[#F8FAFC] hover:bg-[#1C2230] hover:border-[#F5B942]/50'
      } ${isSelected ? 'ring-2 ring-[#F5B942]/60 ring-offset-2 ring-offset-[#0D1017]' : ''}`}
    >
      {/* Active-Module Hero Companion Avatar Marker */}
      {isActiveMarker && (
        <span
          title="Your Hero's current active realm"
          className="absolute -top-3.5 -right-2.5 z-20 inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md bg-[#0D1017] border border-[#F5B942]/70 shadow-lg"
        >
          <HeroCompanionSprite tier={heroTier} className="w-5 h-5" />
          <span className="text-[10px] font-semibold text-[#F5B942]">Here</span>
        </span>
      )}

      {showPorts && (
        <>
          <span
            aria-hidden="true"
            className={`hidden lg:block absolute -left-1 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full ${
              isDone ? 'bg-[#2DD4A0]' : isActive ? 'bg-[#F5B942]' : 'bg-slate-500'
            }`}
          />
          <span
            aria-hidden="true"
            className={`hidden lg:block absolute -right-1 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full ${
              isDone ? 'bg-[#2DD4A0]' : isActive ? 'bg-[#F5B942]' : 'bg-slate-500'
            }`}
          />
        </>
      )}

      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="flex items-center gap-1.5 min-w-0">
          <span className={`text-xs font-semibold ${isDone ? 'text-[#2DD4A0]' : 'text-[#F5B942]'}`}>
            {modNumLabel}
          </span>
          {isWeb && (
            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-[#2DD4A0]/12 text-[#2DD4A0]">
              <PixelBoltIcon className="w-2.5 h-2.5" />
              <span>Web & AI</span>
            </span>
          )}
        </div>

        <span
          className={`inline-flex items-center gap-1 text-xs font-medium shrink-0 ${
            isDone ? 'text-[#2DD4A0]' : 'text-slate-400'
          }`}
        >
          {isDone && <PixelCheckIcon className="w-3 h-3" />}
          <span>
            {completedLessons}/{totalLessons}
          </span>
        </span>
      </div>

      <div className="text-[13px] font-semibold leading-snug line-clamp-2 text-[#F8FAFC]">
        {modCleanTitle}
      </div>
    </button>
  )
);
ModuleSpineNode.displayName = 'ModuleSpineNode';

interface LessonLeafButtonProps {
  lesson: LessonSummary;
  highlighted: boolean;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
  onClick: () => void;
}

const LessonLeafButton = React.forwardRef<HTMLButtonElement, LessonLeafButtonProps>(
  ({ lesson, highlighted, onMouseEnter, onMouseLeave, onClick }, ref) => {
    const isDone = lesson.status === 'COMPLETED';
    const isInProgress = lesson.status === 'IN_PROGRESS';
    const isBoss = lesson.kind === 'BOSS';

    return (
      <button
        ref={ref}
        type="button"
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onFocus={onMouseEnter}
        onBlur={onMouseLeave}
        onClick={onClick}
        className={`group w-full min-w-[250px] max-w-[280px] px-3 py-2 rounded-lg border text-left transition cursor-pointer flex items-center justify-between gap-2 focus-visible:outline-none ${
          highlighted
            ? 'border-[#F5B942] bg-[#1C2230] text-white'
            : isBoss
              ? isDone
                ? 'bg-[#0F241F] border-[#2DD4A0]/50 hover:border-[#F5B942]'
                : 'bg-[#21131C] border-[#F45D78]/55 hover:border-[#F5B942]'
              : isDone
                ? 'bg-[#0F241F] border-[#2DD4A0]/45 hover:border-[#2DD4A0]'
                : isInProgress
                  ? 'bg-[#231D11] border-[#F5B942]/55 hover:border-[#F5B942]'
                  : 'bg-[#151923] border-white/[0.08] hover:bg-[#1C2230] hover:border-[#F5B942]/55'
        }`}
      >
        <div className="flex items-start gap-2 min-w-0">
          <span className="mt-0.5 shrink-0">
            {isBoss ? (
              isDone ? (
                <PixelCrownIcon className="w-3.5 h-3.5" />
              ) : (
                <PixelSkullIcon className="w-3.5 h-3.5" />
              )
            ) : isDone ? (
              <PixelCheckIcon className="w-3.5 h-3.5" />
            ) : lesson.runtime === 'WEB_INTEGRATION' ? (
              <PixelBoltIcon className="w-3.5 h-3.5" />
            ) : (
              <PixelPythonIcon className="w-3.5 h-3.5" />
            )}
          </span>

          <span
            className={`text-[12.5px] leading-snug line-clamp-2 ${
              isBoss
                ? isDone
                  ? 'text-[#A7F3D0] font-medium'
                  : 'text-[#FDA4AF] font-medium'
                : isDone
                  ? 'text-[#D1FAE5]'
                  : 'text-[#F8FAFC]'
            }`}
          >
            {lesson.title}
          </span>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          {lesson.flagged && <PixelFlagIcon className="w-3 h-3 shrink-0" />}
          {isBoss && (
            <span
              className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                isDone ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]' : 'bg-[#F45D78]/15 text-[#F45D78]'
              }`}
            >
              Boss
            </span>
          )}
        </div>
      </button>
    );
  }
);
LessonLeafButton.displayName = 'LessonLeafButton';

interface GateLandmarkBandProps {
  project: PortfolioProject;
  compact: boolean;
  selected: boolean;
  onClick: () => void;
}

export const GateLandmarkBand: React.FC<GateLandmarkBandProps> = ({
  project,
  compact,
  selected,
  onClick,
}) => {
  const isShipped = project.progress.status === 'COMPLETED';
  const isUnlocked = project.milestoneUnlocked;
  const tags = project.techStack.slice(0, 4);
  const leftTags = tags.slice(0, 2);
  const rightTags = tags.slice(2, 4);

  return (
    <div className="relative py-3 z-10">
      {compact ? (
        <div className="flex justify-start pl-10 sm:pl-14 lg:justify-center lg:pl-0">
          <GateLandmarkButton
            project={project}
            isShipped={isShipped}
            isUnlocked={isUnlocked}
            selected={selected}
            onClick={onClick}
          />
        </div>
      ) : (
        <div className="flex flex-col gap-2.5 pl-10 sm:pl-14 lg:pl-0 lg:grid lg:grid-cols-[1fr_272px_1fr] lg:items-center lg:gap-x-0">
          <div className="hidden lg:flex flex-col items-end gap-1.5">
            {leftTags.map((tag) => (
              <div key={tag} className="flex items-center">
                <span className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300">
                  {tag}
                </span>
                <span className="w-8 border-t border-dashed border-[#A78BFA]/55" />
              </div>
            ))}
          </div>

          <div className="flex justify-start lg:justify-center">
            <GateLandmarkButton
              project={project}
              isShipped={isShipped}
              isUnlocked={isUnlocked}
              selected={selected}
              onClick={onClick}
            />
          </div>

          <div className="hidden lg:flex flex-col items-start gap-1.5">
            {rightTags.map((tag) => (
              <div key={tag} className="flex items-center">
                <span className="w-8 border-t border-dashed border-[#A78BFA]/55" />
                <span className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300">
                  {tag}
                </span>
              </div>
            ))}
          </div>

          <div className="flex flex-wrap gap-1.5 pl-6 sm:pl-10 lg:hidden">
            {tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const GateLandmarkButton: React.FC<{
  project: PortfolioProject;
  isShipped: boolean;
  isUnlocked: boolean;
  selected: boolean;
  onClick: () => void;
}> = ({ project, isShipped, isUnlocked, selected, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className={`w-full max-w-[272px] px-4 py-3 text-left rounded-lg border transition cursor-pointer focus-visible:outline-none ${
      isShipped
        ? 'bg-[#0F241F] border-[#2DD4A0]/55 hover:bg-[#132E27]'
        : isUnlocked
          ? 'bg-[#1B1630] border-[#F5B942]/65 hover:border-[#F5B942]'
          : 'bg-[#181429] border-[#A78BFA]/45 hover:border-[#F5B942]/65'
    } ${selected ? 'ring-2 ring-[#F5B942]/60 ring-offset-2 ring-offset-[#0D1017]' : ''}`}
  >
    <div className="flex items-center justify-between gap-2 mb-1">
      <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#A78BFA]">
        <PixelGateIcon className="w-3.5 h-3.5" />
        <span>Portfolio Gate #{project.order}</span>
      </span>

      {isShipped ? (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-[#2DD4A0]">
          <PixelCheckIcon className="w-3 h-3" />
          <span>Shipped</span>
        </span>
      ) : isUnlocked ? (
        <span className="inline-flex items-center gap-1 text-[11px] font-medium text-[#2DD4A0]">
          <Unlock className="w-3 h-3" />
          <span>Unlocked</span>
        </span>
      ) : (
        <span className="inline-flex items-center gap-1 text-[11px] text-slate-400">
          <Lock className="w-3 h-3" />
          <span>
            {project.completedPrerequisiteModules}/{project.requiredModulesCompleted}
          </span>
        </span>
      )}
    </div>

    <div className="text-[13px] font-semibold text-[#F8FAFC] leading-snug flex items-center gap-2">
      <PixelCrownIcon className="w-4 h-4 shrink-0" />
      <span className="line-clamp-2">{project.title}</span>
    </div>
  </button>
);
