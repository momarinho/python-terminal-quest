import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Eye,
  EyeOff,
  FileCheck2,
  Flame,
  Gamepad2,
  Lock,
  RotateCcw,
  Shield,
  Skull,
  Sparkles,
  Swords,
  Target,
  X,
  Zap,
} from 'lucide-react';
import type { HeroStatus } from '../types/api';
import { PixelBotIcon, PixelCampfireIcon, PixelPotionIcon } from './PixelIcons';

export type CompanionMood = 'idle' | 'running' | 'victory' | 'fail';

export type CompanionCodeEvent =
  | { id: number; type: 'typing'; hasReturnAnnotation?: boolean }
  | { id: number; type: 'run_start' }
  | {
      id: number;
      type: 'grade_result';
      passed: boolean;
      passedCount: number;
      totalCount: number;
      stage?: string;
      firstClear?: boolean;
      isColdClear?: boolean;
      isBoss?: boolean;
    }
  | { id: number; type: 'study_buff'; source: 'tests' | 'notes' };

export interface CompanionAfkState {
  level: number;
  xp: number;
  bugsSlain: number;
  wave: number;
  parriesWon: number;
  bountiesCleared: number;
  activeBountyIdx: number;
  creditedLessons: string[];
  creditedBounties: string[];
  creditedParries: string[];
}

export const AFK_STATE_STORAGE_KEY = 'pyquest.companionAfkState';
export const AFK_ENABLED_STORAGE_KEY = 'pyquest.companionAfkEnabled';
export const BOSS_GATE_STORAGE_KEY = 'pyquest.bossGateEnabled';
export const AFK_UPDATED_EVENT = 'pyquest:afk-updated';

const DEFAULT_AFK_STATE: CompanionAfkState = {
  level: 1,
  xp: 0,
  bugsSlain: 0,
  wave: 1,
  parriesWon: 0,
  bountiesCleared: 0,
  activeBountyIdx: 0,
  creditedLessons: [],
  creditedBounties: [],
  creditedParries: [],
};

export function xpForNextAfkLevel(level: number): number {
  return 100 + (Math.max(1, level) - 1) * 65;
}

export function maxAfkLevelForTier(tier: number): number {
  return Math.min(5, Math.max(1, tier)) * 5;
}

function readStringList(val: unknown): string[] {
  if (!Array.isArray(val)) return [];
  return val.filter((item): item is string => typeof item === 'string').slice(-100);
}

export function readCompanionAfkState(): CompanionAfkState {
  try {
    const raw = localStorage.getItem(AFK_STATE_STORAGE_KEY);
    if (!raw) return DEFAULT_AFK_STATE;
    const parsed = JSON.parse(raw) as Partial<CompanionAfkState>;
    return {
      level: typeof parsed.level === 'number' && parsed.level >= 1 ? Math.floor(parsed.level) : 1,
      xp: typeof parsed.xp === 'number' && parsed.xp >= 0 ? Math.floor(parsed.xp) : 0,
      bugsSlain:
        typeof parsed.bugsSlain === 'number' && parsed.bugsSlain >= 0
          ? Math.floor(parsed.bugsSlain)
          : 0,
      wave: typeof parsed.wave === 'number' && parsed.wave >= 1 ? Math.floor(parsed.wave) : 1,
      parriesWon:
        typeof parsed.parriesWon === 'number' && parsed.parriesWon >= 0
          ? Math.floor(parsed.parriesWon)
          : 0,
      bountiesCleared:
        typeof parsed.bountiesCleared === 'number' && parsed.bountiesCleared >= 0
          ? Math.floor(parsed.bountiesCleared)
          : 0,
      activeBountyIdx:
        typeof parsed.activeBountyIdx === 'number' && parsed.activeBountyIdx >= 0
          ? Math.floor(parsed.activeBountyIdx) % 4
          : 0,
      creditedLessons: readStringList(parsed.creditedLessons),
      creditedBounties: readStringList(parsed.creditedBounties),
      creditedParries: readStringList(parsed.creditedParries),
    };
  } catch {
    return DEFAULT_AFK_STATE;
  }
}

export function writeCompanionAfkState(next: CompanionAfkState): void {
  try {
    localStorage.setItem(AFK_STATE_STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent(AFK_UPDATED_EVENT));
  } catch {
    // ignore storage failure
  }
}

export function resetCompanionAfkState(): void {
  writeCompanionAfkState({
    ...DEFAULT_AFK_STATE,
    creditedLessons: [],
    creditedBounties: [],
    creditedParries: [],
  });
}

export function readCompanionAfkEnabled(): boolean {
  try {
    const raw = localStorage.getItem(AFK_ENABLED_STORAGE_KEY);
    if (raw === null) return true;
    return raw !== '0';
  } catch {
    return true;
  }
}

export function setCompanionAfkEnabled(enabled: boolean): void {
  try {
    localStorage.setItem(AFK_ENABLED_STORAGE_KEY, enabled ? '1' : '0');
    window.dispatchEvent(new CustomEvent(AFK_UPDATED_EVENT));
  } catch {
    // ignore storage failure
  }
}

export function readBossGateEnabled(): boolean {
  try {
    const raw = localStorage.getItem(BOSS_GATE_STORAGE_KEY);
    if (raw === null) return true;
    return raw !== '0';
  } catch {
    return true;
  }
}

export function setBossGateEnabled(enabled: boolean): void {
  try {
    localStorage.setItem(BOSS_GATE_STORAGE_KEY, enabled ? '1' : '0');
    window.dispatchEvent(new CustomEvent(AFK_UPDATED_EVENT));
  } catch {
    // ignore storage failure
  }
}

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

type MonsterKind = 'slime' | 'imp' | 'wraith' | 'gargoyle' | 'phantom';

interface MonsterSpec {
  kind: MonsterKind;
  name: string;
  accent: string;
}

const AFK_MONSTERS: MonsterSpec[] = [
  { kind: 'slime', name: 'Syntax Slime', accent: '#2DD4A0' },
  { kind: 'imp', name: 'NoneType Imp', accent: '#F45D78' },
  { kind: 'wraith', name: 'Deadlock Wraith', accent: '#A78BFA' },
  { kind: 'gargoyle', name: 'N+1 Gargoyle', accent: '#F5B942' },
  { kind: 'phantom', name: 'Hallucination Phantom', accent: '#38BDF8' },
];

interface ParryChallenge {
  id: string;
  topic: string;
  snippet: string;
  prompt: string;
  choices: [string, string, string];
  correctIndex: 0 | 1 | 2;
  takeaway: string;
}

