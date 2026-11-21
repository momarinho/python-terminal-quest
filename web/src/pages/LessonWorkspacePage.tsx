import React, { useCallback, useEffect, useRef, useState } from 'react';
import Editor, { DiffEditor, type BeforeMount, type OnMount } from '@monaco-editor/react';
import {
  ChevronLeft,
  ChevronRight,
  Eye,
  FileCode2,
  Loader2,
  RotateCcw,
  Save,
  Send,
  StickyNote,
} from 'lucide-react';
import { api } from '../api/client';
import {
  type CompanionMood,
  HeroCompanionFloating,
} from '../components/HeroCompanion';
import { MarkdownRenderer } from '../components/MarkdownRenderer';
import {
  PixelBoltIcon,
  PixelBotIcon,
  PixelCheckIcon,
  PixelCoinIcon,
  PixelCrossIcon,
  PixelCrownIcon,
  PixelFlagIcon,
  PixelPotionIcon,
  PixelPythonIcon,
  PixelScrollIcon,
  PixelSkullIcon,
  PixelSwordIcon,
  PixelTerminalIcon,
  PixelTrophyIcon,
} from '../components/PixelIcons';
import type { Diagnostic, GradeResult, HeroStatus, LessonDetail } from '../types/api';

type CodeEditorInstance = Parameters<OnMount>[0];
type MonacoInstance = Parameters<OnMount>[1];

const MONACO_THEME_NAME = 'pyquest-obsidian';

let monacoThemeDefined = false;

const definePyQuestTheme: BeforeMount = (monaco) => {
  if (monacoThemeDefined) return;
  monaco.editor.defineTheme(MONACO_THEME_NAME, {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: '', foreground: 'F8FAFC', background: '0F131C' },
      { token: 'comment', foreground: '64748B', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'A78BFA', fontStyle: 'bold' },
      { token: 'keyword.control', foreground: 'F45D78', fontStyle: 'bold' },
      { token: 'storage.type', foreground: '38BDF8' },
      { token: 'type', foreground: '38BDF8' },
      { token: 'type.identifier', foreground: '38BDF8' },
      { token: 'string', foreground: '2DD4A0' },
      { token: 'number', foreground: 'F5B942' },
      { token: 'constant', foreground: 'F5B942' },
      { token: 'delimiter', foreground: '94A3B8' },
      { token: 'operator', foreground: 'F5B942' },
    ],
    colors: {
      'editor.background': '#0F131C',
      'editor.foreground': '#F8FAFC',
      'editor.lineHighlightBackground': '#171D2B',
      'editor.lineHighlightBorder': '#1F2739',
      'editorCursor.foreground': '#F5B942',
      'editor.selectionBackground': '#2D3A5988',
      'editor.inactiveSelectionBackground': '#1C223066',
      'editorLineNumber.foreground': '#475569',
      'editorLineNumber.activeForeground': '#F5B942',
      'editorGutter.background': '#0D1017',
      'editorIndentGuide.background': '#1C2230',
      'editorIndentGuide.activeBackground': '#334155',
      'editorWidget.background': '#151923',
      'editorWidget.border': '#293245',
      'editorHoverWidget.background': '#151923',
      'editorHoverWidget.border': '#F5B942',
      'scrollbarSlider.background': '#33415555',
      'scrollbarSlider.hoverBackground': '#47556988',
    },
  });
  monacoThemeDefined = true;
};

interface LessonWorkspacePageProps {
  lessonId: string;
  hero: HeroStatus | null;
  onBackToDashboard: () => void;
  onBackToModule: (moduleId: string) => void;
  onOpenModuleCampfire: (moduleId: string) => void;
  onNavigateLesson: (lessonId: string) => void;
  onProgressUpdated: () => void;
}

interface ChatMessage {
  role: 'user' | 'oracle';
  text: string;
  provider?: string;
  sources?: string[];
}

type SaveState = 'SAVED' | 'UNSAVED' | 'SAVING';

const LEFT_PANE_STORAGE_KEY = 'pyquest.leftPaneWidthPct';
const TERMINAL_HEIGHT_STORAGE_KEY = 'pyquest.terminalHeightPx';

function loadStoredNumber(key: string, fallback: number, min: number, max: number): number {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return fallback;
    const parsed = Number(raw);
    if (Number.isFinite(parsed)) {
      return Math.min(max, Math.max(min, parsed));
    }
  } catch {
    // ignore storage errors
  }
  return fallback;
}

