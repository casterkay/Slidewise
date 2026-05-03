const steps = [
  {
    number: 1,
    title: "Drop in a video",
    description:
      "Paste a YouTube URL or point to a local recording. Slidewise handles the rest \u2014 download, transcription, keyframe extraction.",
    code: (
      <>
        <span className="text-primary">$</span>{" "}
        <span className="text-primary">claude</span>{" "}
        <span className="text-[#A5D6FF]">&quot;turn this video into slides&quot;</span>
        <br />
        <span className="text-text-tertiary"># paste your URL when prompted</span>
      </>
    ),
  },
  {
    number: 2,
    title: "AI structures your content",
    description:
      "The API transcribes audio, identifies chapters, classifies segments (code, diagrams, explanations), and plans an optimal slide outline.",
    code: (
      <>
        <span className="text-success">Extracting...</span> 12 segments found
        <br />
        <span className="text-success">Planning...</span> 9 slides, 2 code blocks
      </>
    ),
  },
  {
    number: 3,
    title: "Get a slides deck",
    description:
      "Your agent generates a self-contained HTML file. Open it in any browser. Customize themes, reorder slides, or refine content conversationally.",
    code: (
      <>
        <span className="text-success">Wrote</span> slides.html{" "}
        <span className="text-text-tertiary">(self-contained)</span>
        <br />
        <span className="text-primary">$</span>{" "}
        <span className="text-primary">open</span> slides.html
      </>
    ),
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 bg-surface-secondary">
      <div className="max-w-[1120px] mx-auto px-6">
        <div className="text-xs font-semibold uppercase tracking-[0.08em] text-primary mb-3">
          How it works
        </div>
        <h2 className="text-3xl font-bold tracking-tight mb-4">
          Three steps. Zero slides built by hand.
        </h2>
        <p className="text-base text-text-secondary max-w-[520px] mb-12">
          Slidewise processes your video, extracts structure and visuals, and
          generates a fully styled slide deck you can present immediately.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step) => (
            <div key={step.number}>
              <div className="w-9 h-9 rounded-full bg-primary text-white text-sm font-bold flex items-center justify-center mb-4">
                {step.number}
              </div>
              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed">
                {step.description}
              </p>
              <div className="mt-4 bg-[#1E1E2E] rounded-lg px-4 py-3 font-mono text-xs text-white/70 overflow-x-auto border border-white/6">
                {step.code}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
