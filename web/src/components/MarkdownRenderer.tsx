import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  markdown: string;
}

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
          code: ({ className, children }) => {
            const isBlock = Boolean(className) || String(children).includes('\n');
            if (isBlock) {
              const langMatch = className?.match(/language-([A-Za-z0-9_-]+)/);
              const lang = langMatch?.[1];
              return (
                <div className="relative my-4">
                  {lang && (
                    <span className="absolute top-2 right-3 text-[10px] font-mono uppercase tracking-wider text-slate-500 select-none">
                      {lang}
                    </span>
                  )}
                  <pre className="bg-[#0B0E14] border border-white/[0.07] rounded-lg p-4 overflow-x-auto text-[13px] leading-[1.6] text-[#E2E8F0] font-mono">
                    <code>{children}</code>
                  </pre>
                </div>
              );
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
