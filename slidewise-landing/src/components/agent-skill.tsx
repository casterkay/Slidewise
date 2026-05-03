const agentFeatures = [
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="4 17 10 11 4 5" /><line x1="12" y1="19" x2="20" y2="19" />
      </svg>
    ),
    title: "Terminal-native",
    description: "No browser tabs, no app switching. Slides generated right where you code.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
      </svg>
    ),
    title: "Your style, your rules",
    description: "Define custom CSS, preferred themes, and slide layouts. The skill remembers.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="23 4 23 10 17 10" /><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
      </svg>
    ),
    title: "Iterative by design",
    description: "Refine slides conversationally. Split, merge, restyle, or regenerate individual slides.",
  },
];

export function AgentSkill() {
  return (
    <section className="py-24 bg-gradient-to-br from-[#111827] to-[#1E293B] text-white">
      <div className="max-w-[1120px] mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          {/* Left */}
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.08em] text-white/50 mb-3">
              Agent Skill
            </div>
            <h2 className="text-3xl font-bold tracking-tight mb-4 text-white">
              Works where you work.
            </h2>
            <p className="text-base text-white/60 max-w-[600px] mb-8">
              Slidewise ships as a SKILL.md for Claude Code. Install it once,
              then generate and customize slide decks through natural
              conversation in your terminal.
            </p>

            <div className="flex flex-col gap-6">
              {agentFeatures.map((af) => (
                <div key={af.title} className="flex gap-4">
                  <div className="w-10 h-10 rounded-lg bg-white/6 flex items-center justify-center shrink-0">
                    {af.icon}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-white mb-0.5">
                      {af.title}
                    </h4>
                    <p className="text-sm text-white/50 leading-relaxed">
                      {af.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right — Terminal */}
          <div className="bg-black/30 border border-white/8 rounded-xl overflow-hidden">
            <div className="flex items-center gap-2 px-3 py-2 bg-white/4 border-b border-white/6">
              <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#28C840]" />
              <span className="text-xs font-mono text-white/40 ml-1">
                claude
              </span>
            </div>
            <div className="p-4 font-mono text-xs leading-[1.8] text-white/60">
              <span className="text-primary">&gt;</span>{" "}
              <span className="text-white/90">
                turn this youtube video into slides
              </span>
              <br />
              <span className="text-white/30">
                &nbsp;&nbsp;https://youtu.be/dQw4w9W...
              </span>
              <br />
              <br />
              <span className="text-success">Calling Slidewise API...</span>
              <br />
              <span className="text-white/30">
                &nbsp;&nbsp;Extracted 12 segments, 3 code blocks
              </span>
              <br />
              <span className="text-white/30">
                &nbsp;&nbsp;Planned 9 slides
              </span>
              <br />
              <br />
              <span className="text-success">Wrote slides.html</span>{" "}
              <span className="text-white/30">(self-contained)</span>
              <br />
              <br />
              <span className="text-primary">&gt;</span>{" "}
              <span className="text-white/90">
                use the dracula theme and split slide 4
              </span>
              <br />
              <br />
              <span className="text-success">Updated theme to dracula</span>
              <br />
              <span className="text-success">
                Split slide 4 into 4a and 4b
              </span>
              <br />
              <span className="text-success">Wrote slides.html</span>{" "}
              <span className="text-white/30">(10 slides)</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
