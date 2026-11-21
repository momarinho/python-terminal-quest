import React, { useEffect, useState } from 'react';
import { ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { PixelBotIcon, PixelPotionIcon } from './PixelIcons';

export type CompanionMood = 'idle' | 'running' | 'victory' | 'fail';

export interface HeroTierMeta {
  tier: number;
  title: string;
  gearLabel: string;
}

export const HERO_TIER_CATALOG: HeroTierMeta[] = [
  { tier: 1, title: 'Apprentice', gearLabel: 'Wood Sword & Coffee Mug' },
  { tier: 2, title: 'Explorer', gearLabel: 'Hooded Cloak & Cyan Rune' },
  { tier: 3, title: 'Async Knight', gearLabel: 'Visor Helm & Concurrency Sparks' },
  { tier: 4, title: 'Backend Architect', gearLabel: 'Gilded Mantle & Rune Tome' },
  { tier: 5, title: 'AI Grandmaster', gearLabel: 'Emerald-Gold Crown & Aura' },
];

interface HeroCompanionSpriteProps {
  tier: number;
  mood?: CompanionMood;
  className?: string;
  preferSpriteSheet?: boolean;
}

/**
 * Layered 24x24 pixel-art RPG Knight sprite (crispEdges SVG).
 * Structured so PNG sprite sheets in `/sprites/hero-tier-<N>.png` can drop in cleanly later.
 */
export const HeroCompanionSprite: React.FC<HeroCompanionSpriteProps> = ({
  tier,
  mood = 'idle',
  className = 'w-14 h-14',
  preferSpriteSheet = false,
}) => {
  const clampedTier = Math.min(5, Math.max(1, tier));
  const [pngFailed, setPngFailed] = useState(false);

  if (preferSpriteSheet && !pngFailed) {
    return (
      <img
        src={`/sprites/hero-tier-${clampedTier}.png`}
        alt={`Hero Companion Tier ${clampedTier}`}
        onError={() => setPngFailed(true)}
        className={`${className} [image-rendering:pixelated]`}
      />
    );
  }

  const eyeColor =
    mood === 'victory'
      ? '#2DD4A0'
      : mood === 'fail'
        ? '#F45D78'
        : mood === 'running'
          ? '#F5B942'
          : '#38BDF8';

  const tunicColor =
    clampedTier === 1
      ? '#334155'
      : clampedTier === 2
        ? '#1E3A5F'
        : clampedTier === 3
          ? '#312E81'
          : clampedTier === 4
            ? '#3B1D5E'
            : '#064E3B';

  const trimColor =
    clampedTier >= 4 ? '#F5B942' : clampedTier === 3 ? '#38BDF8' : '#94A3B8';

  return (
    <svg
      viewBox="0 0 24 24"
      shapeRendering="crispEdges"
      className={className}
      aria-label={`Tier ${clampedTier} Hero Companion`}
    >
      {/* Tier 5: Radiant Emerald & Gold Aura */}
      {clampedTier === 5 && (
        <g opacity="0.85">
          <rect x="4" y="3" width="1" height="1" fill="#2DD4A0" />
          <rect x="19" y="3" width="1" height="1" fill="#F5B942" />
          <rect x="2" y="10" width="1" height="2" fill="#2DD4A0" />
          <rect x="21" y="10" width="1" height="2" fill="#F5B942" />
          <rect x="5" y="1" width="14" height="1" fill="#2DD4A0" opacity="0.35" />
        </g>
      )}

      {/* Tier 2 & 4: Hooded Cloak / Gilded Mantle back layer */}
      {clampedTier >= 2 && (
        <g>
          <rect x="6" y="11" width="12" height="8" fill={clampedTier >= 4 ? '#1E1B4B' : '#1E293B'} />
          <rect x="5" y="13" width="14" height="5" fill={clampedTier >= 4 ? '#312E81' : '#334155'} />
        </g>
      )}

      {/* Tier 5: Crown */}
      {clampedTier === 5 && (
        <g>
          <rect x="8" y="2" width="2" height="2" fill="#F5B942" />
          <rect x="11" y="1" width="2" height="3" fill="#FDE68A" />
          <rect x="14" y="2" width="2" height="2" fill="#F5B942" />
          <rect x="8" y="4" width="8" height="1" fill="#D97706" />
        </g>
      )}

      {/* Head / Hood / Visor Helm */}
      {clampedTier === 1 && (
        <g>
          {/* Apprentice hair + face */}
          <rect x="8" y="4" width="8" height="2" fill="#92400E" />
          <rect x="7" y="5" width="10" height="2" fill="#B45309" />
          <rect x="8" y="7" width="8" height="4" fill="#FDE68A" />
          <rect x="9" y="8" width="2" height="2" fill="#0D1017" />
          <rect x="13" y="8" width="2" height="2" fill="#0D1017" />
        </g>
      )}

      {clampedTier === 2 && (
        <g>
          {/* Explorer hooded cloak */}
          <rect x="8" y="3" width="8" height="2" fill="#0284C7" />
          <rect x="7" y="5" width="10" height="6" fill="#0369A1" />
          <rect x="8" y="7" width="8" height="4" fill="#0F172A" />
          <rect x="9" y="8" width="2" height="2" fill={eyeColor} />
          <rect x="13" y="8" width="2" height="2" fill={eyeColor} />
        </g>
      )}

      {clampedTier >= 3 && (
        <g>
          {/* Knight Visor Helm (Steel / Dark Obsidian / Emerald-Gold) */}
          <rect
            x="8"
            y="4"
            width="8"
            height="2"
            fill={clampedTier === 5 ? '#F5B942' : clampedTier === 4 ? '#475569' : '#94A3B8'}
          />
          <rect
            x="7"
            y="6"
            width="10"
            height="5"
            fill={clampedTier === 5 ? '#10B981' : clampedTier === 4 ? '#334155' : '#64748B'}
          />
          {/* Visor slit & glowing eyes */}
          <rect x="8" y="8" width="8" height="2" fill="#0B0E14" />
          <rect x="9" y="8" width="2" height="2" fill={eyeColor} />
          <rect x="13" y="8" width="2" height="2" fill={eyeColor} />
        </g>
      )}

      {/* Torso Armor / Tunic */}
      <rect x="8" y="11" width="8" height="6" fill={tunicColor} />
      <rect x="9" y="12" width="6" height="1" fill={trimColor} />
      <rect x="11" y="13" width="2" height="3" fill={trimColor} />

      {/* Tier 4: Gilded Shoulder Pauldrons */}
      {clampedTier >= 4 && (
        <g>
          <rect x="6" y="11" width="2" height="3" fill="#F5B942" />
          <rect x="16" y="11" width="2" height="3" fill="#F5B942" />
        </g>
      )}

      {/* Boots / Legs */}
      <rect x="8" y="17" width="3" height="3" fill="#1E293B" />
      <rect x="13" y="17" width="3" height="3" fill="#1E293B" />
      <rect x="8" y="20" width="3" height="1" fill={trimColor} />
      <rect x="13" y="20" width="3" height="1" fill={trimColor} />

      {/* Left-Hand Gear by Tier */}
      {clampedTier === 1 && (
        /* Warm Coffee Mug */
        <g>
          <rect x="4" y="13" width="3" height="3" fill="#F8FAFC" />
          <rect x="3" y="14" width="1" height="1" fill="#CBD5E1" />
          <rect x="5" y="11" width="1" height="1" fill="#94A3B8" />
        </g>
      )}
      {clampedTier === 2 && (
        /* Glowing Cyan Rune */
        <g>
          <rect x="3" y="12" width="3" height="4" fill="#38BDF8" />
          <rect x="4" y="13" width="1" height="2" fill="#E0F2FE" />
        </g>
      )}
      {clampedTier === 3 && (
        /* Concurrency Lightning Sparks */
        <g>
          <rect x="3" y="10" width="2" height="2" fill="#38BDF8" />
          <rect x="2" y="12" width="3" height="1" fill="#F5B942" />
          <rect x="3" y="13" width="2" height="2" fill="#38BDF8" />
        </g>
      )}
      {clampedTier >= 4 && (
        /* Floating Rune Tome / AI Core */
        <g>
          <rect x="2" y="12" width="4" height="5" fill="#7C3AED" />
          <rect x="3" y="13" width="2" height="3" fill="#E9D5FF" />
        </g>
      )}

      {/* Right-Hand Weapon by Tier */}
      {clampedTier === 1 && (
        /* Wood Practice Sword */
        <g>
          <rect x="18" y="9" width="2" height="6" fill="#B45309" />
          <rect x="17" y="14" width="4" height="1" fill="#F5B942" />
          <rect x="18" y="15" width="2" height="2" fill="#78350F" />
        </g>
      )}
      {clampedTier >= 2 && (
        /* Forged Rune Blade */
        <g>
          <rect
            x="18"
            y="7"
            width="2"
            height="8"
            fill={clampedTier === 5 ? '#2DD4A0' : clampedTier >= 3 ? '#E2E8F0' : '#CBD5E1'}
          />
          <rect x="17" y="14" width="4" height="1" fill="#F5B942" />
          <rect x="18" y="15" width="2" height="2" fill="#92400E" />
        </g>
      )}

      {/* Mood Sparkle Overlay */}
      {mood === 'victory' && (
        <g>
          <rect x="19" y="3" width="2" height="2" fill="#2DD4A0" />
          <rect x="3" y="4" width="2" height="2" fill="#F5B942" />
        </g>
      )}
    </svg>
  );
};

interface HeroCompanionFloatingProps {
  tier: number;
  tierTitle: string;
  mood: CompanionMood;
  onJumpHints: () => void;
  onJumpOracle: () => void;
}

const COLLAPSE_STORAGE_KEY = 'pyquest.companionCollapsed';

const SPEECH_BY_MOOD: Record<CompanionMood, string> = {
  idle: 'Ready when you are — press Ctrl+Enter to grade.',
  running: 'Executing isolated pytest suite...',
  victory: 'Clean pass! Every test assertion held.',
  fail: 'Check the Battle Log diff or unlock a Hint.',
};

export const HeroCompanionFloating: React.FC<HeroCompanionFloatingProps> = ({
  tier,
  tierTitle,
  mood,
  onJumpHints,
  onJumpOracle,
}) => {
  const [collapsed, setCollapsed] = useState<boolean>(() => {
    try {
      return localStorage.getItem(COLLAPSE_STORAGE_KEY) === '1';
    } catch {
      return false;
    }
  });
  const [menuOpen, setMenuOpen] = useState(false);
  const [showBubble, setShowBubble] = useState(false);

  useEffect(() => {
    if (mood === 'idle') {
      setShowBubble(false);
      return;
    }
    setShowBubble(true);
    const timer = window.setTimeout(() => setShowBubble(false), 3800);
    return () => window.clearTimeout(timer);
  }, [mood]);

  const toggleCollapsed = () => {
    const next = !collapsed;
    setCollapsed(next);
    setMenuOpen(false);
    try {
      localStorage.setItem(COLLAPSE_STORAGE_KEY, next ? '1' : '0');
    } catch {
      // ignore storage failure
    }
  };

  if (collapsed) {
    return (
      <div className="fixed bottom-4 right-4 z-40">
        <button
          type="button"
          onClick={toggleCollapsed}
          title={`Expand Hero Companion (${tierTitle})`}
          className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[#151923] border border-white/[0.12] hover:border-[#F5B942]/60 shadow-xl cursor-pointer transition"
        >
          <HeroCompanionSprite tier={tier} mood={mood} className="w-6 h-6" />
          <span className="text-xs font-medium text-slate-200">{tierTitle}</span>
          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-40 flex flex-col items-end gap-2">
      {showBubble && (
        <div className="max-w-[240px] px-3 py-2 rounded-lg bg-[#1C2230] border border-white/[0.12] text-xs text-slate-100 shadow-lg">
          {SPEECH_BY_MOOD[mood]}
        </div>
      )}

      {menuOpen && (
        <div className="w-52 rpg-panel p-2 shadow-2xl space-y-1">
          <div className="px-2 py-1 text-[11px] font-medium text-slate-400 flex items-center gap-1.5">
            <Sparkles className="w-3 h-3 text-[#F5B942]" />
            <span>Companion Actions</span>
          </div>
          <button
            type="button"
            onClick={() => {
              setMenuOpen(false);
              onJumpHints();
            }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-md text-xs text-slate-200 hover:bg-[#1C2230] hover:text-[#F5B942] cursor-pointer transition"
          >
            <PixelPotionIcon className="w-3.5 h-3.5" />
            <span>Open Progressive Hints</span>
          </button>
          <button
            type="button"
            onClick={() => {
              setMenuOpen(false);
              onJumpOracle();
            }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-md text-xs text-slate-200 hover:bg-[#1C2230] hover:text-[#A78BFA] cursor-pointer transition"
          >
            <PixelBotIcon className="w-3.5 h-3.5" />
            <span>Ask RAG Oracle</span>
          </button>
        </div>
      )}

      <div className="flex items-center gap-2 p-2 rounded-xl bg-[#151923]/95 backdrop-blur-sm border border-white/[0.1] shadow-2xl">
        <button
          type="button"
          onClick={() => setMenuOpen((prev) => !prev)}
          title="Click for Hints or Oracle shortcuts"
          className="flex items-center gap-2.5 pr-1 cursor-pointer group"
        >
          <div className="p-1.5 rounded-lg bg-[#0D1017] border border-white/[0.08] group-hover:border-[#F5B942]/50 transition">
            <HeroCompanionSprite tier={tier} mood={mood} className="w-9 h-9" />
          </div>
          <div className="text-left">
            <div className="text-xs font-semibold text-[#F8FAFC] group-hover:text-[#F5B942] transition">
              {tierTitle}
            </div>
            <div className="text-[11px] text-slate-400">Tier {tier}/5 · Quick help</div>
          </div>
        </button>

        <button
          type="button"
          onClick={toggleCollapsed}
          aria-label="Collapse Hero Companion"
          title="Collapse companion"
          className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer transition"
        >
          <ChevronDown className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
