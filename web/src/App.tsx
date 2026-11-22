import React, { useCallback, useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { api } from './api/client';
import { CommandPaletteModal } from './components/CommandPaletteModal';
import { DashboardPage } from './pages/DashboardPage';
import { LessonWorkspacePage } from './pages/LessonWorkspacePage';
import { ModulePage } from './pages/ModulePage';
import { ProjectsPage } from './pages/ProjectsPage';
import { RoadmapPage } from './pages/RoadmapPage';
import type { CurriculumResponse } from './types/api';

type RouteState =
  | { view: 'dashboard' }
  | { view: 'roadmap' }
  | { view: 'module'; moduleId: string; openCampfire?: boolean }
  | { view: 'lesson'; lessonId: string }
  | { view: 'projects' };

function parseHashRoute(): RouteState {
  const hash = window.location.hash;
  if (hash === '#/projects') {
    return { view: 'projects' };
  }
  if (hash === '#/roadmap') {
    return { view: 'roadmap' };
  }
  const lessonMatch = hash.match(/^#\/lessons\/([A-Za-z0-9_-]+)$/);
  if (lessonMatch) {
    return { view: 'lesson', lessonId: lessonMatch[1] };
  }
  const moduleMatch = hash.match(/^#\/modules\/([A-Za-z0-9_-]+)(?:\?(.*))?$/);
  if (moduleMatch) {
    const query = moduleMatch[2] ?? '';
    return {
      view: 'module',
      moduleId: moduleMatch[1],
      openCampfire: query.includes('campfire=1'),
    };
  }
  return { view: 'dashboard' };
}

export const App: React.FC = () => {
  const [curriculum, setCurriculum] = useState<CurriculumResponse | null>(null);
  const [projectCounts, setProjectCounts] = useState<{ completed: number; total: number }>({
    completed: 0,
    total: 1,
  });
  const [route, setRoute] = useState<RouteState>(() => parseHashRoute());
  const [error, setError] = useState<string | null>(null);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  const loadCurriculum = useCallback(() => {
    api
      .getCurriculum()
      .then((data) => {
        setCurriculum(data);
        setError(null);
      })
      .catch((err: Error) => {
        setError(err.message);
      });
  }, []);

  const loadProjectCounts = useCallback(() => {
    api
      .getProjects()
      .then((res) => {
        setProjectCounts({ completed: res.completedProjects, total: res.totalProjects });
      })
      .catch(() => {
        // Non-blocking badge hydration
      });
  }, []);

  useEffect(() => {
    loadCurriculum();
    loadProjectCounts();
  }, [loadCurriculum, loadProjectCounts]);

  useEffect(() => {
    const onHashChange = () => {
      setRoute(parseHashRoute());
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && !e.altKey && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        e.stopPropagation();
        setCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', onKeyDown, true);
    return () => window.removeEventListener('keydown', onKeyDown, true);
  }, []);

  const navigateToDashboard = useCallback(() => {
    window.location.hash = '#/';
    setRoute({ view: 'dashboard' });
    loadCurriculum();
    loadProjectCounts();
  }, [loadCurriculum, loadProjectCounts]);

  const navigateToModule = useCallback(
    (moduleId: string, openCampfire = false) => {
      window.location.hash = openCampfire
        ? `#/modules/${moduleId}?campfire=1`
        : `#/modules/${moduleId}`;
      setRoute({ view: 'module', moduleId, openCampfire });
      loadCurriculum();
    },
    [loadCurriculum]
  );

  const navigateToLesson = useCallback((lessonId: string) => {
    window.location.hash = `#/lessons/${lessonId}`;
    setRoute({ view: 'lesson', lessonId });
  }, []);

  const navigateToProjects = useCallback(() => {
    window.location.hash = '#/projects';
    setRoute({ view: 'projects' });
  }, []);

  const navigateToRoadmap = useCallback(() => {
    window.location.hash = '#/roadmap';
    setRoute({ view: 'roadmap' });
    loadCurriculum();
    loadProjectCounts();
  }, [loadCurriculum, loadProjectCounts]);

  const openCommandPalette = useCallback(() => setCommandPaletteOpen(true), []);

  let pageContent: React.ReactNode;

  if (route.view === 'lesson') {
    pageContent = (
      <LessonWorkspacePage
        lessonId={route.lessonId}
        hero={curriculum?.hero ?? null}
        onBackToDashboard={navigateToDashboard}
        onBackToModule={(modId) => navigateToModule(modId, false)}
        onOpenModuleCampfire={(modId) => navigateToModule(modId, true)}
        onNavigateLesson={navigateToLesson}
        onOpenCommandPalette={openCommandPalette}
        onProgressUpdated={loadCurriculum}
      />
    );
  } else if (route.view === 'projects') {
    pageContent = (
      <ProjectsPage
        onNavigateWorldMap={navigateToDashboard}
        onNavigateRoadmap={navigateToRoadmap}
        onOpenCommandPalette={openCommandPalette}
        onProjectsLoaded={setProjectCounts}
        streak={curriculum?.streak ?? null}
      />
    );
  } else if (!curriculum) {
    pageContent = (
      <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC] flex flex-col items-center justify-center gap-3 p-4 text-center">
        {error ? (
          <div className="text-[#F45D78] text-sm font-medium">
            Failed to load curriculum API: {error}
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <Loader2 className="w-5 h-5 animate-spin text-[#F5B942]" />
            <span className="text-sm font-medium text-slate-300">
              Loading Python Terminal Quest...
            </span>
          </div>
        )}
      </div>
    );
  } else if (route.view === 'roadmap') {
    pageContent = (
      <RoadmapPage
        curriculum={curriculum}
        onSelectModule={(modId) => navigateToModule(modId, false)}
        onSelectLesson={navigateToLesson}
        onNavigateWorldMap={navigateToDashboard}
        onNavigateProjects={navigateToProjects}
        onOpenCommandPalette={openCommandPalette}
        completedProjectsCount={projectCounts.completed}
        totalProjectsCount={projectCounts.total}
      />
    );
  } else if (route.view === 'module') {
    pageContent = (
      <ModulePage
        curriculum={curriculum}
        moduleId={route.moduleId}
        initialOpenCampfire={Boolean(route.openCampfire)}
        onBackToDashboard={navigateToDashboard}
        onNavigateRoadmap={navigateToRoadmap}
        onNavigateProjects={navigateToProjects}
        onOpenCommandPalette={openCommandPalette}
        onSelectModule={(modId) => navigateToModule(modId, false)}
        onSelectLesson={navigateToLesson}
        completedProjectsCount={projectCounts.completed}
        totalProjectsCount={projectCounts.total}
      />
    );
  } else {
    pageContent = (
      <DashboardPage
        curriculum={curriculum}
        onSelectModule={(modId) => navigateToModule(modId, false)}
        onSelectLesson={navigateToLesson}
        onNavigateRoadmap={navigateToRoadmap}
        onNavigateProjects={navigateToProjects}
        onOpenCommandPalette={openCommandPalette}
        onProgressUpdated={() => {
          loadCurriculum();
          loadProjectCounts();
        }}
        completedProjectsCount={projectCounts.completed}
        totalProjectsCount={projectCounts.total}
      />
    );
  }

  return (
    <>
      {pageContent}
      <CommandPaletteModal
        open={commandPaletteOpen}
        curriculum={curriculum}
        onClose={() => setCommandPaletteOpen(false)}
        onNavigateDashboard={navigateToDashboard}
        onNavigateRoadmap={navigateToRoadmap}
        onNavigateProjects={navigateToProjects}
        onSelectModule={(modId) => navigateToModule(modId, false)}
        onSelectLesson={navigateToLesson}
      />
    </>
  );
};

export default App;
