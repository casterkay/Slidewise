import { Layers, Monitor, PenTool, Users } from "lucide-react";

const useCases = [
  {
    icon: <PenTool size={22} className="text-purple-500" strokeWidth={2} />,
    iconBg: "bg-secondary-light",
    title: "Tutorials & Courses",
    description: "Transform technical walkthroughs into structured slide decks with code blocks, diagrams, and speaker notes preserved.",
  },
  {
    icon: <Users size={22} className="text-blue-500" strokeWidth={2} />,
    iconBg: "bg-primary-light",
    title: "Meeting Recordings",
    description: "Distill hour-long meetings into concise recap decks. Key decisions, action items, and discussion points on clear slides.",
  },
  {
    icon: <Layers size={22} className="text-green-600" strokeWidth={2} />,
    iconBg: "bg-success/8",
    title: "Podcasts & Talks",
    description: "Convert conference talks and podcast episodes into shareable visual summaries your audience can skim in minutes.",
  },
  {
    icon: <Monitor size={22} className="text-amber-600" strokeWidth={2} />,
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
