import React from 'react';
import {
  PixelCampfireIcon,
  PixelGateIcon,
  PixelMapIcon,
  PixelPythonIcon,
  PixelScrollIcon,
} from './PixelIcons';
import type { StreakStats } from '../types/api';

interface TopNavProps {
  activeSection: 'world-map' | 'roadmap' | 'module' | 'projects';
  onNavigateWorldMap: () => void;
  onNavigateRoadmap?: () => void;
  onNavigateProjects: () => void;
  completedProjectsCount?: number;
  totalProjectsCount?: number;
  streak?: StreakStats | null;
}

export const TopNav: React.FC<TopNavProps> = ({
  activeSection,
  onNavigateWorldMap,
  onNavigateRoadmap,
  onNavigateProjects,
  completedProjectsCount = 0,
  totalProjectsCount = 1,
  streak = null,
}) => {
  const streakDays = streak?.currentStreakDays ?? 0;
  const bestStreak = streak?.longestStreakDays ?? 0;
  const isLit = streakDays > 0;

  const handleRoadmapClick = () => {
    if (onNavigateRoadmap) {
      onNavigateRoadmap();
    } else {
      window.location.hash = '#/roadmap';
    }
  };

  return (
    <nav className="border-b border-white/[0.08] bg-[#0D1017]/95 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-4">
        <button
          type="button"
          onClick={onNavigateWorldMap}
          className="inline-flex items-center gap-2.5 text-[#F8FAFC] hover:text-[#F5B942] cursor-pointer transition min-w-0 shrink-0"
        >
          <span className="p-1.5 rounded-md bg-[#151923] border border-white/[0.08]">
            <PixelPythonIcon className="w-4 h-4 shrink-0" />
          </span>
          <span className="font-pixel text-[18px] leading-none tracking-tight hidden sm:inline">
            Python Terminal Quest
          </span>
          <span className="font-pixel text-[18px] leading-none sm:hidden">PyQuest</span>
        </button>

        <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
          {streak && (
            <div
              title={`Current Streak: ${streakDays} day(s) | Longest: ${bestStreak} day(s) | Active Days: ${streak.activeDaysTotal}`}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium border ${
                streak.activeToday
                  ? 'bg-[#F5B942]/12 border-[#F5B942]/40 text-[#F5B942]'
                  : isLit
                    ? 'bg-[#151923] border-white/[0.08] text-amber-200'
                    : 'bg-[#151923] border-white/[0.06] text-slate-400'
              }`}
            >
              <PixelCampfireIcon className="w-3.5 h-3.5 shrink-0" />
              <span className="whitespace-nowrap">{streakDays}d streak</span>
            </div>
          )}

          <button
            type="button"
            onClick={onNavigateWorldMap}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer transition whitespace-nowrap ${
              activeSection === 'world-map' || activeSection === 'module'
                ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                : 'text-slate-300 hover:text-white hover:bg-[#1C2230]'
            }`}
          >
            <PixelScrollIcon className="w-3.5 h-3.5 shrink-0" />
            <span>Quests</span>
          </button>

          <button
            type="button"
            onClick={handleRoadmapClick}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer transition whitespace-nowrap ${
              activeSection === 'roadmap'
                ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                : 'text-slate-300 hover:text-[#38BDF8] hover:bg-[#1C2230]'
            }`}
          >
            <PixelMapIcon className="w-3.5 h-3.5 shrink-0" />
            <span>Roadmap</span>
          </button>

          <button
            type="button"
            onClick={onNavigateProjects}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer transition whitespace-nowrap ${
              activeSection === 'projects'
                ? 'bg-[#2DD4A0] text-[#07130F] font-semibold'
                : 'text-slate-300 hover:text-[#A78BFA] hover:bg-[#1C2230]'
            }`}
          >
            <PixelGateIcon className="w-3.5 h-3.5 shrink-0" />
            <span>Guild</span>
            <span
              className={`px-1.5 py-0.5 rounded text-[11px] font-semibold ${
                activeSection === 'projects'
                  ? 'bg-[#07130F]/15 text-[#07130F]'
                  : 'bg-white/[0.06] text-[#2DD4A0]'
              }`}
            >
              {completedProjectsCount}/{totalProjectsCount}
            </span>
          </button>
        </div>
      </div>
    </nav>
  );
};
