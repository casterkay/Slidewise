import { WaitlistForm } from "./waitlist-form";

export function Hero() {
  return (
    <section className="pt-[156px] pb-24 text-center relative overflow-hidden">
      {/* Glow */}
      <div className="absolute -top-[200px] left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-[radial-gradient(circle,var(--color-primary-glow)_0%,transparent_70%)] pointer-events-none" />

      <div className="max-w-[1120px] mx-auto px-6 relative">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary-light border border-primary/12 rounded-full text-xs font-semibold text-primary uppercase tracking-wider mb-6">
          <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
          Coming Soon
        </div>

        <h1 className="text-[clamp(36px,6vw,64px)] font-extrabold leading-[1.08] tracking-[-0.03em] max-w-[780px] mx-auto mb-6">
          Video in.
          <br />
          <span className="bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent">
            Beautiful slides
          </span>{" "}
          out.
        </h1>

        <p className="text-lg leading-relaxed text-text-secondary max-w-[560px] mx-auto mb-8">
          Turn podcasts, tutorials, meeting recordings, and screen recordings
          into polished reveal.js slide decks &mdash; right from your terminal.
        </p>

        <WaitlistForm id="hero-form" />

        <p className="mt-4 text-xs text-text-tertiary">
          Free during beta. No spam, ever.
        </p>

        {/* Demo Visual */}
        <div className="mt-16" aria-hidden="true">
          <div className="bg-surface border border-border rounded-2xl shadow-[0_16px_48px_rgba(0,0,0,0.1)] overflow-hidden max-w-[920px] mx-auto">
            {/* Toolbar */}
            <div className="flex items-center gap-2 px-4 py-3 bg-surface-secondary border-b border-border">
              <div className="w-3 h-3 rounded-full bg-[#FF5F57]" />
              <div className="w-3 h-3 rounded-full bg-[#FFBD2E]" />
              <div className="w-3 h-3 rounded-full bg-[#28C840]" />
            </div>
            {/* Body */}
            <div className="grid grid-cols-1 md:grid-cols-[1fr_32px_1fr] items-center gap-4 md:gap-0 p-8">
              {/* Input */}
              <div className="bg-surface-secondary border border-dashed border-border-strong rounded-xl p-6 min-h-[200px] flex flex-col justify-center">
                <div className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">
                  Input
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-text rounded-lg flex items-center justify-center shrink-0">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                      <polygon points="5 3 19 12 5 21 5 3" />
                    </svg>
                  </div>
                  <div className="text-left">
                    <div className="text-sm font-semibold text-text">
                      Building a REST API with FastAPI
                    </div>
                    <div className="text-xs text-text-tertiary mt-0.5">
                      youtube.com &middot; 14:32
                    </div>
                  </div>
                </div>
              </div>

              {/* Arrow */}
              <div className="flex items-center justify-center text-primary rotate-90 md:rotate-0">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12" />
                  <polyline points="12 5 19 12 12 19" />
                </svg>
              </div>

              {/* Output */}
              <div className="bg-[#1E1E2E] border border-white/6 rounded-xl p-6 min-h-[200px] flex flex-col justify-center">
                <div className="text-xs font-semibold uppercase tracking-wider text-white/30 mb-3">
                  Output
                </div>
                <div className="flex flex-col gap-2">
                  <div className="text-lg font-bold text-white">
                    REST API with FastAPI
                  </div>
                  <ul className="list-none flex flex-col gap-1">
                    {[
                      "Project setup and dependencies",
                      "Defining Pydantic models",
                      "CRUD endpoints and routing",
                      "Error handling patterns",
                    ].map((item) => (
                      <li
                        key={item}
                        className="text-sm text-white/60 pl-4 relative before:content-[''] before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:rounded-full before:bg-primary"
                      >
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
