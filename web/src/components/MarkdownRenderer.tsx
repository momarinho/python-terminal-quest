import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  markdown: string;
}

const CodeBlockWithCopy: React.FC<{ lang?: string; rawCode: string }> = ({ lang, rawCode }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(rawCode);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = rawCode;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    }
  };

  return (
    <div className="relative my-4 group rounded-lg border border-white/[0.07] bg-[#0B0E14] overflow-hidden">
      <div className="flex items-center justify-between px-3 py-1.5 bg-[#121620] border-b border-white/[0.06] text-[10px] font-mono text-slate-400">
        <span className="uppercase tracking-wider">{lang || 'code'}</span>
        <button
          type="button"
          onClick={handleCopy}
          className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-white/[0.05] hover:bg-white/[0.1] text-slate-300 hover:text-[#F5B942] cursor-pointer transition"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-[#2DD4A0]" />
              <span className="text-[#2DD4A0]">Copied</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-[13px] leading-[1.6] text-[#E2E8F0] font-mono">
        <code>{rawCode}</code>
      </pre>
    </div>
  );
};

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ markdown }) => {
  return (
    <div className="space-y-4 font-prose text-[14.5px] leading-relaxed text-[#E2E8F0]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="font-prose text-xl font-bold text-[#F8FAFC] border-b border-white/[0.08] pb-2.5 mt-2 mb-4 tracking-tight">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="font-prose text-base font-semibold text-[#F8FAFC] mt-7 mb-2.5 pl-3 border-l-[3px] border-[#F5B942] tracking-tight">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="font-prose text-sm font-semibold text-[#38BDF8] mt-5 mb-2">
              {children}
            </h3>
          ),
          p: ({ children }) => <p className="text-slate-300 leading-7">{children}</p>,
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noreferrer"
              className="text-[#38BDF8] underline underline-offset-2 hover:text-[#F5B942] transition"
            >
              {children}
            </a>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-outside space-y-1.5 text-slate-300 pl-5">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-outside space-y-1.5 text-slate-300 pl-5">
              {children}
            </ol>
          ),
          li: ({ children }) => <li className="leading-7">{children}</li>,
          hr: () => <hr className="border-t border-white/[0.08] my-6" />,
          blockquote: ({ children }) => (
            <blockquote className="border-l-[3px] border-[#F5B942] bg-[#151923] rounded-r-lg px-4 py-3 text-slate-200 my-4">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="overflow-x-auto my-4 border border-white/[0.08] rounded-lg">
              <table className="w-full text-left border-collapse text-xs">{children}</table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-[#1C2230] text-[#F8FAFC] border-b border-white/[0.08] font-semibold">
              {children}
            </thead>
          ),
          th: ({ children }) => (
            <th className="px-3.5 py-2.5 font-semibold text-[#F5B942]">{children}</th>
          ),
          td: ({ children }) => (
            <td className="px-3.5 py-2.5 border-t border-white/[0.06] text-slate-300">
              {children}
            </td>
          ),
          code: ({ className, children }) => {
            const rawText = String(children).replace(/\n$/, '');
            const isBlock = Boolean(className) || String(children).includes('\n');
            if (isBlock) {
              const langMatch = className?.match(/language-([A-Za-z0-9_-]+)/);
              return <CodeBlockWithCopy lang={langMatch?.[1]} rawCode={rawText} />;
            }
            return (
              <code className="bg-slate-400/[0.14] text-[#BAE6FD] px-1.5 py-[1px] rounded-[4px] text-[13px] font-mono">
                {children}
              </code>
            );
          },
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
};
