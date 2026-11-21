export type LessonStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';
export type LessonMode = 'PYTHON_CORE' | 'PYTEST_TDD' | 'BUG_FIX' | 'FASTAPI' | 'AI_SYSTEMS';
export type LessonKind = 'STANDARD' | 'BOSS';
export type LessonRuntime = 'STANDARD' | 'WEB_INTEGRATION';

export interface LinkedinAngle {
  hook: string;
  pythonInsight: string;
  codeComparison: string;
}

export interface ModuleInsight {
  moduleId: string;
  linkedinAngle: LinkedinAngle;
  bossLinkedinAngle?: LinkedinAngle | null;
  reflectionPrompts: string[];
}

export interface StreakStats {
  currentStreakDays: number;
  longestStreakDays: number;
  activeToday: boolean;
  activeDaysTotal: number;
}

export interface HeroStatus {
  tier: number;
  title: string;
  subtitle: string;
  completedModules: number;
  completedLessons: number;
  earnedXp: number;
  nextTier: number | null;
  nextTierTitle: string | null;
  modulesForNextTier: number;
}

export interface LessonSummary {
  id: string;
  moduleId: string;
  moduleTitle: string;
  title: string;
  objective: string;
  mode: LessonMode;
  kind: LessonKind;
  runtime: LessonRuntime;
  xp: number;
  tags: string[];
  entryFile: string;
  status: LessonStatus;
  attempts: number;
  hintsRevealed: number;
  totalHints: number;
  flagged: boolean;
  hasNotes: boolean;
}

export interface ModuleGroup {
  id: string;
  title: string;
  totalLessons: number;
  completedLessons: number;
  totalXp: number;
  earnedXp: number;
  lessons: LessonSummary[];
  insight?: ModuleInsight | null;
}

export interface CurriculumResponse {
  totalLessons: number;
  completedLessons: number;
  inProgressLessons: number;
  notStartedLessons: number;
  totalXp: number;
  earnedXp: number;
  streak: StreakStats;
  hero: HeroStatus;
  modules: ModuleGroup[];
}

export interface LessonProgress {
  lessonId: string;
  status: LessonStatus;
  attempts: number;
  hintsRevealed: number;
  lastDiagnostics: string;
  notes: string;
  flagged: boolean;
  updatedAt: string;
}

export interface LessonDetail {
  id: string;
  moduleId: string;
  moduleTitle: string;
  title: string;
  objective: string;
  mode: LessonMode;
  kind: LessonKind;
  runtime: LessonRuntime;
  xp: number;
  tags: string[];
  entryFile: string;
  conceptMarkdown: string;
  files: Record<string, string>;
  unlockedHints: string[];
  totalHints: number;
  progress: LessonProgress;
  prevLessonId: string | null;
  nextLessonId: string | null;
}

export interface TestCaseResult {
  name: string;
  passed: boolean;
  message: string;
}

export interface Diagnostic {
  file: string;
  line: number;
  column?: number | null;
  severity: string;
  message: string;
}

export interface GradeResult {
  passed: boolean;
  stage: 'SYNTAX' | 'EXECUTION' | 'TEST' | 'PASSED';
  exitCode: number;
  stdout: string;
  stderr: string;
  testCases: TestCaseResult[];
  diagnostics: Diagnostic[];
  summary: string;
}

export interface RunResponse {
  result: GradeResult;
  progress: LessonProgress;
  hero: HeroStatus;
}

export interface HintResponse {
  lessonId: string;
  unlockedHints: string[];
  totalHints: number;
  progress: LessonProgress;
}

export interface OracleCitation {
  lessonId: string;
  title: string;
  snippet: string;
  score: number;
}

export interface OracleResponse {
  answer: string;
  provider: string;
  mode: 'stub' | 'offline-rag' | 'live-llm';
  citations: OracleCitation[];
  citedSources: string[];
  guardrailTriggered: boolean;
  latencyMs: number;
}

export type ProjectStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';

export interface ChecklistItemSpec {
  id: string;
  text: string;
}

export interface SprintSpec {
  id: string;
  title: string;
  items: ChecklistItemSpec[];
}

export interface ProjectProgress {
  projectId: string;
  status: ProjectStatus;
  completedChecklistIds: string[];
  repoUrl: string;
  updatedAt: string;
}

export interface PortfolioProject {
  id: string;
  order: number;
  title: string;
  milestoneLabel: string;
  requiredModulesCompleted: number;
  prerequisiteModuleIds: string[];
  completedPrerequisiteModules: number;
  milestoneUnlocked: boolean;
  techStack: string[];
  businessContext: string;
  packageLayout: string;
  sprints: SprintSpec[];
  reviewCriteria: string[];
  showcaseTips: string[];
  aiReviewPrompts: string[];
  progress: ProjectProgress;
}

export interface ProjectsResponse {
  totalProjects: number;
  completedProjects: number;
  unlockedProjects: number;
  projects: PortfolioProject[];
}
