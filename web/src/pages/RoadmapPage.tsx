import React, { useEffect, useMemo, useState } from 'react';
import { Layers, Network, RotateCcw } from 'lucide-react';
import { api } from '../api/client';
import { GateLandmarkBand, ModuleBranchBand } from '../components/RoadmapGraphNodes';
import {
  RoadmapInspectorDrawer,
  type SelectedRoadmapNode,
} from '../components/RoadmapInspectorDrawer';
import { TopNav } from '../components/TopNav';
import type {
  CurriculumResponse,
  LessonSummary,
  ModuleGroup,
  PortfolioProject,
} from '../types/api';

interface RoadmapPageProps {
  curriculum: CurriculumResponse;
  onSelectModule: (moduleId: string) => void;
  onSelectLesson?: (lessonId: string) => void;
  onNavigateWorldMap: () => void;
  onNavigateProjects: () => void;
  completedProjectsCount?: number;
  totalProjectsCount?: number;
}

type GraphFilter = 'ALL' | 'WEB_INTEGRATION' | 'BOSSES' | 'FLAGGED';
type GraphViewMode = 'FULL' | 'COMPACT';

interface PhaseSpec {
  number: number;
  title: string;
  subtitle: string;
  moduleRange: [number, number];
}

const GATE_AFTER_MODULE_ID: Record<string, string> = {
  'module-05': 'proj-01-cli-ledger-reconciler',
  'module-09': 'proj-02-inventory-audit-service',
};

const PHASES: PhaseSpec[] = [
  {
    number: 1,
    title: 'Foundations, OOP & Ecosystem Base',
    subtitle: 'Modules 1–5 · Python 3.13, Data Structures, OOP, Generators & Core Libraries',
    moduleRange: [1, 5],
  },
  {
    number: 2,
    title: 'Architecture, Typing & Concurrency',
    subtitle: 'Modules 6–7 · src/ Layout, Pydantic v2, pytest, Thread/Process Pools & asyncio',
    moduleRange: [6, 7],
  },
  {
    number: 3,
    title: 'SQL & ORM Engineering',
    subtitle: 'Modules 8–9 · Analytic CTEs, Indexes, SQLAlchemy 2.0, Zero-N+1 & Alembic',
    moduleRange: [8, 9],
  },
  {
    number: 4,
    title: 'FastAPI & Distributed Systems',
    subtitle: 'Module 10+ · Production FastAPI, Auth/RBAC, RFC 7807, Observability & AI RAG',
    moduleRange: [10, 20],
  },
];

function parseModuleOrder(modId: string): number {
  const match = modId.match(/(\d+)$/);
  return match ? Number.parseInt(match[1], 10) : 0;
}

function filterModuleLessons(module: ModuleGroup, filter: GraphFilter): LessonSummary[] {
  switch (filter) {
    case 'WEB_INTEGRATION':
      return module.lessons.some((l) => l.runtime === 'WEB_INTEGRATION') ? module.lessons : [];
    case 'BOSSES':
      return module.lessons.filter((l) => l.kind === 'BOSS');
    case 'FLAGGED':
      return module.lessons.filter((l) => l.flagged);
    case 'ALL':
    default:
      return module.lessons;
  }
}