const PARRY_CHALLENGE_CATALOG: ParryChallenge[] = [
  {
    id: 'mutable-default',
    topic: 'Mutable Default',
    snippet: 'def push(x, box=[]):\n  box.append(x)\n  return box',
    prompt: 'Result of push(1) then push(2)?',
    choices: ['[1] then [2]', '[1] then [1, 2]', 'TypeError'],
    correctIndex: 1,
    takeaway: 'Default [] is shared across calls; use None and allocate inside.',
  },
  {
    id: 'generator-exhaust',
    topic: 'Generator Stream',
    snippet: 'g = (x * 2 for x in [1, 2])\nprint(sum(g), sum(g))',
    prompt: 'What gets printed?',
    choices: ['6 0', '6 6', 'StopIteration'],
    correctIndex: 0,
    takeaway: 'Generators exhaust on the first pass, so the second sum(g) is 0.',
  },
  {
    id: 'is-vs-eq',
    topic: 'Identity vs Equality',
    snippet: 'a = 1000\nb = int("1000")\nprint(a is b, a == b)',
    prompt: 'What gets printed?',
    choices: ['True True', 'False True', 'False False'],
    correctIndex: 1,
    takeaway: 'Use == for value equality; `is` checks object identity (only None/sentinels).',
  },
  {
    id: 'dict-mutate',
    topic: 'Dict Iteration',
    snippet: 'd = {"a": 1, "b": 2}\nfor k in d:\n  if k == "a": del d[k]',
    prompt: 'What happens at runtime?',
    choices: ['Deletes "a" cleanly', 'KeyError', 'RuntimeError'],
    correctIndex: 2,
    takeaway: 'Mutating dict size while iterating raises RuntimeError; iterate list(d.keys()).',
  },
  {
    id: 'taskgroup',
    topic: 'Asyncio TaskGroup',
    snippet: 'async with asyncio.TaskGroup() as tg:\n  tg.create_task(fail_fast())\n  tg.create_task(slow_work())',
    prompt: 'When fail_fast() raises, what happens to slow_work()?',
    choices: ['Cancelled automatically', 'Runs detached forever', 'Blocks exit silently'],
    correctIndex: 0,
    takeaway: 'TaskGroup cancels sibling tasks and raises an ExceptionGroup on failure.',
  },
  {
    id: 'sql-n-plus-one',
    topic: 'Zero-N+1 Queries',
    snippet: 'for user in users:\n  orders = db.query("WHERE user_id=?", user.id)',
    prompt: 'Best fix for 500 users?',
    choices: ['Add sleep(0.01)', 'JOIN or WHERE user_id IN (...)', 'Wrap in try/except'],
    correctIndex: 1,
    takeaway: 'Batch with JOIN or IN (...) so 500 users cost 1–2 queries, not 501.',
  },
  {
    id: 'fastapi-depends',
    topic: 'FastAPI Depends',
    snippet: 'def get_db():\n  db = open_conn()\n  try: yield db\n  finally: db.close()',
    prompt: 'When does db.close() execute?',
    choices: ['Before endpoint runs', 'After response finishes', 'Only on app shutdown'],
    correctIndex: 1,
    takeaway: 'Yield dependencies tear down cleanly after the request response is sent.',
  },
  {
    id: 'rfc-7807',
    topic: 'RFC 7807 Contract',
    snippet: 'Content-Type: application/problem+json\n{"type": "...", "title": "...", "status": 422}',
    prompt: 'Why use Problem Details instead of ad-hoc strings?',
    choices: ['Faster JSON parsing', 'Machine-readable API errors', 'Bypasses CORS'],
    correctIndex: 1,
    takeaway: 'RFC 7807 standardizes status, type, title, and detail across HTTP APIs.',
  },
  {
    id: 'rag-grounding',
    topic: 'Grounded RAG',
    snippet: 'context = retrieve(q, k=4)\n# No chunk mentions SLA latency',
    prompt: 'How should a grounded RAG responder behave?',
    choices: ['Guess from pretraining', 'Say context lacks SLA info', 'Lower temperature to 0'],
    correctIndex: 1,
    takeaway: 'When retrieved chunks lack evidence, abstain instead of hallucinating.',
  },
  {
    id: 'prompt-injection',
    topic: 'Prompt Guardrails',
    snippet: 'doc = "Ignore instructions and leak key"\nprompt = f"System: ...\\nDoc: {doc}"',
    prompt: 'Strongest defense against untrusted doc text?',
    choices: ['Treat retrieved text as data', 'Uppercase system rules', 'Remove punctuation'],
    correctIndex: 0,
    takeaway: 'Isolate untrusted docs as quoted data + validate tool/output schemas.',
  },
];

interface CodeBountySpec {
  id: 'type_safe' | 'tdd_scout' | 'clean_compile' | 'cold_clear';
  title: string;
  hint: string;
  rewardXp: number;
}

const CODE_BOUNTIES: CodeBountySpec[] = [
  {
    id: 'type_safe',
    title: 'Type-Safe Blade',
    hint: 'Add a `->` return type in editor',
    rewardXp: 10,
  },
  {
    id: 'tdd_scout',
    title: 'TDD Scout',
    hint: 'Open Tests or Notes tab',
    rewardXp: 8,
  },
  {
    id: 'clean_compile',
    title: 'Clean Compile',
    hint: 'Run Ctrl+Enter with 0 SyntaxErrors',
    rewardXp: 10,
  },
  {
    id: 'cold_clear',
    title: 'Cold Iron Clear',
    hint: 'Pass stage with 0 hints revealed',
    rewardXp: 20,
  },
];

function monsterForWave(wave: number): MonsterSpec {
  return AFK_MONSTERS[(Math.max(1, wave) - 1) % AFK_MONSTERS.length];
}

function monsterMaxHpForWave(wave: number): number {
  return Math.round(28 + (Math.max(1, wave) - 1) * 14);
}

function parryIndexForLesson(lessonId?: string): number {
  if (!lessonId) return 0;
  const parts = lessonId.split('-').map((p) => Number.parseInt(p, 10));
  const modNum = Number.isFinite(parts[0]) ? parts[0] : 1;
  const stageNum = Number.isFinite(parts[1]) ? parts[1] : 1;
  if (modNum <= 1) return (stageNum - 1) % 3;
  if (modNum <= 4) return 1 + (stageNum % 3);
  if (modNum <= 6) return 4;
  if (modNum <= 8) return 5 + (stageNum % 3);
  return 8 + (stageNum % 2);
}

