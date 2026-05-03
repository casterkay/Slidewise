import { Code, Flag, Image as ImageIcon, MessageSquare, Search, Sliders } from "lucide-react";

const features = [
  {
    icon: <Code size={18} />,
    title: "Slides Output",
    description: "Self-contained HTML. No dependencies to install. Open in any browser, present anywhere.",
  },
  {
    icon: <Search size={18} />,
    title: "Smart Segmentation",
    description: "Chapters, topic shifts, and code blocks detected automatically. Each segment maps to the right slide type.",
  },
  {
    icon: <ImageIcon size={18} />,
    title: "Keyframe Extraction",
    description: "Representative frames pulled from each segment. Diagrams and screen content preserved as slide images.",
  },
  {
    icon: <Sliders size={18} />,
    title: "Customizable Themes",
    description: "Night, Moon, Dracula, Solarized, and more. Or bring your own CSS for a completely custom look.",
  },
  {
    icon: <MessageSquare size={18} />,
    title: "Conversational Refinement",
    description: '"Make slide 3 shorter." "Add a code example." "Change the theme." Iterate naturally with your agent.',
  },
  {
    icon: <Flag size={18} />,
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
