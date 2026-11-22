import React, { useEffect, useState } from 'react';
import {
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  FileCheck2,
  Flame,
  Lock,
  Shield,
  Skull,
  Sparkles,
  X,
} from 'lucide-react';
import type { HeroStatus } from '../types/api';
import { PixelBotIcon, PixelPotionIcon } from './PixelIcons';

export type CompanionMood = 'idle' | 'running' | 'victory' | 'fail';

export interface HeroTierMeta {
  tier: number;
  requiredModules: number;
  title: string;
  gearLabel: string;
  lore: string;
}

export const HERO_TIER_CATALOG: HeroTierMeta[] = [
  {
    tier: 1,
    requiredModules: 0,
    title: 'Apprentice',
    gearLabel: 'Wood Sword & Coffee Mug',
    lore: 'Armed with a practice blade, fresh coffee, and Python 3.13 fundamentals.',
  },
  {
    tier: 2,
    requiredModules: 3,
    title: 'Explorer',
    gearLabel: 'Hooded Cloak & Cyan Rune',
    lore: 'Cloaked in structural protocols, O(1) deques, and lazy generator streams.',
  },
  {
    tier: 3,
    requiredModules: 6,
    title: 'Async Knight',
    gearLabel: 'Visor Helm & Concurrency Sparks',
    lore: 'Forged in TaskGroups, process pools, and zero-N+1 SQL execution plans.',
  },
  {
    tier: 4,
    requiredModules: 9,
    title: 'Backend Architect',
    gearLabel: 'Gilded Mantle & Rune Tome',
    lore: 'Commanding FastAPI gateways, RFC 7807 contracts, Outbox relays, and Circuit Breakers.',
  },
  {
    tier: 5,
    requiredModules: 12,
    title: 'AI Grandmaster',
    gearLabel: 'Emerald-Gold Crown & Aura',
    lore: 'Master of grounded hybrid RAG, prompt-injection guardrails, and production LLM evals.',
  },
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

  const weaponYOffset = mood === 'victory' ? -2 : mood === 'fail' ? 1 : 0;
  const weaponTransform = weaponYOffset !== 0 ? `translate(0, ${weaponYOffset})` : undefined;
  const leftGearClass = mood === 'running' ? 'animate-pulse' : undefined;

  return (
    <svg
      viewBox="0 0 24 24"
      shapeRendering="crispEdges"
      className={className}
      aria-label={`Tier ${clampedTier} Hero Companion`}
    >
      {/* Fail Mood: Crimson Warning Rune above head */}
      {mood === 'fail' && (
        <g>
          <rect x="11" y="0" width="2" height="2" fill="#F45D78" />
          <rect x="11" y="3" width="2" height="1" fill="#F45D78" />
        </g>
      )}

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
          <rect x="8" y="4" width="8" height="2" fill="#92400E" />
          <rect x="7" y="5" width="10" height="2" fill="#B45309" />
          <rect x="8" y="7" width="8" height="4" fill="#FDE68A" />
          <rect x="9" y="8" width="2" height="2" fill="#0D1017" />
          <rect x="13" y="8" width="2" height="2" fill="#0D1017" />
        </g>
      )}

      {clampedTier === 2 && (
        <g>
          <rect x="8" y="3" width="8" height="2" fill="#0284C7" />
          <rect x="7" y="5" width="10" height="6" fill="#0369A1" />
          <rect x="8" y="7" width="8" height="4" fill="#0F172A" />
          <rect x="9" y="8" width="2" height="2" fill={eyeColor} />
          <rect x="13" y="8" width="2" height="2" fill={eyeColor} />
        </g>
      )}

      {clampedTier >= 3 && (
        <g>
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
        <g className={leftGearClass}>
          <rect x="4" y="13" width="3" height="3" fill="#F8FAFC" />
          <rect x="3" y="14" width="1" height="1" fill="#CBD5E1" />
          <rect x="5" y="11" width="1" height="1" fill="#94A3B8" />
        </g>
      )}
      {clampedTier === 2 && (
        <g className={leftGearClass}>
          <rect x="3" y="12" width="3" height="4" fill="#38BDF8" />
          <rect x="4" y="13" width="1" height="2" fill="#E0F2FE" />
        </g>
      )}
      {clampedTier === 3 && (
        <g className={leftGearClass}>
          <rect x="3" y="10" width="2" height="2" fill="#38BDF8" />
          <rect x="2" y="12" width="3" height="1" fill="#F5B942" />
          <rect x="3" y="13" width="2" height="2" fill="#38BDF8" />
        </g>
      )}
      {clampedTier >= 4 && (
        <g className={leftGearClass}>
          <rect x="2" y="12" width="4" height="5" fill="#7C3AED" />
          <rect x="3" y="13" width="2" height="3" fill="#E9D5FF" />
        </g>
      )}

      {/* Right-Hand Weapon by Tier (Reacts to mood pose) */}
      {clampedTier === 1 && (
        <g transform={weaponTransform}>
          <rect x="18" y="9" width="2" height="6" fill="#B45309" />
          <rect x="17" y="14" width="4" height="1" fill="#F5B942" />
          <rect x="18" y="15" width="2" height="2" fill="#78350F" />
        </g>
      )}
      {clampedTier >= 2 && (
        <g transform={weaponTransform}>
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
          <rect x="19" y="2" width="2" height="2" fill="#2DD4A0" />
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
  speechText?: string | null;
  onJumpHints: () => void;
  onJumpTests?: () => void;
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
  speechText,
  onJumpHints,
  onJumpTests,
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

  const activeSpeech = speechText?.trim() || SPEECH_BY_MOOD[mood];

  useEffect(() => {
    if (mood === 'idle' && !speechText) {
      setShowBubble(false);
      return;
    }
    setShowBubble(true);
    const timer = window.setTimeout(() => setShowBubble(false), 5200);
    return () => window.clearTimeout(timer);
  }, [mood, speechText]);

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
        <div
          className={`max-w-[270px] px-3 py-2 rounded-lg border text-xs shadow-lg leading-relaxed ${
            mood === 'victory'
              ? 'bg-[#102620] border-[#2DD4A0]/45 text-[#D1FAE5]'
              : mood === 'fail'
                ? 'bg-[#231219] border-[#F45D78]/45 text-[#FECDD3]'
                : 'bg-[#1C2230] border-white/[0.12] text-slate-100'
          }`}
        >
          {activeSpeech}
        </div>
      )}

      {menuOpen && (
        <div className="w-60 rpg-panel p-2.5 shadow-2xl space-y-1.5">
          <div className="px-2 py-1 text-[11px] font-medium text-slate-400 flex items-center gap-1.5">
            <Sparkles className="w-3 h-3 text-[#F5B942]" />
            <span>Companion Tactical Briefing</span>
          </div>
          <div className="px-2 py-1.5 rounded bg-[#0D1017] border border-white/[0.06] text-[11px] text-slate-300 leading-relaxed">
            {activeSpeech}
          </div>
          {onJumpTests && (
            <button
              type="button"
              onClick={() => {
                setMenuOpen(false);
                onJumpTests();
              }}
              className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-md text-xs text-slate-200 hover:bg-[#1C2230] hover:text-[#2DD4A0] cursor-pointer transition"
            >
              <FileCheck2 className="w-3.5 h-3.5" />
              <span>Open Verification Tests</span>
            </button>
          )}
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
          title="Click for tactical advice, Tests, Hints, or Oracle shortcuts"
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

export interface HeroArmoryModalProps {
  open: boolean;
  onClose: () => void;
  hero: HeroStatus;
  completedLessons: number;
  totalLessons: number;
  coldClearsCount: number;
  bossesDefeated: number;
  totalBosses: number;
  streakDays: number;
}

export const HeroArmoryModal: React.FC<HeroArmoryModalProps> = ({
  open,
  onClose,
  hero,
  completedLessons,
  totalLessons,
  coldClearsCount,
  bossesDefeated,
  totalBosses,
  streakDays,
}) => {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/75 backdrop-blur-[2px] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Hero Companion Evolution Armory"
    >
      <div className="rpg-panel-gold max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="px-5 py-4 border-b border-white/[0.08] bg-[#0D1017] flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <Shield className="w-4 h-4 text-[#F5B942]" />
            <div>
              <h2 className="text-sm font-semibold text-[#F8FAFC]">
                Hero Companion Evolution &amp; Armory
              </h2>
              <p className="text-xs text-slate-400">
                Clear all stages in a realm to unlock higher tiers ({hero.completedModules}/12
                modules cleared).
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer transition"
          >
            <span>Esc</span>
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {/* Combat & Mastery Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-3">
              <div className="text-[11px] text-slate-400">Stages Cleared</div>
              <div className="text-base font-bold text-[#2DD4A0] mt-0.5">
                {completedLessons} / {totalLessons}
              </div>
            </div>
            <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-3">
              <div className="text-[11px] text-slate-400">Cold Clears (No Hints)</div>
              <div className="text-base font-bold text-[#38BDF8] mt-0.5">{coldClearsCount}</div>
            </div>
            <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-3 flex items-center justify-between">
              <div>
                <div className="text-[11px] text-slate-400">Bosses Slain</div>
                <div className="text-base font-bold text-[#F45D78] mt-0.5">
                  {bossesDefeated} / {totalBosses}
                </div>
              </div>
              <Skull className="w-4 h-4 text-[#F45D78]/70" />
            </div>
            <div className="bg-[#0D1017] border border-white/[0.08] rounded-lg p-3 flex items-center justify-between">
              <div>
                <div className="text-[11px] text-slate-400">Active Streak</div>
                <div className="text-base font-bold text-[#F5B942] mt-0.5">{streakDays}d</div>
              </div>
              <Flame className="w-4 h-4 text-[#F5B942]/80" />
            </div>
          </div>

          {/* 5-Tier Evolution Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {HERO_TIER_CATALOG.map((item) => {
              const unlocked = hero.tier >= item.tier;
              const equipped = hero.tier === item.tier;
              return (
                <div
                  key={item.tier}
                  className={`rounded-lg border p-4 flex flex-col justify-between gap-3 transition ${
                    equipped
                      ? 'bg-[#231D11] border-[#F5B942]/70'
                      : unlocked
                        ? 'bg-[#0F241F]/60 border-[#2DD4A0]/40'
                        : 'bg-[#0D1017] border-white/[0.07] opacity-80'
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between gap-2 text-xs">
                      <span className="font-semibold text-[#F5B942]">Tier {item.tier}</span>
                      {equipped ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-[#F5B942]/20 text-[#F5B942] font-semibold">
                          <Sparkles className="w-3 h-3" />
                          <span>Equipped</span>
                        </span>
                      ) : unlocked ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-[#2DD4A0]/15 text-[#2DD4A0] font-medium">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>Unlocked</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-white/[0.05] text-slate-400">
                          <Lock className="w-3 h-3" />
                          <span>
                            {hero.completedModules}/{item.requiredModules} modules
                          </span>
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-3.5">
                      <div
                        className={`p-2 rounded-lg bg-[#0D1017] border ${
                          equipped
                            ? 'border-[#F5B942]/50'
                            : unlocked
                              ? 'border-[#2DD4A0]/35'
                              : 'border-white/[0.08] grayscale'
                        }`}
                      >
                        <HeroCompanionSprite
                          tier={item.tier}
                          mood={equipped ? 'victory' : 'idle'}
                          className="w-16 h-16"
                        />
                      </div>
                      <div className="min-w-0">
                        <div className="text-sm font-semibold text-[#F8FAFC]">{item.title}</div>
                        <div className="text-xs text-[#38BDF8] mt-0.5">{item.gearLabel}</div>
                      </div>
                    </div>

                    <p className="text-xs text-slate-400 leading-relaxed">{item.lore}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
