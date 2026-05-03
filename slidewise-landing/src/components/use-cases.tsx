const useCases = [
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
    iconBg: "bg-secondary-light",
    title: "Tutorials & Courses",
    description: "Transform technical walkthroughs into structured slide decks with code blocks, diagrams, and speaker notes preserved.",
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    iconBg: "bg-primary-light",
    title: "Meeting Recordings",
    description: "Distill hour-long meetings into concise recap decks. Key decisions, action items, and discussion points on clear slides.",
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M19 16V6a2 2 0 0 0-2-2H2" /><path d="M22 20H7a2 2 0 0 1-2-2V9" /><path d="m9 13 3 3 3-3" />
      </svg>
    ),
    iconBg: "bg-success/8",
    title: "Podcasts & Talks",
    description: "Convert conference talks and podcast episodes into shareable visual summaries your audience can skim in minutes.",
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" ry="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" />
      </svg>
    ),
    iconBg: "bg-warning/8",
    title: "Screen Recordings",
    description: "Turn demo recordings and product walkthroughs into step-by-step visual guides with extracted keyframes.",
  },
];

export function UseCases() {
  return (
    <section id="use-cases" className="py-24">
      <div className="max-w-[1120px] mx-auto px-6">
        <div className="text-xs font-semibold uppercase tracking-[0.08em] text-primary mb-3">
          Use cases
        </div>
        <h2 className="text-3xl font-bold tracking-tight mb-4">
          Any video. Any context.
        </h2>
        <p className="text-base text-text-secondary max-w-[520px] mb-12">
          If it was worth recording, it&apos;s worth turning into slides your
          team can reference, share, and present.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {useCases.map((uc) => (
            <div
              key={uc.title}
              className="bg-surface border border-border rounded-2xl p-8 transition-all duration-200 hover:border-border-strong hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)]"
            >
              <div className={`w-11 h-11 rounded-xl flex items-center justify-center mb-4 ${uc.iconBg}`}>
                {uc.icon}
              </div>
              <h3 className="text-base font-semibold mb-2">{uc.title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed">
                {uc.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
