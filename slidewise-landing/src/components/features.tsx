const features = [
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="16 18 22 12 16 6" /><polyline points="8 6 2 12 8 18" />
      </svg>
    ),
    title: "reveal.js Output",
    description: "Self-contained HTML. No dependencies to install. Open in any browser, present anywhere.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
    ),
    title: "Smart Segmentation",
    description: "Chapters, topic shifts, and code blocks detected automatically. Each segment maps to the right slide type.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" /><circle cx="8.5" cy="8.5" r="1.5" /><polyline points="21 15 16 10 5 21" />
      </svg>
    ),
    title: "Keyframe Extraction",
    description: "Representative frames pulled from each segment. Diagrams and screen content preserved as slide images.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 20V10" /><path d="M18 20V4" /><path d="M6 20v-4" />
      </svg>
    ),
    title: "Customizable Themes",
    description: "Night, Moon, Dracula, Solarized, and more. Or bring your own CSS for a completely custom look.",
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
    ),
    title: "Conversational Refinement",
    description: '"Make slide 3 shorter." "Add a code example." "Change the theme." Iterate naturally with your agent.',
  },
  {
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" /><line x1="4" y1="22" x2="4" y2="15" />
      </svg>
    ),
    title: "Speaker Notes",
    description: "Transcript segments become speaker notes automatically. Present with full context without reading slides.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-24 bg-surface-secondary">
      <div className="max-w-[1120px] mx-auto px-6">
        <div className="text-xs font-semibold uppercase tracking-[0.08em] text-primary mb-3">
          Features
        </div>
        <h2 className="text-3xl font-bold tracking-tight mb-4">
          Built for developers who present.
        </h2>
        <p className="text-base text-text-secondary max-w-[520px] mb-12">
          No drag-and-drop. No templates to fill in. Just structured data and
          beautiful output.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((f) => (
            <div
              key={f.title}
              className="bg-surface border border-border rounded-2xl p-6"
            >
              <div className="w-9 h-9 rounded-lg bg-primary-light text-primary flex items-center justify-center mb-3">
                {f.icon}
              </div>
              <h3 className="text-sm font-semibold mb-1">{f.title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed">
                {f.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