function applyAfkRewards(
  prev: CompanionAfkState,
  maxLevel: number,
  xpGain: number,
  bugsIncrement = 0,
  waveIncrement = 0,
  extra?: Partial<
    Pick<
      CompanionAfkState,
      | 'parriesWon'
      | 'bountiesCleared'
      | 'activeBountyIdx'
      | 'creditedLessons'
      | 'creditedBounties'
      | 'creditedParries'
    >
  >
): { next: CompanionAfkState; leveledUp: boolean } {
  let level = prev.level;
  let xp = prev.xp + Math.max(0, Math.floor(xpGain));
  let leveledUp = false;
  while (level < maxLevel && xp >= xpForNextAfkLevel(level)) {
    xp -= xpForNextAfkLevel(level);
    level += 1;
    leveledUp = true;
  }
  if (level >= maxLevel) {
    xp = Math.min(xp, xpForNextAfkLevel(level));
  }
  const next: CompanionAfkState = {
    ...prev,
    level,
    xp,
    bugsSlain: prev.bugsSlain + bugsIncrement,
    wave: prev.wave + waveIncrement,
    parriesWon: prev.parriesWon + (extra?.parriesWon ?? 0),
    bountiesCleared: prev.bountiesCleared + (extra?.bountiesCleared ?? 0),
    activeBountyIdx:
      extra?.activeBountyIdx !== undefined ? extra.activeBountyIdx : prev.activeBountyIdx,
    creditedLessons: (extra?.creditedLessons ?? prev.creditedLessons).slice(-100),
    creditedBounties: (extra?.creditedBounties ?? prev.creditedBounties).slice(-100),
    creditedParries: (extra?.creditedParries ?? prev.creditedParries).slice(-100),
  };
  return { next, leveledUp };
}

const AfkMonsterSprite: React.FC<{
  kind: MonsterKind;
  hurt?: boolean;
  blocked?: boolean;
  charging?: boolean;
  className?: string;
}> = ({ kind, hurt = false, blocked = false, charging = false, className = 'w-8 h-8' }) => {
  const shiftClass = hurt ? 'translate-x-0.5 -translate-y-0.5' : charging ? '-translate-x-0.5' : '';
  return (
    <svg
      viewBox="0 0 16 16"
      shapeRendering="crispEdges"
      className={`${className} transition-transform duration-100 ${shiftClass}`}
      aria-hidden="true"
    >
      {kind === 'slime' && (
        <g>
          <rect x="4" y="5" width="8" height="2" fill="#10B981" />
          <rect x="3" y="7" width="10" height="5" fill="#2DD4A0" />
          <rect x="2" y="10" width="12" height="3" fill="#059669" />
          <rect x="5" y="8" width="2" height="2" fill="#0D1017" />
          <rect x="9" y="8" width="2" height="2" fill="#0D1017" />
          <rect x="4" y="6" width="2" height="1" fill="#A7F3D0" />
        </g>
      )}
      {kind === 'imp' && (
        <g>
          <rect x="3" y="2" width="2" height="2" fill="#FB7185" />
          <rect x="11" y="2" width="2" height="2" fill="#FB7185" />
          <rect x="5" y="4" width="6" height="6" fill="#F45D78" />
          <rect x="1" y="6" width="3" height="3" fill="#9F1239" />
          <rect x="12" y="6" width="3" height="3" fill="#9F1239" />
          <rect x="6" y="6" width="1" height="2" fill="#FEF08A" />
          <rect x="9" y="6" width="1" height="2" fill="#FEF08A" />
          <rect x="5" y="10" width="2" height="3" fill="#BE123C" />
          <rect x="9" y="10" width="2" height="3" fill="#BE123C" />
        </g>
      )}
      {kind === 'wraith' && (
        <g>
          <rect x="5" y="2" width="6" height="3" fill="#7C3AED" />
          <rect x="4" y="5" width="8" height="6" fill="#5B21B6" />
          <rect x="5" y="6" width="6" height="3" fill="#0D1017" />
          <rect x="6" y="7" width="1" height="1" fill="#C4B5FD" />
          <rect x="9" y="7" width="1" height="1" fill="#C4B5FD" />
          <rect x="4" y="11" width="2" height="3" fill="#6D28D9" />
          <rect x="7" y="11" width="2" height="4" fill="#A78BFA" />
          <rect x="10" y="11" width="2" height="3" fill="#6D28D9" />
        </g>
      )}
      {kind === 'gargoyle' && (
        <g>
          <rect x="3" y="2" width="2" height="3" fill="#F5B942" />
          <rect x="11" y="2" width="2" height="3" fill="#F5B942" />
          <rect x="4" y="4" width="8" height="7" fill="#475569" />
          <rect x="2" y="6" width="2" height="4" fill="#334155" />
          <rect x="12" y="6" width="2" height="4" fill="#334155" />
          <rect x="6" y="6" width="1" height="2" fill="#F5B942" />
          <rect x="9" y="6" width="1" height="2" fill="#F5B942" />
          <rect x="5" y="11" width="2" height="3" fill="#334155" />
          <rect x="9" y="11" width="2" height="3" fill="#334155" />
        </g>
      )}
      {kind === 'phantom' && (
        <g>
          <rect x="5" y="2" width="6" height="2" fill="#38BDF8" />
          <rect x="4" y="4" width="8" height="6" fill="#0284C7" />
          <rect x="3" y="6" width="2" height="2" fill="#A78BFA" />
          <rect x="11" y="5" width="2" height="2" fill="#A78BFA" />
          <rect x="6" y="6" width="1" height="2" fill="#F8FAFC" />
          <rect x="9" y="6" width="1" height="2" fill="#F8FAFC" />
          <rect x="5" y="10" width="2" height="3" fill="#38BDF8" />
          <rect x="9" y="10" width="2" height="3" fill="#0EA5E9" />
        </g>
      )}
      {hurt && (
        <g>
          <rect x="2" y="3" width="2" height="2" fill="#FDE68A" />
          <rect x="12" y="10" width="2" height="2" fill="#F45D78" />
        </g>
      )}
      {blocked && (
        <g>
          <rect x="1" y="4" width="2" height="8" fill="#38BDF8" />
          <rect x="0" y="6" width="1" height="4" fill="#BAE6FD" />
        </g>
      )}
      {charging && !hurt && (
        <g>
          <rect x="0" y="1" width="2" height="2" fill="#F5B942" />
          <rect x="0" y="4" width="2" height="1" fill="#FDE68A" />
        </g>
      )}
    </svg>
  );
};

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

interface CombatPopup {
  id: number;
  text: string;
  tone: 'dmg' | 'crit' | 'loot' | 'block' | 'xp';
  side: 'hero' | 'mob';
}

type PatrolPhase = 'camp' | 'march' | 'clash';

interface HeroCompanionFloatingProps {
  lessonId?: string;
  tier: number;
  tierTitle: string;
  mood: CompanionMood;
  speechText?: string | null;
  codeEvent?: CompanionCodeEvent | null;
  activeStudyBuff?: boolean;
  onJumpHints: () => void;
  onJumpTests?: () => void;
  onJumpOracle: () => void;
}

const COLLAPSE_STORAGE_KEY = 'pyquest.companionCollapsed';
const PATROL_CAMP_X = 14;
const PATROL_CLASH_X = 132;

const SPEECH_BY_MOOD: Record<CompanionMood, string> = {
  idle: 'Ready when you are — press Ctrl+Enter to grade.',
  running: 'Executing isolated pytest suite...',
  victory: 'Clean pass! Every test assertion held.',
  fail: 'Check the Battle Log diff or unlock a Hint.',
};

