import { WaitlistForm } from "./waitlist-form";

export function FinalCTA() {
  return (
    <section id="waitlist" className="py-24 text-center">
      <div className="max-w-[1120px] mx-auto px-6">
        <div className="text-xs font-semibold uppercase tracking-[0.08em] text-primary mb-3">
          Early Access
        </div>
        <h2 className="text-3xl font-bold tracking-tight mb-4 max-w-[500px] mx-auto">
          Stop building slides by hand.
        </h2>
        <p className="text-base text-text-secondary max-w-[520px] mx-auto mb-8">
          Join the waitlist for early access. Free during beta &mdash; we&apos;ll
          notify you as soon as it&apos;s ready.
        </p>
        <WaitlistForm id="footer-form" />
      </div>
    </section>
  );
}
