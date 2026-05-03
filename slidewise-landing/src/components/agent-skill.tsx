import { RotateCcw, Terminal, Wand2 } from "lucide-react";

const agentFeatures = [
  {
    icon: <Terminal size={18} className="text-blue-500" strokeWidth={2} />,
    title: "Terminal-native",
    description: "No browser tabs, no app switching. Slides generated right where you code.",
  },
  {
    icon: <Wand2 size={18} className="text-purple-500" strokeWidth={2} />,
    title: "Your style, your rules",
    description: "Define custom CSS, preferred themes, and slide layouts. The skill remembers.",
  },
  {
    icon: <RotateCcw size={18} className="text-green-600" strokeWidth={2} />,
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