export const RoadmapPage: React.FC<RoadmapPageProps> = ({
  curriculum,
  onSelectModule,
  onSelectLesson,
  onNavigateWorldMap,
  onNavigateProjects,
  completedProjectsCount = 0,
  totalProjectsCount = 1,
}) => {
  const [projects, setProjects] = useState<PortfolioProject[]>([]);
  const [filter, setFilter] = useState<GraphFilter>('ALL');
  const [viewMode, setViewMode] = useState<GraphViewMode>('FULL');
  const [hoveredLessonId, setHoveredLessonId] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<SelectedRoadmapNode | null>(null);

  useEffect(() => {
    api
      .getProjects()
      .then((res) => setProjects(res.projects))
      .catch(() => {
        // Degrades gracefully if projects endpoint is temporarily unavailable
      });
  }, []);

  const projectsById = useMemo(() => {
    const map = new Map<string, PortfolioProject>();
    for (const p of projects) {
      map.set(p.id, p);
    }
    return map;
  }, [projects]);

  const activeModuleId = useMemo(() => {
    const firstIncomplete = curriculum.modules.find(
      (m) => m.totalLessons > 0 && m.completedLessons < m.totalLessons
    );
    return firstIncomplete?.id ?? curriculum.modules[curriculum.modules.length - 1]?.id ?? null;
  }, [curriculum.modules]);

  const stats = useMemo(() => {
    const modulesCompleted = curriculum.modules.filter(
      (m) => m.totalLessons > 0 && m.completedLessons === m.totalLessons
    ).length;
    let totalBosses = 0;
    let bossesDefeated = 0;
    for (const mod of curriculum.modules) {
      for (const lesson of mod.lessons) {
        if (lesson.kind === 'BOSS') {
          totalBosses++;
          if (lesson.status === 'COMPLETED') {
            bossesDefeated++;
          }
        }
      }
    }
    const gatesUnlocked = projects.filter((p) => p.milestoneUnlocked).length;
    return {
      modulesCompleted,
      totalModules: curriculum.modules.length,
      completedLessons: curriculum.completedLessons,
      totalLessons: curriculum.totalLessons,
      bossesDefeated,
      totalBosses,
      gatesUnlocked,
      totalGates: projects.length || totalProjectsCount,
    };
  }, [curriculum, projects, totalProjectsCount]);

  const visibleSections = useMemo(() => {
    return PHASES.map((phase) => {
      const phaseModules = curriculum.modules
        .filter((m) => {
          const num = parseModuleOrder(m.id);
          return num >= phase.moduleRange[0] && num <= phase.moduleRange[1];
        })
        .map((mod) => ({
          module: mod,
          order: parseModuleOrder(mod.id),
          visibleLessons: filterModuleLessons(mod, filter),
        }))
        .filter((item) => item.visibleLessons.length > 0);

      return { phase, items: phaseModules };
    }).filter((section) => section.items.length > 0);
  }, [curriculum.modules, filter]);

  const handleJumpPhase = (phaseNumber: number) => {
    const target = document.getElementById(`phase-${phaseNumber}`);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const handleNavigateLesson = (lessonId: string) => {
    setSelectedNode(null);
    if (onSelectLesson) {
      onSelectLesson(lessonId);
    } else {
      window.location.hash = `#/lessons/${lessonId}`;
    }
  };

  const handleNavigateModule = (moduleId: string) => {
    setSelectedNode(null);
    onSelectModule(moduleId);
  };

  const handleNavigateProjects = () => {
    setSelectedNode(null);
    onNavigateProjects();
  };

  const selectedLessonId = selectedNode?.kind === 'lesson' ? selectedNode.lesson.id : null;
  const selectedModuleId = selectedNode?.kind === 'module' ? selectedNode.module.id : null;
  const selectedGateId = selectedNode?.kind === 'gate' ? selectedNode.project.id : null;

  return (
    <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC] flex flex-col">
      <TopNav
        activeSection="roadmap"
        onNavigateWorldMap={onNavigateWorldMap}
        onNavigateRoadmap={() => {}}
        onNavigateProjects={onNavigateProjects}
        completedProjectsCount={completedProjectsCount}
        totalProjectsCount={totalProjectsCount}
        streak={curriculum.streak}
      />

      {/* Single Sleek Control Strip */}
      <div className="sticky top-0 z-30 border-b border-white/[0.08] bg-[#10141E]/95 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-2.5 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
            <span className="text-[#2DD4A0] font-medium">
              {stats.modulesCompleted}/{stats.totalModules} modules
            </span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-200 font-medium">
              {stats.completedLessons}/{stats.totalLessons} lessons
            </span>
            <span className="text-slate-600">•</span>
            <span className="text-[#F45D78] font-medium">
              {stats.bossesDefeated}/{stats.totalBosses} bosses
            </span>
            <span className="text-slate-600">•</span>
            <span className="text-[#A78BFA] font-medium">
              {stats.gatesUnlocked}/{stats.totalGates} gates
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <div className="hidden md:flex items-center rounded-md bg-[#0D1017] p-0.5 border border-white/[0.08]">
              {PHASES.map((phase) => {
                const isVisible = visibleSections.some((s) => s.phase.number === phase.number);
                return (
                  <button
                    key={phase.number}
                    type="button"
                    disabled={!isVisible}
                    onClick={() => handleJumpPhase(phase.number)}
                    className={`px-2 py-1 rounded text-xs font-medium transition ${
                      isVisible
                        ? 'text-slate-300 hover:text-[#F5B942] hover:bg-[#1C2230] cursor-pointer'
                        : 'text-slate-600 cursor-not-allowed'
                    }`}
                  >
                    P{phase.number}
                  </button>
                );
              })}
            </div>

            <div className="inline-flex items-center rounded-md bg-[#0D1017] p-0.5 border border-white/[0.08]">
              {(
                [
                  ['ALL', 'All'],
                  ['WEB_INTEGRATION', 'Web & AI'],
                  ['BOSSES', 'Bosses'],
                  ['FLAGGED', 'Flagged'],
                ] as const
              ).map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setFilter(key)}
                  className={`px-2.5 py-1 rounded text-xs font-medium cursor-pointer transition ${
                    filter === key
                      ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>

            <div className="inline-flex items-center rounded-md border border-white/[0.08] bg-[#0D1017] p-0.5">
              <button
                type="button"
                onClick={() => setViewMode('FULL')}
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium cursor-pointer transition ${
                  viewMode === 'FULL'
                    ? 'bg-[#38BDF8] text-[#0D1017] font-semibold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Network className="w-3.5 h-3.5" />
                <span>Full Tree</span>
              </button>
              <button
                type="button"
                onClick={() => setViewMode('COMPACT')}
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium cursor-pointer transition ${
                  viewMode === 'COMPACT'
                    ? 'bg-[#38BDF8] text-[#0D1017] font-semibold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>Compact Spine</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Skill-Tree Canvas */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 pb-16">
        {visibleSections.length === 0 ? (
          <div className="rpg-panel p-12 text-center space-y-4">
            <p className="text-sm text-slate-400">No roadmap nodes match the selected filter.</p>
            <button
              type="button"
              onClick={() => setFilter('ALL')}
              className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rpg-btn-gold cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset Filter</span>
            </button>
          </div>
        ) : (
          <div className="relative space-y-12">
            {/* Continuous Central Vertical Spine */}
            <div
              aria-hidden="true"
              className="pointer-events-none absolute top-4 bottom-4 left-5 sm:left-7 lg:left-1/2 lg:-translate-x-1/2 w-[3px] rounded-full bg-gradient-to-b from-[#38BDF8]/70 via-[#F5B942]/70 to-[#A78BFA]/70"
            />

            {visibleSections.map(({ phase, items }) => (
              <section key={phase.number} id={`phase-${phase.number}`} className="scroll-mt-24 space-y-6">
                {/* Phase Pill Header */}
                <div className="relative z-10 flex justify-start pl-10 sm:pl-14 lg:justify-center lg:pl-0">
                  <div className="px-4 py-2 rounded-lg bg-[#151923] border border-white/[0.1] text-left lg:text-center shadow-sm">
                    <div className="text-[11px] font-semibold text-[#F5B942]">
                      Phase {phase.number} — {phase.title}
                    </div>
                    <div className="text-xs text-slate-400 mt-0.5">{phase.subtitle}</div>
                  </div>
                </div>

                {/* Modules & Portfolio Gates */}
                <div className="space-y-8">
                  {items.map(({ module, order, visibleLessons }) => {
                    const gateId = filter === 'ALL' ? GATE_AFTER_MODULE_ID[module.id] : undefined;
                    const gateProject = gateId ? projectsById.get(gateId) : undefined;

                    return (
                      <React.Fragment key={module.id}>
                        <ModuleBranchBand
                          module={module}
                          moduleOrder={order}
                          lessons={visibleLessons}
                          compact={viewMode === 'COMPACT'}
                          isActiveMarker={activeModuleId === module.id}
                          heroTier={curriculum.hero.tier}
                          hoveredLessonId={hoveredLessonId}
                          selectedLessonId={selectedLessonId}
                          selectedModuleId={selectedModuleId}
                          onHoverLesson={setHoveredLessonId}
                          onClickLesson={(lesson, mod) =>
                            setSelectedNode({ kind: 'lesson', lesson, module: mod })
                          }
                          onClickModule={(mod) => setSelectedNode({ kind: 'module', module: mod })}
                        />

                        {gateProject && (
                          <GateLandmarkBand
                            project={gateProject}
                            compact={viewMode === 'COMPACT'}
                            selected={selectedGateId === gateProject.id}
                            onClick={() => setSelectedNode({ kind: 'gate', project: gateProject })}
                          />
                        )}
                      </React.Fragment>
                    );
                  })}
                </div>
              </section>
            ))}
          </div>
        )}
      </main>

      <RoadmapInspectorDrawer
        selected={selectedNode}
        onClose={() => setSelectedNode(null)}
        onSelectLesson={handleNavigateLesson}
        onSelectModule={handleNavigateModule}
        onNavigateProjects={handleNavigateProjects}
      />
    </div>
  );
};