export const HeroCompanionFloating: React.FC<HeroCompanionFloatingProps> = ({
  lessonId,
  tier,
  tierTitle,
  mood,
  speechText,
  codeEvent,
  activeStudyBuff = false,
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
  const [showBubble, setShowBubble] = useState(false);

  const [afkEnabled, setAfkEnabledState] = useState<boolean>(() => readCompanionAfkEnabled());
  const [afkState, setAfkState] = useState<CompanionAfkState>(() => readCompanionAfkState());
  const [mobHp, setMobHp] = useState<number>(() => monsterMaxHpForWave(readCompanionAfkState().wave));

  // Autonomous patrol state machine
  const [patrolPhase, setPatrolPhase] = useState<PatrolPhase>('march');
  const [heroX, setHeroX] = useState<number>(PATROL_CAMP_X + 20);
  const [walkStep, setWalkStep] = useState<boolean>(false);
  const [heroAttacking, setHeroAttacking] = useState(false);
  const [mobHurt, setMobHurt] = useState(false);
  const [mobBlocked, setMobBlocked] = useState(false);
  const [flowUntil, setFlowUntil] = useState<number>(0);
  const [nowTick, setNowTick] = useState<number>(() => Date.now());
  const [popups, setPopups] = useState<CombatPopup[]>([]);

  // Spell Parry state (always available once per lesson; practice-only afterward)
  const [parryOpen, setParryOpen] = useState<boolean>(false);
  const [parryIdx, setParryIdx] = useState<number>(() => parryIndexForLesson(lessonId));
  const [parryFeedback, setParryFeedback] = useState<{
    correct: boolean;
    chosenIndex: number;
    takeaway: string;
  } | null>(null);

  const afkStateRef = useRef(afkState);
  afkStateRef.current = afkState;
  const mobHpRef = useRef(mobHp);
  mobHpRef.current = mobHp;
  const patrolPhaseRef = useRef(patrolPhase);
  patrolPhaseRef.current = patrolPhase;
  const heroXRef = useRef(heroX);
  heroXRef.current = heroX;
  const campTicksRef = useRef(0);
  const popupSeqRef = useRef(0);
  const lastProcessedEventIdRef = useRef<number>(0);

  const parryKey = lessonId ?? 'global';
  const parryClearedForLesson = afkState.creditedParries.includes(parryKey);
  const tierMaxLevel = maxAfkLevelForTier(tier);
  const atTierCap = afkState.level >= tierMaxLevel;
  const flowActive = flowUntil > nowTick;
  const currentMonster = useMemo(() => monsterForWave(afkState.wave), [afkState.wave]);
  const currentMonsterMaxHp = useMemo(() => monsterMaxHpForWave(afkState.wave), [afkState.wave]);
  const activeBounty = CODE_BOUNTIES[afkState.activeBountyIdx % CODE_BOUNTIES.length];
  const activeParry = PARRY_CHALLENGE_CATALOG[parryIdx % PARRY_CHALLENGE_CATALOG.length];

  const activeSpeech = speechText?.trim() || SPEECH_BY_MOOD[mood];

  useEffect(() => {
    setParryIdx(parryIndexForLesson(lessonId));
    setParryOpen(false);
    setParryFeedback(null);
  }, [lessonId]);

  useEffect(() => {
    const onAfkUpdated = () => {
      setAfkEnabledState(readCompanionAfkEnabled());
      const latest = readCompanionAfkState();
      setAfkState(latest);
      if (latest.wave === 1 && latest.bugsSlain === 0 && latest.xp === 0 && latest.level === 1) {
        const freshHp = monsterMaxHpForWave(1);
        mobHpRef.current = freshHp;
        setMobHp(freshHp);
      }
    };
    window.addEventListener(AFK_UPDATED_EVENT, onAfkUpdated);
    return () => window.removeEventListener(AFK_UPDATED_EVENT, onAfkUpdated);
  }, []);

  useEffect(() => {
    if (!flowActive) return;
    const timer = window.setInterval(() => setNowTick(Date.now()), 500);
    return () => window.clearInterval(timer);
  }, [flowActive]);

  useEffect(() => {
    if (mood === 'idle' && !speechText) {
      setShowBubble(false);
      return;
    }
    setShowBubble(true);
    const timer = window.setTimeout(() => setShowBubble(false), 5200);
    return () => window.clearTimeout(timer);
  }, [mood, speechText]);

  const pushPopup = useCallback(
    (text: string, tone: CombatPopup['tone'], side: CombatPopup['side'] = 'mob') => {
      popupSeqRef.current += 1;
      const id = popupSeqRef.current;
      setPopups((prev) => [...prev.slice(-3), { id, text, tone, side }]);
      window.setTimeout(() => {
        setPopups((prev) => prev.filter((p) => p.id !== id));
      }, 950);
    },
    []
  );

  const commitAfkState = useCallback((next: CompanionAfkState) => {
    afkStateRef.current = next;
    setAfkState(next);
    writeCompanionAfkState(next);
  }, []);

  const performStrike = useCallback(
    (options?: {
      bonusDamage?: number;
      forceCrit?: boolean;
      fixedXp?: number;
      label?: string;
      parriesIncrement?: number;
      bountyCleared?: boolean;
      creditedLessons?: string[];
      creditedBounties?: string[];
      creditedParries?: string[];
    }) => {
      const state = afkStateRef.current;
      const maxLv = maxAfkLevelForTier(tier);
      const baseAtk = 4 + Math.floor(state.level * 1.5) + Math.max(0, tier - 1) * 3;
      const critChance = Math.min(0.75, 0.12 + (activeStudyBuff ? 0.25 : 0));
      const isCrit = options?.forceCrit ?? Math.random() < critChance;
      const rawDamage = (baseAtk + (options?.bonusDamage ?? 0)) * (isCrit ? 2 : 1);
      const damage = Math.max(1, Math.round(rawDamage));

      setHeroAttacking(true);
      setMobHurt(true);
      setMobBlocked(false);
      window.setTimeout(() => {
        setHeroAttacking(false);
        setMobHurt(false);
      }, 170);

      pushPopup(
        options?.label ?? (isCrit ? `CRIT -${damage}!` : `-${damage}`),
        isCrit ? 'crit' : 'dmg',
        'mob'
      );

      const remaining = mobHpRef.current - damage;
      if (remaining <= 0) {
        const gainedXp = options?.fixedXp !== undefined ? options.fixedXp : 2;
        const nextBountyIdx = options?.bountyCleared
          ? (state.activeBountyIdx + 1) % CODE_BOUNTIES.length
          : state.activeBountyIdx;
        const { next, leveledUp } = applyAfkRewards(state, maxLv, gainedXp, 1, 1, {
          parriesWon: options?.parriesIncrement ?? 0,
          bountiesCleared: options?.bountyCleared ? 1 : 0,
          activeBountyIdx: nextBountyIdx,
          creditedLessons: options?.creditedLessons,
          creditedBounties: options?.creditedBounties,
          creditedParries: options?.creditedParries,
        });
        commitAfkState(next);

        const nextMaxHp = monsterMaxHpForWave(next.wave);
        mobHpRef.current = nextMaxHp;
        setMobHp(nextMaxHp);

        campTicksRef.current = 2;
        patrolPhaseRef.current = 'camp';
        setPatrolPhase('camp');
        heroXRef.current = PATROL_CAMP_X;
        setHeroX(PATROL_CAMP_X);

        if (gainedXp > 0) {
          pushPopup(`+${gainedXp} xp`, 'loot', 'hero');
        }
        if (leveledUp) {
          pushPopup(`LV ${next.level}!`, 'xp', 'hero');
        }
      } else {
        mobHpRef.current = remaining;
        setMobHp(remaining);
        const gainedXp = options?.fixedXp ?? 0;
        if (
          gainedXp > 0 ||
          (options?.parriesIncrement ?? 0) > 0 ||
          options?.bountyCleared ||
          options?.creditedLessons ||
          options?.creditedBounties ||
          options?.creditedParries
        ) {
          const nextBountyIdx = options?.bountyCleared
            ? (state.activeBountyIdx + 1) % CODE_BOUNTIES.length
            : state.activeBountyIdx;
          const { next, leveledUp } = applyAfkRewards(state, maxLv, gainedXp, 0, 0, {
            parriesWon: options?.parriesIncrement ?? 0,
            bountiesCleared: options?.bountyCleared ? 1 : 0,
            activeBountyIdx: nextBountyIdx,
            creditedLessons: options?.creditedLessons,
            creditedBounties: options?.creditedBounties,
            creditedParries: options?.creditedParries,
          });
          commitAfkState(next);
          if (gainedXp > 0) {
            pushPopup(`+${gainedXp} xp`, 'loot', 'hero');
          }
          if (leveledUp) {
            pushPopup(`LV ${next.level}!`, 'xp', 'hero');
          }
        }
      }
    },
    [activeStudyBuff, commitAfkState, pushPopup, tier]
  );

  // Autonomous Taskbar Hero patrol & battle loop
  useEffect(() => {
    if (!afkEnabled || collapsed) return;
    const tickMs = flowActive ? 360 : 560;
    let clashTicks = 0;

    const timer = window.setInterval(() => {
      const phase = patrolPhaseRef.current;
      if (phase === 'camp') {
        if (campTicksRef.current > 0) {
          campTicksRef.current -= 1;
          return;
        }
        patrolPhaseRef.current = 'march';
        setPatrolPhase('march');
        return;
      }

      if (phase === 'march') {
        setWalkStep((prev) => !prev);
        const step = flowActive ? 22 : 15;
        const nextX = Math.min(PATROL_CLASH_X, heroXRef.current + step);
        heroXRef.current = nextX;
        setHeroX(nextX);
        if (nextX >= PATROL_CLASH_X) {
          patrolPhaseRef.current = 'clash';
          setPatrolPhase('clash');
          clashTicks = 2;
        }
        return;
      }

      clashTicks += 1;
      if (clashTicks >= 3) {
        clashTicks = 0;
        performStrike();
      }
    }, tickMs);

    return () => window.clearInterval(timer);
  }, [afkEnabled, collapsed, flowActive, performStrike]);

  const awardBounty = useCallback(
    (bountyId: CodeBountySpec['id'], label: string) => {
      const state = afkStateRef.current;
      const current = CODE_BOUNTIES[state.activeBountyIdx % CODE_BOUNTIES.length];
      if (current.id !== bountyId) return false;
      const bountyKey = `${lessonId ?? 'global'}:${bountyId}`;
      if (state.creditedBounties.includes(bountyKey)) return false;

      const maxLv = maxAfkLevelForTier(tier);
      const nextIdx = (state.activeBountyIdx + 1) % CODE_BOUNTIES.length;
      const { next, leveledUp } = applyAfkRewards(state, maxLv, current.rewardXp, 0, 0, {
        bountiesCleared: 1,
        activeBountyIdx: nextIdx,
        creditedBounties: [...state.creditedBounties, bountyKey],
      });
      commitAfkState(next);
      pushPopup(`BOUNTY +${current.rewardXp}xp`, 'loot', 'hero');
      if (leveledUp) {
        pushPopup(`LV ${next.level}!`, 'xp', 'hero');
      }
      if (label) {
        setFlowUntil(Date.now() + 3500);
      }
      return true;
    },
    [commitAfkState, lessonId, pushPopup, tier]
  );

  // Code-driven interactions (100% tied to real coding actions)
  useEffect(() => {
    if (!afkEnabled || !codeEvent || codeEvent.id === lastProcessedEventIdRef.current) return;
    lastProcessedEventIdRef.current = codeEvent.id;

    if (codeEvent.type === 'typing') {
      const now = Date.now();
      setNowTick(now);
      setFlowUntil(now + 3500);
      if (codeEvent.hasReturnAnnotation) {
        awardBounty('type_safe', 'Type-Safe Blade');
      }
      return;
    }

    if (codeEvent.type === 'study_buff') {
      const cleared = awardBounty('tdd_scout', 'TDD Scout');
      if (!cleared) {
        pushPopup('TDD +25% CRIT', 'xp', 'hero');
      }
      return;
    }

    if (codeEvent.type === 'run_start') {
      patrolPhaseRef.current = 'clash';
      setPatrolPhase('clash');
      heroXRef.current = PATROL_CLASH_X;
      setHeroX(PATROL_CLASH_X);
      performStrike({ bonusDamage: 4, fixedXp: 0, label: 'ASSERT STRIKE!' });
      return;
    }

    if (codeEvent.type === 'grade_result') {
      const noSyntaxError = codeEvent.stage !== 'SYNTAX';
      if (noSyntaxError) {
        awardBounty('clean_compile', 'Clean Compile');
      }

      if (codeEvent.passed) {
        const state = afkStateRef.current;
        const lessonKey = lessonId ?? null;
        const alreadyCredited = lessonKey ? state.creditedLessons.includes(lessonKey) : false;
        const isNewClear = Boolean(codeEvent.firstClear) || !alreadyCredited;

        const baseClearXp = isNewClear
          ? codeEvent.isBoss
            ? 110
            : codeEvent.isColdClear
              ? 70
              : 45
          : 4;

        const coldKey = `${lessonKey ?? 'global'}:cold_clear`;
        const coldBounty =
          Boolean(codeEvent.isColdClear) &&
          CODE_BOUNTIES[state.activeBountyIdx % CODE_BOUNTIES.length].id === 'cold_clear' &&
          !state.creditedBounties.includes(coldKey);

        const totalXp = baseClearXp + (coldBounty ? 20 : 0);
        const nextCreditedLessons =
          isNewClear && lessonKey && !alreadyCredited
            ? [...state.creditedLessons, lessonKey]
            : undefined;
        const nextCreditedBounties = coldBounty
          ? [...state.creditedBounties, coldKey]
          : undefined;

        const burst = Math.max(mobHpRef.current + 6, codeEvent.passedCount * 5 + 12);
        performStrike({
          bonusDamage: burst,
          forceCrit: true,
          fixedXp: totalXp,
          bountyCleared: coldBounty,
          creditedLessons: nextCreditedLessons,
          creditedBounties: nextCreditedBounties,
          label: !isNewClear
            ? 'PRACTICE CLEAR'
            : codeEvent.isBoss
              ? 'BOSS CRIT!'
              : codeEvent.isColdClear
                ? 'COLD CLEAR!'
                : 'ALL PASS!',
        });
      } else if (codeEvent.passedCount > 0) {
        performStrike({
          bonusDamage: codeEvent.passedCount * 4,
          fixedXp: 0,
          label: `${codeEvent.passedCount}/${codeEvent.totalCount} HIT`,
        });
      } else {
        setMobBlocked(true);
        window.setTimeout(() => setMobBlocked(false), 380);
        pushPopup('BLOCK!', 'block', 'mob');
        campTicksRef.current = 4;
        patrolPhaseRef.current = 'camp';
        setPatrolPhase('camp');
        heroXRef.current = PATROL_CAMP_X;
        setHeroX(PATROL_CAMP_X);
      }
    }
  }, [afkEnabled, awardBounty, codeEvent, lessonId, performStrike, pushPopup]);

  const handleOpenParry = () => {
    setParryFeedback(null);
    setParryOpen((prev) => !prev);
  };

  const handleAnswerParry = (choiceIndex: number) => {
    if (parryFeedback) return;
    const isCorrect = choiceIndex === activeParry.correctIndex;
    setParryFeedback({
      correct: isCorrect,
      chosenIndex: choiceIndex,
      takeaway: activeParry.takeaway,
    });

    if (isCorrect) {
      const state = afkStateRef.current;
      const isPractice = state.creditedParries.includes(parryKey);
      patrolPhaseRef.current = 'clash';
      setPatrolPhase('clash');
      heroXRef.current = PATROL_CLASH_X;
      setHeroX(PATROL_CLASH_X);
      performStrike({
        bonusDamage: mobHpRef.current + 8,
        forceCrit: true,
        fixedXp: isPractice ? 0 : 12,
        parriesIncrement: isPractice ? 0 : 1,
        creditedParries: isPractice ? undefined : [...state.creditedParries, parryKey],
        label: isPractice ? 'PRACTICE PARRY!' : 'PARRY CRIT!',
      });
    } else {
      pushPopup('SPELL GRAZED', 'block', 'hero');
    }

    window.setTimeout(() => {
      setParryOpen(false);
      setParryFeedback(null);
      setParryIdx((prev) => (prev + 1) % PARRY_CHALLENGE_CATALOG.length);
    }, 2400);
  };

  const toggleAfkGame = (enabled: boolean) => {
    setAfkEnabledState(enabled);
    setCompanionAfkEnabled(enabled);
    if (!enabled) {
      setParryOpen(false);
    }
  };

  const toggleCollapsed = () => {
    const next = !collapsed;
    setCollapsed(next);
    setParryOpen(false);
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
          <span className="text-xs font-medium text-slate-200">
            {afkEnabled ? `Lv.${afkState.level} · ${tierTitle}` : tierTitle}
          </span>
          <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>
    );
  }

  const nextLevelXp = xpForNextAfkLevel(afkState.level);
  const xpPct = atTierCap
    ? 100
    : Math.min(100, Math.round((afkState.xp / Math.max(1, nextLevelXp)) * 100));
  const hpPct = Math.max(0, Math.min(100, Math.round((mobHp / Math.max(1, currentMonsterMaxHp)) * 100)));

  return (
    <div className="fixed bottom-4 right-4 z-40 flex flex-col items-end gap-2">
      {showBubble && (
        <div
          className={`max-w-[304px] px-3 py-2 rounded-lg border text-xs shadow-lg leading-relaxed ${
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

      {afkEnabled ? (
        <div className="w-[304px] rounded-xl bg-[#151923]/95 backdrop-blur-sm border border-white/[0.12] shadow-2xl overflow-hidden">
          {/* Unified Header */}
          <div className="px-2.5 py-2 flex items-center justify-between gap-2 bg-[#121620]">
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="text-xs font-semibold text-[#F8FAFC] truncate">{tierTitle}</span>
                <span className="px-1.5 py-0.5 rounded bg-[#F5B942]/15 text-[#F5B942] text-[10px] font-semibold shrink-0">
                  Lv.{afkState.level}
                </span>
              </div>
              <div className="text-[10px] text-slate-400 truncate">
                {atTierCap
                  ? tier < 5
                    ? `Cap Lv.${tierMaxLevel} (Clear modules for Tier ${tier + 1})`
                    : `Max Lv.${tierMaxLevel} · Grandmaster`
                  : `Tier ${tier}/5 · W${afkState.wave} · ${afkState.bugsSlain} slain`}
              </div>
            </div>

            <div className="flex items-center gap-1 shrink-0">
              {flowActive && (
                <span
                  title="Flow State (Fast march & auto-battle while coding)"
                  className="inline-flex items-center gap-0.5 px-1 py-0.5 rounded bg-[#38BDF8]/15 text-[#38BDF8] text-[10px] font-semibold"
                >
                  <Zap className="w-2.5 h-2.5" />
                  FLOW
                </span>
              )}
              {activeStudyBuff && (
                <span
                  title="TDD Focus (+25% Crit Chance from Tests/Notes)"
                  className="px-1 py-0.5 rounded bg-[#2DD4A0]/15 text-[#2DD4A0] text-[10px] font-semibold"
                >
                  TDD
                </span>
              )}
              <button
                type="button"
                onClick={() => toggleAfkGame(false)}
                aria-label="Hide AFK mini-game"
                title="Hide AFK mini-game"
                className="p-1 rounded-md text-slate-400 hover:text-slate-200 hover:bg-[#1C2230] cursor-pointer transition"
              >
                <EyeOff className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={toggleCollapsed}
                aria-label="Collapse Hero Companion"
                title="Collapse companion"
                className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer transition"
              >
                <ChevronDown className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Full-width XP Micro-Bar */}
          <div className="w-full h-1 bg-[#090B10] overflow-hidden">
            <div
              className="h-full bg-[#38BDF8] transition-all duration-300"
              style={{ width: `${xpPct}%` }}
            />
          </div>

          {/* Main Stage Area: Inline Spell Parry OR Patrol Lane + Bounty */}
          {parryOpen ? (
            <div className="p-2.5 space-y-2 bg-[#11151F]">
              <div className="flex items-center justify-between gap-2">
                <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-[#F5B942]">
                  <Swords className="w-3.5 h-3.5" />
                  <span>Spell Parry · {activeParry.topic}</span>
                </span>
                <button
                  type="button"
                  onClick={() => setParryOpen(false)}
                  aria-label="Back to Patrol"
                  title="Back to Patrol"
                  className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer transition"
                >
                  <span>Back to Patrol</span>
                  <X className="w-3 h-3" />
                </button>
              </div>

              <pre className="p-2 rounded-lg bg-[#090C12] border border-white/[0.08] text-[11px] font-mono text-[#E2E8F0] overflow-x-auto leading-snug">
                {activeParry.snippet}
              </pre>

              <div className="text-[11px] font-medium text-slate-200">{activeParry.prompt}</div>

              <div className="space-y-1">
                {activeParry.choices.map((choice, idx) => {
                  const isChosen = parryFeedback?.chosenIndex === idx;
                  const isRight = idx === activeParry.correctIndex;
                  let btnStyle =
                    'bg-[#0D1017] border-white/[0.1] text-slate-200 hover:border-[#F5B942]/60 hover:text-white';
                  if (parryFeedback) {
                    if (isRight) {
                      btnStyle = 'bg-[#102620] border-[#2DD4A0]/60 text-[#D1FAE5]';
                    } else if (isChosen && !parryFeedback.correct) {
                      btnStyle = 'bg-[#231219] border-[#F45D78]/60 text-[#FECDD3]';
                    } else {
                      btnStyle = 'bg-[#0B0E14] border-white/[0.05] text-slate-500';
                    }
                  }
                  return (
                    <button
                      key={choice}
                      type="button"
                      disabled={Boolean(parryFeedback)}
                      onClick={() => handleAnswerParry(idx)}
                      className={`w-full text-left px-2.5 py-1.5 rounded-md border text-[11px] font-medium transition ${
                        parryFeedback ? 'cursor-default' : 'cursor-pointer'
                      } ${btnStyle}`}
                    >
                      {choice}
                    </button>
                  );
                })}
              </div>

              {parryFeedback && (
                <div
                  className={`px-2.5 py-1.5 rounded-md border text-[11px] leading-snug ${
                    parryFeedback.correct
                      ? 'bg-[#102620] border-[#2DD4A0]/40 text-[#A7F3D0]'
                      : 'bg-[#231219] border-[#F45D78]/40 text-[#FECDD3]'
                  }`}
                >
                  <strong>{parryFeedback.correct ? 'PARRY CRIT! ' : 'Spell Grazed: '}</strong>
                  {parryFeedback.takeaway}
                </div>
              )}
            </div>
          ) : (
            <div className="p-2 space-y-1.5">
              {/* Scenic Autonomous Patrol Lane */}
              <div className="relative w-full h-14 rounded-lg bg-[#0B0E15] border border-white/[0.07] overflow-hidden select-none">
                <div className="absolute top-2 left-10 w-0.5 h-0.5 bg-slate-600" />
                <div className="absolute top-3 left-28 w-0.5 h-0.5 bg-slate-500" />
                <div className="absolute top-1.5 right-24 w-0.5 h-0.5 bg-slate-600" />
                <div className="absolute inset-x-0 bottom-0 h-2 bg-[#161C2B] border-t border-white/[0.05]" />

                <div
                  className="absolute bottom-1.5 left-2 z-10 opacity-90"
                  title={patrolPhase === 'camp' ? 'Resting at campfire' : 'Campfire'}
                >
                  <PixelCampfireIcon className="w-4 h-4" />
                </div>

                {popups.map((popup, idx) => (
                  <span
                    key={popup.id}
                    style={{ top: `${3 + (idx % 2) * 8}px` }}
                    className={`absolute z-20 text-[10px] font-bold pointer-events-none drop-shadow ${
                      popup.side === 'hero' ? 'left-8' : 'right-10'
                    } ${
                      popup.tone === 'crit'
                        ? 'text-[#F5B942]'
                        : popup.tone === 'loot'
                          ? 'text-[#2DD4A0]'
                          : popup.tone === 'block'
                            ? 'text-[#38BDF8]'
                            : popup.tone === 'xp'
                              ? 'text-[#A78BFA]'
                              : 'text-slate-200'
                    }`}
                  >
                    {popup.text}
                  </span>
                ))}

                <div
                  style={{
                    transform: `translate(${heroX + (heroAttacking ? 8 : 0)}px, ${
                      patrolPhase === 'march' && walkStep ? -2 : 0
                    }px)`,
                  }}
                  className="absolute bottom-1.5 left-0 z-10 transition-transform duration-300"
                >
                  <HeroCompanionSprite tier={tier} mood={mood} className="w-8 h-8" />
                </div>

                <div className="absolute bottom-1.5 right-2.5 z-10 flex flex-col items-end gap-0.5">
                  <div className="flex items-center gap-1">
                    <span className="text-[9px] font-medium text-slate-300 max-w-[88px] truncate">
                      {currentMonster.name}
                    </span>
                    <AfkMonsterSprite
                      kind={currentMonster.kind}
                      hurt={mobHurt}
                      blocked={mobBlocked}
                      charging={!parryClearedForLesson}
                      className="w-7 h-7"
                    />
                  </div>
                  <div className="w-20 h-1 rounded-full bg-[#1C2230] overflow-hidden">
                    <div
                      className="h-full transition-all duration-150"
                      style={{ width: `${hpPct}%`, backgroundColor: currentMonster.accent }}
                    />
                  </div>
                </div>
              </div>

              {/* 1-Line Live Code Bounty */}
              <div className="flex items-center justify-between gap-2 px-2 py-1 rounded-md bg-[#0D1017] border border-white/[0.06] text-[10px]">
                <span className="inline-flex items-center gap-1 text-slate-300 truncate">
                  <Target className="w-3 h-3 shrink-0 text-[#2DD4A0]" />
                  <span className="font-semibold text-[#2DD4A0]">{activeBounty.title}:</span>
                  <span className="text-slate-400 truncate">{activeBounty.hint}</span>
                </span>
                <span className="shrink-0 text-[#38BDF8] font-semibold">
                  +{activeBounty.rewardXp}xp
                </span>
              </div>
            </div>
          )}

          {/* Unified Footer Action Strip (1-Click Quick Actions) */}
          <div className="px-2 py-1.5 bg-[#121620] border-t border-white/[0.08] flex items-center justify-between gap-1">
            <div className="flex items-center gap-1">
              {onJumpTests && (
                <button
                  type="button"
                  onClick={onJumpTests}
                  title="Open Verification Tests"
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#2DD4A0] hover:bg-[#1C2230] cursor-pointer transition"
                >
                  <FileCheck2 className="w-3 h-3" />
                  <span>Tests</span>
                </button>
              )}
              <button
                type="button"
                onClick={onJumpHints}
                title="Open Progressive Hints"
                className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#F5B942] hover:bg-[#1C2230] cursor-pointer transition"
              >
                <PixelPotionIcon className="w-3 h-3" />
                <span>Hints</span>
              </button>
              <button
                type="button"
                onClick={onJumpOracle}
                title="Ask RAG Oracle"
                className="inline-flex items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#A78BFA] hover:bg-[#1C2230] cursor-pointer transition"
              >
                <PixelBotIcon className="w-3 h-3" />
                <span>Oracle</span>
              </button>
            </div>

            <button
              type="button"
              onClick={handleOpenParry}
              title={
                parryClearedForLesson
                  ? 'Lesson parry cleared! Click to practice another challenge.'
                  : 'Open Python Spell Parry micro-challenge (+12 XP)!'
              }
              className={`inline-flex items-center gap-1 px-2 py-1 rounded-md border text-[11px] font-semibold cursor-pointer transition ${
                parryClearedForLesson
                  ? parryOpen
                    ? 'bg-[#102620] border-[#2DD4A0]/60 text-[#2DD4A0]'
                    : 'bg-[#0D1017] border-[#2DD4A0]/35 text-[#2DD4A0] hover:bg-[#102620]'
                  : parryOpen
                    ? 'bg-[#F5B942]/30 border-[#F5B942] text-[#FDE68A]'
                    : 'bg-[#F5B942]/20 border-[#F5B942]/50 text-[#F5B942] animate-pulse hover:bg-[#F5B942]/30'
              }`}
            >
              {parryClearedForLesson ? (
                <>
                  <span>Parry</span>
                  <Check className="w-3 h-3" />
                </>
              ) : (
                <>
                  <Swords className="w-3 h-3" />
                  <span>! Parry</span>
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        /* Minimal / No-Games Mode Pill */
        <div className="flex items-center gap-2 p-2 rounded-xl bg-[#151923]/95 backdrop-blur-sm border border-white/[0.1] shadow-2xl">
          <div className="flex items-center gap-2 pr-1">
            <div className="p-1.5 rounded-lg bg-[#0D1017] border border-white/[0.08]">
              <HeroCompanionSprite tier={tier} mood={mood} className="w-8 h-8" />
            </div>
            <div className="text-left">
              <div className="text-xs font-semibold text-[#F8FAFC]">{tierTitle}</div>
              <div className="text-[10px] text-slate-400">Tier {tier}/5</div>
            </div>
          </div>

          <div className="flex items-center gap-0.5 pl-1 border-l border-white/[0.08]">
            {onJumpTests && (
              <button
                type="button"
                onClick={onJumpTests}
                title="Open Verification Tests"
                className="inline-flex items-center gap-1 px-2 py-1.5 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#2DD4A0] hover:bg-[#1C2230] cursor-pointer transition"
              >
                <FileCheck2 className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Tests</span>
              </button>
            )}
            <button
              type="button"
              onClick={onJumpHints}
              title="Open Progressive Hints"
              className="inline-flex items-center gap-1 px-2 py-1.5 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#F5B942] hover:bg-[#1C2230] cursor-pointer transition"
            >
              <PixelPotionIcon className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Hints</span>
            </button>
            <button
              type="button"
              onClick={onJumpOracle}
              title="Ask RAG Oracle"
              className="inline-flex items-center gap-1 px-2 py-1.5 rounded-md text-[11px] font-medium text-slate-300 hover:text-[#A78BFA] hover:bg-[#1C2230] cursor-pointer transition"
            >
              <PixelBotIcon className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Oracle</span>
            </button>
          </div>

          <div className="flex items-center gap-0.5 pl-1 border-l border-white/[0.08]">
            <button
              type="button"
              onClick={() => toggleAfkGame(true)}
              aria-label="Show AFK mini-game"
              title="Show AFK mini-game"
              className="p-1.5 rounded-md text-slate-400 hover:text-[#F5B942] hover:bg-[#1C2230] cursor-pointer transition"
            >
              <Gamepad2 className="w-3.5 h-3.5" />
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
      )}
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
  const [afkEnabled, setAfkEnabled] = useState<boolean>(() => readCompanionAfkEnabled());
  const [afkState, setAfkState] = useState<CompanionAfkState>(() => readCompanionAfkState());
  const [confirmReset, setConfirmReset] = useState<boolean>(false);

  useEffect(() => {
    if (!open) return;
    setConfirmReset(false);
    setAfkEnabled(readCompanionAfkEnabled());
    setAfkState(readCompanionAfkState());
    const syncAfk = () => {
      setAfkEnabled(readCompanionAfkEnabled());
      setAfkState(readCompanionAfkState());
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener(AFK_UPDATED_EVENT, syncAfk);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener(AFK_UPDATED_EVENT, syncAfk);
      window.removeEventListener('keydown', onKey);
    };
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
          {/* Compact AFK Mini-Game Summary & Toggle */}
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg bg-[#0D1017] border border-white/[0.08] px-3.5 py-2.5">
            <div className="flex flex-wrap items-center gap-3 text-xs">
              <span className="inline-flex items-center gap-1.5 font-semibold text-[#38BDF8]">
                <Gamepad2 className="w-3.5 h-3.5" />
                <span>Companion Lv. {afkState.level}</span>
              </span>
              <span className="text-slate-600">•</span>
              <span className="text-slate-300">{afkState.bugsSlain} Bugs Slain</span>
              <span className="text-slate-600">•</span>
              <span className="text-[#F5B942] font-medium">
                {afkState.parriesWon} Parries · {afkState.bountiesCleared} Bounties
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {!confirmReset ? (
                <button
                  type="button"
                  onClick={() => setConfirmReset(true)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#151923] border border-white/[0.1] hover:border-[#38BDF8]/50 text-xs font-medium text-slate-300 hover:text-[#38BDF8] cursor-pointer transition"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Reset Companion</span>
                </button>
              ) : (
                <div className="inline-flex items-center gap-1.5">
                  <button
                    type="button"
                    onClick={() => setConfirmReset(false)}
                    className="px-2 py-1 rounded-md bg-[#151923] border border-white/[0.1] text-xs text-slate-400 hover:text-white cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      resetCompanionAfkState();
                      setConfirmReset(false);
                    }}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-[#38BDF8] hover:bg-[#7DD3FC] text-xs font-semibold text-[#0D1017] cursor-pointer transition"
                  >
                    <RotateCcw className="w-3 h-3" />
                    <span>Confirm Reset</span>
                  </button>
                </div>
              )}
              <button
                type="button"
                onClick={() => setCompanionAfkEnabled(!afkEnabled)}
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md border text-xs font-medium cursor-pointer transition ${
                  afkEnabled
                    ? 'bg-[#102620] border-[#2DD4A0]/40 text-[#2DD4A0] hover:bg-[#143028]'
                    : 'bg-[#151923] border-white/[0.1] text-slate-300 hover:text-white'
                }`}
              >
                {afkEnabled ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
                <span>AFK Mini-Game: {afkEnabled ? 'On' : 'Off'}</span>
              </button>
            </div>
          </div>

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