export const LessonWorkspacePage: React.FC<LessonWorkspacePageProps> = ({
  lessonId,
  hero,
  onBackToDashboard,
  onBackToModule,
  onOpenModuleCampfire,
  onNavigateLesson,
  onProgressUpdated,
}) => {
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [files, setFiles] = useState<Record<string, string>>({});
  const [activeFile, setActiveFile] = useState<string>('');
  const [leftTab, setLeftTab] = useState<'concept' | 'hints' | 'oracle' | 'notes'>('concept');
  const [loading, setLoading] = useState<boolean>(true);
  const [runningTests, setRunningTests] = useState<boolean>(false);
  const [saveState, setSaveState] = useState<SaveState>('SAVED');
  const [gradeResult, setGradeResult] = useState<GradeResult | null>(null);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [companionMood, setCompanionMood] = useState<CompanionMood>('idle');

  const [notesText, setNotesText] = useState<string>('');
  const [notesSaveState, setNotesSaveState] = useState<SaveState>('SAVED');
  const [togglingFlag, setTogglingFlag] = useState<boolean>(false);
  const notesTimerRef = useRef<number | null>(null);

  const editorRef = useRef<CodeEditorInstance | null>(null);
  const monacoRef = useRef<MonacoInstance | null>(null);

  const [solutionFiles, setSolutionFiles] = useState<Record<string, string> | null>(null);
  const [showSolutionConfirm, setShowSolutionConfirm] = useState<boolean>(false);
  const [editorMode, setEditorMode] = useState<'CODE' | 'SOLUTION_DIFF' | 'SOLUTION_ONLY'>('CODE');
  const [loadingSolution, setLoadingSolution] = useState<boolean>(false);

  const [leftPanePct, setLeftPanePct] = useState<number>(() =>
    loadStoredNumber(LEFT_PANE_STORAGE_KEY, 42, 24, 66)
  );
  const [terminalHeightPx, setTerminalHeightPx] = useState<number>(() =>
    loadStoredNumber(TERMINAL_HEIGHT_STORAGE_KEY, 250, 130, 520)
  );
  const splitContainerRef = useRef<HTMLDivElement | null>(null);
  const rightPaneRef = useRef<HTMLDivElement | null>(null);

  const [question, setQuestion] = useState<string>('');
  const [askingOracle, setAskingOracle] = useState<boolean>(false);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  const filesRef = useRef<Record<string, string>>({});
  filesRef.current = files;
  const lessonRef = useRef<LessonDetail | null>(null);
  lessonRef.current = lesson;
  const autoSaveTimerRef = useRef<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setGradeResult(null);
    setErrorBanner(null);
    setSolutionFiles(null);
    setShowSolutionConfirm(false);
    setEditorMode('CODE');
    setSaveState('SAVED');
    setNotesSaveState('SAVED');
    setCompanionMood('idle');
    setChatHistory([]);
    if (notesTimerRef.current) {
      window.clearTimeout(notesTimerRef.current);
      notesTimerRef.current = null;
    }
    if (monacoRef.current) {
      for (const model of monacoRef.current.editor.getModels()) {
        monacoRef.current.editor.setModelMarkers(model, 'pyquest-syntax', []);
      }
    }

    api
      .getLesson(lessonId)
      .then((data) => {
        if (cancelled) return;
        setLesson(data);
        setFiles(data.files);
        setNotesText(data.progress.notes ?? '');
        const fileKeys = Object.keys(data.files);
        const preferred =
          fileKeys.find((k) => k === data.entryFile || k.endsWith(data.entryFile)) ??
          fileKeys[0] ??
          '';
        setActiveFile(preferred);
        setLoading(false);
      })
      .catch((err: Error) => {
        if (cancelled) return;
        setErrorBanner(err.message);
        setLoading(false);
      });

    return () => {
      cancelled = true;
      if (autoSaveTimerRef.current) window.clearTimeout(autoSaveTimerRef.current);
      if (notesTimerRef.current) window.clearTimeout(notesTimerRef.current);
    };
  }, [lessonId]);

  const handleSave = useCallback(async () => {
    const currentLesson = lessonRef.current;
    if (!currentLesson) return;
    if (autoSaveTimerRef.current) {
      window.clearTimeout(autoSaveTimerRef.current);
      autoSaveTimerRef.current = null;
    }
    setSaveState('SAVING');
    setErrorBanner(null);
    try {
      await api.saveDraft(currentLesson.id, filesRef.current);
      setSaveState('SAVED');
    } catch (err) {
      setSaveState('UNSAVED');
      setErrorBanner((err as Error).message);
    }
  }, []);

  const handleRunTests = useCallback(async () => {
    const currentLesson = lessonRef.current;
    if (!currentLesson) return;
    if (autoSaveTimerRef.current) {
      window.clearTimeout(autoSaveTimerRef.current);
      autoSaveTimerRef.current = null;
    }
    setRunningTests(true);
    setCompanionMood('running');
    setSaveState('SAVING');
    setErrorBanner(null);
    try {
      const res = await api.runTests(currentLesson.id, filesRef.current);
      setGradeResult(res.result);
      setSaveState('SAVED');
      setCompanionMood(res.result.passed ? 'victory' : 'fail');
      setLesson((prev) => (prev ? { ...prev, progress: res.progress } : prev));
      onProgressUpdated();
    } catch (err) {
      setSaveState('UNSAVED');
      setCompanionMood('fail');
      setErrorBanner((err as Error).message);
    } finally {
      setRunningTests(false);
    }
  }, [onProgressUpdated]);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleRunTests();
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
        e.preventDefault();
        handleSave();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [handleRunTests, handleSave]);

  const syncMonacoDiagnostics = useCallback(
    (
      monaco: MonacoInstance | null,
      currentLesson: LessonDetail | null,
      currentRun: GradeResult | null,
      mode: string
    ) => {
      if (!monaco) return;
      const models = monaco.editor.getModels();
      for (const model of models) {
        monaco.editor.setModelMarkers(model, 'pyquest-syntax', []);
      }
      if (
        mode !== 'CODE' ||
        !currentLesson ||
        !currentRun ||
        currentRun.passed ||
        !currentRun.diagnostics ||
        currentRun.diagnostics.length === 0
      ) {
        return;
      }

      type MonacoModel = ReturnType<MonacoInstance['editor']['getModels']>[number];
      const markersByModel = new Map<
        MonacoModel,
        Parameters<MonacoInstance['editor']['setModelMarkers']>[2]
      >();

      for (const diag of currentRun.diagnostics) {
        const targetModel =
          models.find(
            (m: MonacoModel) =>
              m.uri.path.endsWith(`/${diag.file}`) || m.uri.path.endsWith(`/${activeFile}`)
          ) ?? editorRef.current?.getModel();
        if (!targetModel) continue;

        const maxLine = targetModel.getLineCount();
        const line = Math.min(Math.max(1, diag.line || 1), maxLine);
        const lineLength = targetModel.getLineLength(line);
        const startCol = diag.column && diag.column > 0 ? Math.min(diag.column, lineLength + 1) : 1;
        const endCol = Math.max(startCol + 1, lineLength + 1);

        const existing = markersByModel.get(targetModel) ?? [];
        existing.push({
          severity: monaco.MarkerSeverity.Error,
          message: diag.message,
          startLineNumber: line,
          startColumn: startCol,
          endLineNumber: line,
          endColumn: endCol,
        });
        markersByModel.set(targetModel, existing);
      }

      for (const [model, markers] of markersByModel.entries()) {
        monaco.editor.setModelMarkers(model, 'pyquest-syntax', markers);
      }
    },
    [activeFile]
  );

  useEffect(() => {
    syncMonacoDiagnostics(monacoRef.current, lesson, gradeResult, editorMode);
  }, [lesson, gradeResult, editorMode, activeFile, syncMonacoDiagnostics]);

  const handleEditorMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    syncMonacoDiagnostics(monaco, lessonRef.current, gradeResult, editorMode);
  };

  const handleCodeChange = (value: string | undefined) => {
    const nextValue = value ?? '';
    setFiles((prev) => {
      const updated = { ...prev, [activeFile]: nextValue };
      filesRef.current = updated;
      return updated;
    });
    setSaveState('UNSAVED');

    if (autoSaveTimerRef.current) {
      window.clearTimeout(autoSaveTimerRef.current);
    }
    autoSaveTimerRef.current = window.setTimeout(() => {
      const currentLesson = lessonRef.current;
      if (!currentLesson) return;
      setSaveState('SAVING');
      api
        .saveDraft(currentLesson.id, filesRef.current)
        .then(() => setSaveState('SAVED'))
        .catch(() => setSaveState('UNSAVED'));
    }, 800);
  };

  const handleRevealHint = async () => {
    if (!lesson) return;
    try {
      const res = await api.revealHint(lesson.id);
      setLesson((prev) =>
        prev ? { ...prev, unlockedHints: res.unlockedHints, progress: res.progress } : prev
      );
    } catch (err) {
      setErrorBanner((err as Error).message);
    }
  };

  const handleToggleFlag = async () => {
    if (!lesson || togglingFlag) return;
    setTogglingFlag(true);
    try {
      const updated = await api.toggleFlag(lesson.id, !lesson.progress.flagged);
      setLesson((prev) => (prev ? { ...prev, progress: updated } : prev));
      onProgressUpdated();
    } catch (err) {
      setErrorBanner((err as Error).message);
    } finally {
      setTogglingFlag(false);
    }
  };

  const persistNotes = useCallback(async (targetId: string, content: string) => {
    setNotesSaveState('SAVING');
    try {
      const updated = await api.saveNotes(targetId, content);
      setLesson((prev) =>
        prev && prev.id === targetId ? { ...prev, progress: updated } : prev
      );
      setNotesSaveState('SAVED');
    } catch (err) {
      setNotesSaveState('UNSAVED');
      setErrorBanner((err as Error).message);
    }
  }, []);

  const handleNotesChange = (value: string) => {
    setNotesText(value);
    setNotesSaveState('UNSAVED');
    if (notesTimerRef.current) window.clearTimeout(notesTimerRef.current);
    const currentId = lesson?.id;
    if (!currentId) return;
    notesTimerRef.current = window.setTimeout(() => {
      persistNotes(currentId, value);
    }, 650);
  };

  const handleSaveNotesNow = () => {
    if (!lesson) return;
    if (notesTimerRef.current) {
      window.clearTimeout(notesTimerRef.current);
      notesTimerRef.current = null;
    }
    persistNotes(lesson.id, notesText);
  };

  const handleReset = async () => {
    if (!lesson) return;
    if (!window.confirm('Reset your code in this lesson back to the starter template?')) return;
    try {
      const res = await api.resetLesson(lesson.id);
      setFiles(res.files);
      setGradeResult(null);
      setSaveState('SAVED');
      setEditorMode('CODE');
      setCompanionMood('idle');
    } catch (err) {
      setErrorBanner((err as Error).message);
    }
  };

  const loadAndOpenSolution = async (targetMode: 'SOLUTION_DIFF' | 'SOLUTION_ONLY') => {
    if (!lesson) return;
    setLoadingSolution(true);
    try {
      const sol = solutionFiles ?? (await api.getSolution(lesson.id)).files;
      setSolutionFiles(sol);
      setShowSolutionConfirm(false);
      setEditorMode(targetMode);
    } catch (err) {
      setErrorBanner((err as Error).message);
    } finally {
      setLoadingSolution(false);
    }
  };

  const handleToggleSolution = () => {
    if (!lesson) return;
    if (editorMode !== 'CODE') {
      setEditorMode('CODE');
      return;
    }
    if (solutionFiles) {
      setEditorMode('SOLUTION_DIFF');
      return;
    }
    if (lesson.progress.status === 'COMPLETED') {
      loadAndOpenSolution('SOLUTION_DIFF');
    } else {
      setShowSolutionConfirm(true);
    }
  };

  const jumpToDiagnostic = (diag: Diagnostic) => {
    setEditorMode('CODE');
    const matchingKey = Object.keys(files).find(
      (k) => k === diag.file || k.endsWith(diag.file)
    );
    if (matchingKey) setActiveFile(matchingKey);

    window.setTimeout(() => {
      const ed = editorRef.current;
      if (!ed) return;
      const line = Math.max(1, diag.line || 1);
      const col = Math.max(1, diag.column || 1);
      ed.revealLineInCenter(line);
      ed.setPosition({ lineNumber: line, column: col });
      ed.focus();
    }, 40);
  };

  const handleAskOracle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!lesson || !question.trim()) return;
    const userQ = question.trim();
    setQuestion('');
    setChatHistory((prev) => [...prev, { role: 'user', text: userQ }]);
    setAskingOracle(true);
    try {
      const diagSummary = gradeResult?.summary ?? lesson.progress.lastDiagnostics ?? '';
      const res = await api.askOracle(lesson.id, userQ, files, diagSummary);
      setChatHistory((prev) => [
        ...prev,
        {
          role: 'oracle',
          text: res.answer,
          provider: res.provider,
          sources: res.citedSources,
        },
      ]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: 'oracle', text: `Oracle error: ${(err as Error).message}`, provider: 'error' },
      ]);
    } finally {
      setAskingOracle(false);
    }
  };

  const startHorizontalResize = (e: React.MouseEvent) => {
    e.preventDefault();
    const container = splitContainerRef.current;
    if (!container) return;
    const onMove = (ev: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      if (rect.width <= 0) return;
      const pct = Math.min(66, Math.max(24, ((ev.clientX - rect.left) / rect.width) * 100));
      setLeftPanePct(pct);
      try {
        localStorage.setItem(LEFT_PANE_STORAGE_KEY, String(Math.round(pct)));
      } catch {
        // ignore
      }
    };
    const onUp = () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  };

  const startVerticalResize = (e: React.MouseEvent) => {
    e.preventDefault();
    const rightPane = rightPaneRef.current;
    if (!rightPane) return;
    const onMove = (ev: MouseEvent) => {
      const rect = rightPane.getBoundingClientRect();
      const nextHeight = Math.min(520, Math.max(130, rect.bottom - ev.clientY));
      setTerminalHeightPx(nextHeight);
      try {
        localStorage.setItem(TERMINAL_HEIGHT_STORAGE_KEY, String(Math.round(nextHeight)));
      } catch {
        // ignore
      }
    };
    const onUp = () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  };

  if (loading || !lesson) {
    return (
      <div className="min-h-screen bg-[#0D1017] text-[#F8FAFC] flex items-center justify-center gap-3">
        {errorBanner ? (
          <div className="text-[#F45D78] text-sm font-medium">{errorBanner}</div>
        ) : (
          <>
            <Loader2 className="w-5 h-5 animate-spin text-[#F5B942]" />
            <span className="text-sm font-medium text-slate-300">Loading stage #{lessonId}...</span>
          </>
        )}
      </div>
    );
  }

  const fileList = Object.keys(files);
  const isBossLesson = lesson.kind === 'BOSS';
  const isWebLesson = lesson.runtime === 'WEB_INTEGRATION';
  const isCleared = lesson.progress.status === 'COMPLETED';
  const isFlagged = lesson.progress.flagged;

  return (
    <div className="h-screen flex flex-col bg-[#0D1017] text-[#F8FAFC] overflow-hidden">
      {/* Slim Workspace Header with Ghost Secondary Actions */}
      <header className="h-14 shrink-0 border-b border-white/[0.08] bg-[#0D1017] px-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2 min-w-0">
          <button
            type="button"
            onClick={onBackToDashboard}
            className="hidden sm:inline-flex items-center px-2.5 py-1.5 rounded-md text-xs font-medium text-slate-400 hover:text-white hover:bg-[#1C2230] cursor-pointer shrink-0 transition"
          >
            World Map
          </button>

          <button
            type="button"
            onClick={() => onBackToModule(lesson.moduleId)}
            className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs font-medium text-slate-200 hover:text-[#F5B942] hover:bg-[#1C2230] cursor-pointer shrink-0 transition"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            <span>Realm</span>
          </button>

          <div className="h-4 w-px bg-white/[0.1] hidden sm:block shrink-0" />

          <div className="flex items-center gap-2.5 min-w-0">
            <span
              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold shrink-0 ${
                isBossLesson
                  ? 'bg-[#F45D78]/15 text-[#F45D78]'
                  : 'bg-[#38BDF8]/12 text-[#38BDF8]'
              }`}
            >
              {isBossLesson ? (
                isCleared ? (
                  <PixelCrownIcon className="w-3 h-3" />
                ) : (
                  <PixelSkullIcon className="w-3 h-3" />
                )
              ) : isWebLesson ? (
                <PixelBoltIcon className="w-3 h-3" />
              ) : (
                <PixelPythonIcon className="w-3 h-3" />
              )}
              <span>{isBossLesson ? `Boss #${lesson.id}` : `#${lesson.id}`}</span>
            </span>

            <span className="font-semibold text-sm text-[#F8FAFC] truncate">{lesson.title}</span>

            {isCleared && (
              <span className="hidden md:inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#2DD4A0]/15 text-[#2DD4A0] text-[11px] font-medium shrink-0">
                <PixelCheckIcon className="w-3 h-3" />
                <span>Cleared</span>
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          <div className="hidden md:flex items-center mr-1">
            <button
              type="button"
              disabled={!lesson.prevLessonId}
              onClick={() => lesson.prevLessonId && onNavigateLesson(lesson.prevLessonId)}
              title="Previous stage"
              className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-[#1C2230] disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed transition"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              type="button"
              disabled={!lesson.nextLessonId}
              onClick={() => lesson.nextLessonId && onNavigateLesson(lesson.nextLessonId)}
              title="Next stage"
              className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-[#1C2230] disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed transition"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Clean Ghost Buttons */}
          <button
            type="button"
            onClick={handleToggleFlag}
            disabled={togglingFlag}
            title="Flag this stage for later review"
            className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium cursor-pointer transition ${
              isFlagged
                ? 'bg-[#F45D78]/15 text-[#F45D78]'
                : 'text-slate-300 hover:text-white hover:bg-[#1C2230]'
            }`}
          >
            <PixelFlagIcon className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">{isFlagged ? 'Flagged' : 'Flag'}</span>
          </button>

          <button
            type="button"
            onClick={handleToggleSolution}
            disabled={loadingSolution}
            title="Compare or inspect reference solution"
            className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium cursor-pointer transition ${
              editorMode !== 'CODE'
                ? 'bg-[#F5B942]/15 text-[#F5B942]'
                : 'text-slate-300 hover:text-white hover:bg-[#1C2230]'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">
              {editorMode !== 'CODE' ? 'Back to Code' : 'Solution'}
            </span>
          </button>

          <button
            type="button"
            onClick={handleReset}
            title="Reset starter files"
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-300 hover:text-white hover:bg-[#1C2230] text-xs font-medium cursor-pointer transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">Reset</span>
          </button>

          <button
            type="button"
            onClick={handleSave}
            title="Save draft (Ctrl+S)"
            className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-300 hover:text-white hover:bg-[#1C2230] text-xs font-medium cursor-pointer transition"
          >
            <Save className="w-3.5 h-3.5" />
            <span className="hidden xl:inline">Save</span>
          </button>

          <button
            type="button"
            onClick={handleRunTests}
            disabled={runningTests}
            className="ml-1 inline-flex items-center gap-1.5 px-4 py-1.5 disabled:opacity-50 text-xs font-semibold cursor-pointer rpg-btn-emerald"
          >
            {runningTests ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <PixelSwordIcon className="w-3.5 h-3.5" />
            )}
            <span>{runningTests ? 'Grading...' : 'Run & Grade'}</span>
          </button>
        </div>
      </header>

      {/* Reference Solution Confirmation Modal */}
      {showSolutionConfirm && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-[2px] flex items-center justify-center p-4">
          <div className="rpg-panel-gold max-w-md w-full p-6 space-y-4">
            <div className="flex items-center gap-2.5 text-[#F5B942] text-sm font-semibold">
              <PixelPotionIcon className="w-4 h-4" />
              <span>Reveal Reference Solution?</span>
            </div>
            <p className="text-sm text-slate-300 leading-relaxed">
              You haven&apos;t cleared Stage <strong className="text-[#F5B942]">#{lesson.id}</strong>{' '}
              yet ({lesson.unlockedHints.length}/{lesson.totalHints} progressive hints unlocked). Try
              unlocking hints first before inspecting the reference solution.
            </p>
            <div className="flex items-center justify-end gap-2.5 pt-2">
              <button
                type="button"
                onClick={() => {
                  setShowSolutionConfirm(false);
                  setLeftTab('hints');
                }}
                className="px-3.5 py-2 rounded-md text-slate-300 hover:text-white hover:bg-[#1C2230] text-xs font-medium cursor-pointer transition"
              >
                Try Hints First
              </button>
              <button
                type="button"
                onClick={() => loadAndOpenSolution('SOLUTION_DIFF')}
                className="px-3.5 py-2 text-xs font-semibold cursor-pointer rpg-btn-gold"
              >
                Reveal Solution
              </button>
            </div>
          </div>
        </div>
      )}

      {errorBanner && (
        <div className="bg-[#2B131B] border-b border-[#F45D78]/40 px-4 py-2 text-xs text-[#FDA4AF] flex items-center justify-between">
          <span>Error: {errorBanner}</span>
          <button
            type="button"
            onClick={() => setErrorBanner(null)}
            className="text-[#F45D78] hover:text-white cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Resizable Split-Screen Workspace */}
      <div ref={splitContainerRef} className="flex-1 flex flex-col lg:flex-row min-h-0">
        {/* LEFT PANE */}
        <div
          style={{ '--left-pane-w': `${leftPanePct}%` } as React.CSSProperties}
          className="w-full lg:w-[var(--left-pane-w)] shrink-0 flex flex-col min-h-0 bg-[#0D1017]"
        >
          <div className="h-11 shrink-0 border-b border-white/[0.08] bg-[#121620] px-3 flex items-center gap-1 overflow-x-auto whitespace-nowrap">
            <button
              type="button"
              onClick={() => setLeftTab('concept')}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer shrink-0 transition ${
                leftTab === 'concept'
                  ? 'bg-[#1C2230] text-[#F5B942]'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <PixelScrollIcon className="w-3.5 h-3.5" />
              <span>Concept</span>
            </button>

            <button
              type="button"
              onClick={() => setLeftTab('hints')}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer shrink-0 transition ${
                leftTab === 'hints'
                  ? 'bg-[#1C2230] text-[#F5B942]'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <PixelPotionIcon className="w-3.5 h-3.5" />
              <span>
                Hints ({lesson.unlockedHints.length}/{lesson.totalHints})
              </span>
            </button>

            <button
              type="button"
              onClick={() => setLeftTab('notes')}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer shrink-0 transition ${
                leftTab === 'notes'
                  ? 'bg-[#1C2230] text-[#38BDF8]'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <StickyNote className="w-3.5 h-3.5 text-[#38BDF8]" />
              <span>Notes</span>
              {notesText.trim().length > 0 && (
                <span className="w-1.5 h-1.5 rounded-full bg-[#38BDF8] inline-block" aria-hidden="true" />
              )}
            </button>

            <button
              type="button"
              onClick={() => setLeftTab('oracle')}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[13px] font-medium cursor-pointer shrink-0 transition ${
                leftTab === 'oracle'
                  ? 'bg-[#1C2230] text-[#A78BFA]'
                  : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
              }`}
            >
              <PixelBotIcon className="w-3.5 h-3.5" />
              <span>Oracle</span>
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-6 bg-[#0D1017]">
            {leftTab === 'concept' && (
              <div className="space-y-6">
                <div className="rpg-panel p-4 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-xs font-semibold text-slate-400">
                      {lesson.moduleTitle}
                    </span>
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#F5B942]">
                      <PixelCoinIcon className="w-3.5 h-3.5" />
                      <span>+{lesson.xp} XP</span>
                    </span>
                  </div>

                  <p className="text-sm text-[#F8FAFC] leading-relaxed">
                    <span className="text-[#2DD4A0] font-semibold mr-1.5">Objective:</span>
                    {lesson.objective}
                  </p>

                  <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300">
                      {isWebLesson ? (
                        <PixelBoltIcon className="w-3 h-3" />
                      ) : (
                        <PixelPythonIcon className="w-3 h-3" />
                      )}
                      <span>{isWebLesson ? 'Web & AI' : 'Python 3.13'}</span>
                    </span>
                    <span className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-slate-300">
                      {lesson.mode}
                    </span>
                    {lesson.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 rounded-md text-[11px] bg-white/[0.05] text-[#BAE6FD]"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                <MarkdownRenderer markdown={lesson.conceptMarkdown} />
              </div>
            )}

            {leftTab === 'hints' && (
              <div className="space-y-4">
                <div className="rpg-panel p-4 flex items-center justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-semibold text-[#F5B942]">Progressive Hints</h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Reveal tactical clues one level at a time before inspecting the solution.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={handleRevealHint}
                    disabled={lesson.unlockedHints.length >= lesson.totalHints}
                    className="px-3.5 py-2 disabled:opacity-40 text-xs font-semibold cursor-pointer shrink-0 rpg-btn-gold"
                  >
                    {lesson.unlockedHints.length >= lesson.totalHints
                      ? 'All Unlocked'
                      : `Unlock Hint #${lesson.unlockedHints.length + 1}`}
                  </button>
                </div>

                {lesson.unlockedHints.length === 0 ? (
                  <div className="text-center py-12 border border-dashed border-white/[0.1] rounded-lg text-xs text-slate-400">
                    No hints unlocked yet. Click &quot;Unlock Hint #1&quot; above if you get stuck.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {lesson.unlockedHints.map((hint, idx) => (
                      <div key={idx} className="rpg-panel-gold p-4 space-y-2">
                        <div className="text-xs font-semibold text-[#F5B942]">Hint #{idx + 1}</div>
                        <MarkdownRenderer markdown={hint} />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {leftTab === 'notes' && (
              <div className="h-full flex flex-col gap-3">
                <div className="rpg-panel p-4 flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-semibold text-[#38BDF8]">Personal Study Notes</h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Capture mental models, Python edge cases, or LinkedIn bullets (saved in SQLite).
                    </p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                        notesSaveState === 'SAVED'
                          ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]'
                          : notesSaveState === 'SAVING'
                            ? 'bg-[#F5B942]/15 text-[#F5B942]'
                            : 'bg-white/[0.06] text-slate-300'
                      }`}
                    >
                      {notesSaveState === 'SAVED'
                        ? 'Saved'
                        : notesSaveState === 'SAVING'
                          ? 'Saving...'
                          : 'Unsaved'}
                    </span>
                    <button
                      type="button"
                      onClick={handleSaveNotesNow}
                      disabled={notesSaveState === 'SAVING'}
                      className="px-2.5 py-1 rounded-md text-slate-300 hover:text-white hover:bg-[#1C2230] text-xs font-medium cursor-pointer transition"
                    >
                      Save
                    </button>
                  </div>
                </div>

                <textarea
                  value={notesText}
                  onChange={(e) => handleNotesChange(e.target.value)}
                  placeholder="Jot down takeaways, edge cases, or LinkedIn snippet drafts for this stage..."
                  className="flex-1 min-h-[260px] w-full bg-[#0B0E14] border border-white/[0.08] focus:border-[#F5B942]/60 rounded-lg p-4 text-sm text-[#F8FAFC] placeholder-slate-500 leading-relaxed resize-none focus:outline-none"
                />
              </div>
            )}

            {leftTab === 'oracle' && (
              <div className="h-full flex flex-col justify-between gap-4">
                <div className="space-y-3 overflow-y-auto pr-1">
                  <div className="rpg-panel p-4 text-xs text-slate-300 space-y-1.5">
                    <div className="text-xs font-semibold text-[#A78BFA] flex items-center gap-2">
                      <PixelBotIcon className="w-4 h-4" />
                      <span>RAG Oracle</span>
                    </div>
                    <p className="text-slate-400 leading-relaxed">
                      Ask about your code or pytest diagnostics. Active files,{' '}
                      <code className="bg-slate-400/[0.14] text-[#BAE6FD] px-1 rounded">
                        concept.md
                      </code>
                      , and the latest test summary are sent automatically.
                    </p>
                  </div>

                  {chatHistory.map((msg, i) => (
                    <div
                      key={i}
                      className={`p-4 text-xs space-y-2 rounded-lg border ${
                        msg.role === 'user'
                          ? 'bg-[#1C2230] border-[#F5B942]/35 text-[#FDE68A] ml-6'
                          : 'bg-[#151923] border-white/[0.08] text-[#F8FAFC] mr-2'
                      }`}
                    >
                      <div className="text-[11px] font-semibold text-slate-400">
                        {msg.role === 'user' ? 'You' : `Oracle (${msg.provider ?? 'rag'})`}
                      </div>
                      <MarkdownRenderer markdown={msg.text} />
                      {msg.sources && msg.sources.length > 0 && (
                        <div className="pt-2 border-t border-white/[0.06] text-[11px] font-mono text-slate-400">
                          Sources: {msg.sources.join(', ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <form
                  onSubmit={handleAskOracle}
                  className="flex gap-2 pt-3 border-t border-white/[0.08]"
                >
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask the Oracle about your Python code or error..."
                    className="flex-1 bg-[#0B0E14] border border-white/[0.08] rounded-md px-3 py-2 text-xs text-[#F8FAFC] placeholder-slate-500 focus:outline-none focus:border-[#F5B942]/60"
                  />
                  <button
                    type="submit"
                    disabled={askingOracle || !question.trim()}
                    className="px-3.5 py-2 disabled:opacity-40 text-xs font-semibold inline-flex items-center gap-1.5 cursor-pointer rpg-btn-gold"
                  >
                    {askingOracle ? (
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Send className="w-3.5 h-3.5" />
                    )}
                    <span>Ask</span>
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>

        {/* Horizontal Draggable Divider */}
        <div
          onMouseDown={startHorizontalResize}
          title="Drag to resize left/right split"
          className="hidden lg:flex w-1.5 shrink-0 bg-[#121620] hover:bg-[#F5B942]/40 border-x border-white/[0.06] cursor-col-resize items-center justify-center transition select-none"
        />

        {/* RIGHT PANE: Obsidian Monaco Editor + Battle Log */}
        <div ref={rightPaneRef} className="flex-1 flex flex-col min-h-0 min-w-0 bg-[#0F131C]">
          <div className="h-11 shrink-0 border-b border-white/[0.08] bg-[#121620] px-3 flex items-center justify-between gap-2 overflow-x-auto">
            <div className="flex items-center gap-1.5">
              {fileList.map((filePath) => {
                const simpleName = filePath.split('/').pop() ?? filePath;
                const isSelected = filePath === activeFile;
                return (
                  <button
                    key={filePath}
                    type="button"
                    onClick={() => setActiveFile(filePath)}
                    title={filePath}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-mono cursor-pointer transition ${
                      isSelected
                        ? 'bg-[#1C2230] text-[#F5B942] border border-white/[0.08]'
                        : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
                    }`}
                  >
                    <FileCode2 className="w-3.5 h-3.5 text-[#F5B942]" />
                    <span>{simpleName}</span>
                  </button>
                );
              })}
            </div>

            <div className="flex items-center gap-2 shrink-0">
              {editorMode !== 'CODE' && (
                <div className="inline-flex rounded-md border border-white/[0.08] bg-[#0D1017] p-0.5 text-xs font-medium">
                  <button
                    type="button"
                    onClick={() => setEditorMode('SOLUTION_DIFF')}
                    className={`px-2 py-0.5 rounded cursor-pointer transition ${
                      editorMode === 'SOLUTION_DIFF'
                        ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                        : 'text-slate-300'
                    }`}
                  >
                    Diff
                  </button>
                  <button
                    type="button"
                    onClick={() => setEditorMode('SOLUTION_ONLY')}
                    className={`px-2 py-0.5 rounded cursor-pointer transition ${
                      editorMode === 'SOLUTION_ONLY'
                        ? 'bg-[#F5B942] text-[#0D1017] font-semibold'
                        : 'text-slate-300'
                    }`}
                  >
                    Solution
                  </button>
                </div>
              )}

              <span
                className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                  saveState === 'SAVED'
                    ? 'text-[#2DD4A0]'
                    : saveState === 'SAVING'
                      ? 'text-[#F5B942]'
                      : 'text-slate-400'
                }`}
              >
                {saveState === 'SAVED'
                  ? 'Saved'
                  : saveState === 'SAVING'
                    ? 'Saving...'
                    : 'Unsaved'}
              </span>
              <span className="hidden xl:inline text-[11px] font-mono text-slate-500">
                Ctrl+Enter to run
              </span>
            </div>
          </div>

          <div className="flex-1 min-h-[160px] relative">
            {editorMode === 'CODE' && (
              <Editor
                height="100%"
                language="python"
                theme={MONACO_THEME_NAME}
                beforeMount={definePyQuestTheme}
                path={`inmemory://workspace/${lesson.id}/${activeFile}`}
                value={files[activeFile] ?? ''}
                keepCurrentModel={true}
                onMount={handleEditorMount}
                onChange={handleCodeChange}
                options={{
                  fontSize: 13,
                  lineHeight: 21,
                  fontFamily: '"JetBrains Mono", monospace',
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  tabSize: 4,
                  insertSpaces: true,
                  padding: { top: 14, bottom: 14 },
                }}
              />
            )}

            {editorMode === 'SOLUTION_DIFF' && solutionFiles && (
              <DiffEditor
                height="100%"
                language="python"
                theme={MONACO_THEME_NAME}
                beforeMount={definePyQuestTheme}
                original={files[activeFile] ?? ''}
                modified={solutionFiles[activeFile] ?? ''}
                originalModelPath={`inmemory://diff-orig/${lesson.id}/${activeFile}`}
                modifiedModelPath={`inmemory://diff-sol/${lesson.id}/${activeFile}`}
                keepCurrentOriginalModel={true}
                keepCurrentModifiedModel={true}
                options={{
                  readOnly: true,
                  renderSideBySide: true,
                  fontSize: 13,
                  fontFamily: '"JetBrains Mono", monospace',
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                }}
              />
            )}

            {editorMode === 'SOLUTION_ONLY' && solutionFiles && (
              <Editor
                height="100%"
                language="python"
                theme={MONACO_THEME_NAME}
                beforeMount={definePyQuestTheme}
                path={`inmemory://solution-only/${lesson.id}/${activeFile}`}
                value={solutionFiles[activeFile] ?? ''}
                keepCurrentModel={true}
                options={{
                  readOnly: true,
                  fontSize: 13,
                  lineHeight: 21,
                  fontFamily: '"JetBrains Mono", monospace',
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  padding: { top: 14, bottom: 14 },
                }}
              />
            )}
          </div>

          <div
            onMouseDown={startVerticalResize}
            title="Drag to resize editor / battle log"
            className="h-1.5 shrink-0 bg-[#121620] hover:bg-[#F5B942]/40 border-y border-white/[0.06] cursor-row-resize flex items-center justify-center transition select-none"
          />

          {/* Battle Log (JetBrains Mono 13px) */}
          <div
            style={{ height: `${terminalHeightPx}px` }}
            className="shrink-0 bg-[#0B0E14] flex flex-col"
          >
            <div className="h-10 shrink-0 px-4 bg-[#121620] border-b border-white/[0.08] flex items-center justify-between text-xs">
              <div className="flex items-center gap-2 font-mono text-[13px] text-slate-300">
                <PixelTerminalIcon className="w-4 h-4" />
                <span>Battle Log — Python 3.13 + pytest (isolated temp workspace)</span>
              </div>

              {gradeResult && (
                <span
                  className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md font-mono text-xs font-medium ${
                    gradeResult.passed
                      ? 'bg-[#2DD4A0]/15 text-[#2DD4A0]'
                      : 'bg-[#F45D78]/15 text-[#F45D78]'
                  }`}
                >
                  {gradeResult.passed ? (
                    <PixelCheckIcon className="w-3 h-3" />
                  ) : (
                    <PixelCrossIcon className="w-3 h-3" />
                  )}
                  <span>
                    {gradeResult.stage} — {gradeResult.summary}
                  </span>
                </span>
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-4 font-mono text-[13px] leading-[1.6] space-y-3">
              {!gradeResult && !runningTests && (
                <div className="text-slate-400">
                  Ready. Press <strong className="text-[#F5B942]">Ctrl+Enter</strong> or click{' '}
                  <strong className="text-[#2DD4A0]">Run &amp; Grade</strong> to execute the
                  verification suite.
                </div>
              )}

              {runningTests && (
                <div className="flex items-center gap-2 text-[#F5B942]">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Running isolated pytest verification suite...</span>
                </div>
              )}

              {gradeResult && (
                <>
                  {gradeResult.passed && (
                    <div
                      className={`p-4 rounded-lg border flex flex-wrap items-center justify-between gap-3 font-sans ${
                        isBossLesson
                          ? 'bg-[#21131C] border-[#F5B942]/45'
                          : 'bg-[#102620] border-[#2DD4A0]/45'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-[#0D1017] border border-[#F5B942]/40">
                          {isBossLesson ? (
                            <PixelCrownIcon className="w-5 h-5" />
                          ) : (
                            <PixelTrophyIcon className="w-5 h-5" />
                          )}
                        </div>
                        <div>
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-sm font-semibold text-[#F8FAFC]">
                              {isBossLesson ? 'Boss Defeated!' : 'Stage Cleared!'}
                            </span>
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-[#F5B942]/15 text-xs font-semibold text-[#F5B942]">
                              <PixelCoinIcon className="w-3 h-3" />
                              <span>+{lesson.xp} XP</span>
                            </span>
                          </div>
                          <div className="text-xs text-slate-300 mt-0.5">
                            {isBossLesson
                              ? 'Realm boss defeated — visit the Campfire to review prompts & share your build.'
                              : 'All pytest verification checks passed cleanly.'}
                          </div>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() => {
                          if (isBossLesson) {
                            onOpenModuleCampfire(lesson.moduleId);
                          } else if (lesson.nextLessonId) {
                            onNavigateLesson(lesson.nextLessonId);
                          } else {
                            onBackToModule(lesson.moduleId);
                          }
                        }}
                        className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold cursor-pointer rpg-btn-gold shrink-0"
                      >
                        <span>
                          {isBossLesson
                            ? 'Next Stage: Campfire →'
                            : lesson.nextLessonId
                              ? 'Next Stage →'
                              : 'Realm Overview →'}
                        </span>
                      </button>
                    </div>
                  )}

                  {gradeResult.diagnostics && gradeResult.diagnostics.length > 0 && (
                    <div className="space-y-1.5">
                      <div className="text-xs font-sans font-semibold text-[#F45D78]">
                        Syntax Diagnostics ({gradeResult.diagnostics.length}) — Click to jump
                      </div>
                      <div className="space-y-1.5">
                        {gradeResult.diagnostics.map((diag, idx) => (
                          <button
                            key={idx}
                            type="button"
                            onClick={() => jumpToDiagnostic(diag)}
                            className="w-full text-left p-3 rounded-lg bg-[#231219] hover:bg-[#2E1721] border border-[#F45D78]/35 text-[13px] text-[#FECDD3] cursor-pointer transition flex items-start justify-between gap-3"
                          >
                            <div className="space-y-0.5 min-w-0">
                              <div className="font-semibold text-[#FDA4AF]">
                                {diag.file}:{diag.line}
                                {diag.column ? `:${diag.column}` : ''} [{diag.severity}]
                              </div>
                              <div className="text-slate-200 whitespace-pre-wrap break-words">
                                {diag.message}
                              </div>
                            </div>
                            <span className="font-sans text-xs font-medium text-[#F5B942] shrink-0">
                              Jump →
                            </span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {gradeResult.testCases.length > 0 && (
                    <div className="space-y-2">
                      {gradeResult.testCases.map((tc, idx) => (
                        <div
                          key={idx}
                          className={`p-3 rounded-lg border ${
                            tc.passed
                              ? 'bg-[#0F241F] border-[#2DD4A0]/30 text-[#A7F3D0]'
                              : 'bg-[#231219] border-[#F45D78]/35 text-[#FECDD3]'
                          }`}
                        >
                          <div className="flex items-center gap-2 font-medium">
                            {tc.passed ? (
                              <PixelCheckIcon className="w-3.5 h-3.5 shrink-0" />
                            ) : (
                              <PixelCrossIcon className="w-3.5 h-3.5 shrink-0" />
                            )}
                            <span>{tc.name}</span>
                          </div>
                          {!tc.passed && tc.message && (
                            <pre className="mt-1.5 text-[13px] leading-[1.6] text-[#FDA4AF] whitespace-pre-wrap pl-5">
                              {tc.message}
                            </pre>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {gradeResult.stderr && (
                    <div className="space-y-1">
                      <div className="text-xs font-sans font-semibold text-[#F45D78]">
                        Execution / Stderr Summary
                      </div>
                      <pre className="bg-[#231219] border border-[#F45D78]/30 rounded-lg p-3.5 text-[#FECDD3] whitespace-pre-wrap">
                        {gradeResult.stderr}
                      </pre>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Collapsible Floating 5-Tier Hero Companion */}
      <HeroCompanionFloating
        tier={hero?.tier ?? 1}
        tierTitle={hero?.title ?? 'Apprentice'}
        mood={companionMood}
        onJumpHints={() => setLeftTab('hints')}
        onJumpOracle={() => setLeftTab('oracle')}
      />
    </div>
  );
};
