import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Search, X } from 'lucide-react';
import type { CurriculumResponse } from '../types/api';
import {
  PixelCheckIcon,
  PixelGateIcon,
  PixelMapIcon,
  PixelPythonIcon,
  PixelScrollIcon,
  PixelSkullIcon,
} from './PixelIcons';

interface CommandItem {
  id: string;
  kind: 'view' | 'module' | 'lesson';
  title: string;
  subtitle: string;
  keywords: string;
  completed?: boolean;
  isBoss?: boolean;
  action: () => void;
}

interface CommandPaletteModalProps {
  open: boolean;
  curriculum: CurriculumResponse | null;
  onClose: () => void;
  onNavigateDashboard: () => void;
  onNavigateRoadmap: () => void;
  onNavigateProjects: () => void;
  onSelectModule: (moduleId: string) => void;
  onSelectLesson: (lessonId: string) => void;
}

export const CommandPaletteModal: React.FC<CommandPaletteModalProps> = ({
  open,
  curriculum,
  onClose,
  onNavigateDashboard,
  onNavigateRoadmap,
  onNavigateProjects,
  onSelectModule,
  onSelectLesson,
}) => {
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    if (!open) return;
    setQuery('');
    setActiveIndex(0);
    window.setTimeout(() => inputRef.current?.focus(), 20);
  }, [open]);

  const items = useMemo<CommandItem[]>(() => {
    const base: CommandItem[] = [
      {
        id: 'view-world-map',
        kind: 'view',
        title: 'World Map (Quests Dashboard)',
        subtitle: 'Overview, character sheet, search & review queue',
        keywords: 'dashboard world map quests home',
        action: onNavigateDashboard,
      },
      {
        id: 'view-roadmap',
        kind: 'view',
        title: 'Skill-Tree Roadmap',
        subtitle: 'Interactive 5-phase engineering progression tree',
        keywords: 'roadmap skill tree phases graph',
        action: onNavigateRoadmap,
      },
      {
        id: 'view-projects',
        kind: 'view',
        title: 'Portfolio Guild (Capstone PRDs)',
        subtitle: '3 production portfolio project specs & checklists',
        keywords: 'guild portfolio projects prd gate',
        action: onNavigateProjects,
      },
    ];

    if (!curriculum) return base;

    for (const mod of curriculum.modules) {
      base.push({
        id: `mod-${mod.id}`,
        kind: 'module',
        title: mod.title,
        subtitle: `${mod.completedLessons}/${mod.totalLessons} stages • ${mod.subtitle || 'Realm overview'}`,
        keywords: `${mod.id} ${mod.title} ${mod.subtitle ?? ''}`,
        completed: mod.totalLessons > 0 && mod.completedLessons === mod.totalLessons,
        action: () => onSelectModule(mod.id),
      });
    }

    for (const mod of curriculum.modules) {
      for (const lesson of mod.lessons) {
        base.push({
          id: `lesson-${lesson.id}`,
          kind: 'lesson',
          title: `#${lesson.id} — ${lesson.title}`,
          subtitle: `${lesson.moduleTitle} • ${lesson.objective}`,
          keywords: `${lesson.id} ${lesson.title} ${lesson.moduleTitle} ${lesson.tags.join(' ')} ${lesson.objective}`,
          completed: lesson.status === 'COMPLETED',
          isBoss: lesson.kind === 'BOSS',
          action: () => onSelectLesson(lesson.id),
        });
      }
    }

    return base;
  }, [
    curriculum,
    onNavigateDashboard,
    onNavigateRoadmap,
    onNavigateProjects,
    onSelectModule,
    onSelectLesson,
  ]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return items.slice(0, 15);
    }
    const tokens = q.split(/\s+/).filter(Boolean);
    return items
      .filter((item) => {
        const haystack = `${item.title} ${item.keywords}`.toLowerCase();
        return tokens.every((tok) => haystack.includes(tok));
      })
      .slice(0, 24);
  }, [items, query]);

  useEffect(() => {
    setActiveIndex(0);
  }, [query]);

  if (!open) return null;

  const runSelection = (item: CommandItem | undefined) => {
    if (!item) return;
    onClose();
    item.action();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((prev) => (filtered.length === 0 ? 0 : (prev + 1) % filtered.length));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((prev) =>
        filtered.length === 0 ? 0 : (prev - 1 + filtered.length) % filtered.length
      );
    } else if (e.key === 'Enter') {
      e.preventDefault();
      runSelection(filtered[activeIndex]);
    }
  };

  return (
    <div
      className="fixed inset-0 z-[60] bg-black/70 backdrop-blur-[2px] flex items-start justify-center pt-16 sm:pt-24 p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Quick Jump Command Palette"
      onClick={onClose}
    >
      <div
        className="rpg-panel-gold max-w-2xl w-full overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        <div className="px-4 py-3 border-b border-white/[0.08] bg-[#0D1017] flex items-center gap-3">
          <Search className="w-4 h-4 text-[#F5B942] shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Jump to any stage, module, or view (e.g. 09-02, selectinload, alembic, roadmap)..."
            className="flex-1 bg-transparent text-sm text-[#F8FAFC] placeholder-slate-500 focus:outline-none"
          />
          <button
            type="button"
            onClick={onClose}
            className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer"
          >
            <span>Esc</span>
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="max-h-[380px] overflow-y-auto p-2 space-y-1 bg-[#121620]">
          {filtered.length === 0 ? (
            <div className="py-10 text-center text-xs text-slate-400">
              No stages, modules, or views match &quot;{query}&quot;.
            </div>
          ) : (
            filtered.map((item, idx) => {
              const selected = idx === activeIndex;
              return (
                <button
                  key={item.id}
                  type="button"
                  onMouseEnter={() => setActiveIndex(idx)}
                  onClick={() => runSelection(item)}
                  className={`w-full text-left px-3 py-2.5 rounded-md flex items-center justify-between gap-3 cursor-pointer transition ${
                    selected
                      ? 'bg-[#1C2230] border border-[#F5B942]/45'
                      : 'border border-transparent hover:bg-[#181E2B]'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="shrink-0">
                      {item.kind === 'view' ? (
                        item.id === 'view-roadmap' ? (
                          <PixelMapIcon className="w-4 h-4" />
                        ) : item.id === 'view-projects' ? (
                          <PixelGateIcon className="w-4 h-4" />
                        ) : (
                          <PixelScrollIcon className="w-4 h-4" />
                        )
                      ) : item.kind === 'module' ? (
                        <PixelScrollIcon className="w-4 h-4" />
                      ) : item.isBoss ? (
                        <PixelSkullIcon className="w-4 h-4" />
                      ) : (
                        <PixelPythonIcon className="w-4 h-4" />
                      )}
                    </span>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold text-[#F8FAFC] truncate flex items-center gap-2">
                        <span className="truncate">{item.title}</span>
                        {item.completed && <PixelCheckIcon className="w-3 h-3 shrink-0" />}
                      </div>
                      <div className="text-[11px] text-slate-400 truncate mt-0.5">
                        {item.subtitle}
                      </div>
                    </div>
                  </div>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                </button>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
