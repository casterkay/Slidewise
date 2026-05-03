"use client";

import { useState, useTransition } from "react";
import { joinWaitlist } from "@/app/actions";

export function WaitlistForm({ id }: { id: string }) {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [isPending, startTransition] = useTransition();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    startTransition(async () => {
      const result = await joinWaitlist(email);
      setMessage(result.message);
      setIsSuccess(result.success);
      if (result.success) setEmail("");
    });
  }

  return (
    <div>
      <form
        id={id}
        onSubmit={handleSubmit}
        className="flex flex-col sm:flex-row gap-3 max-w-[440px] mx-auto"
        aria-label="Join the waitlist"
      >
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@email.com"
          required
          aria-label="Email address"
          className="flex-1 px-4 py-3 text-base border-[1.5px] border-border-strong rounded-xl bg-surface text-text outline-none transition-all duration-200 placeholder:text-text-tertiary focus:border-primary focus:shadow-[0_0_0_3px_var(--color-primary-glow)]"
        />
        <button
          type="submit"
          disabled={isPending}
          className="px-6 py-3 text-base font-semibold text-white bg-primary rounded-xl whitespace-nowrap transition-all duration-200 hover:bg-primary-hover active:scale-[0.97] disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
        >
          {isPending ? "Joining..." : "Join Waitlist"}
        </button>
      </form>
      <div
        role="status"
        aria-live="polite"
        className={`text-center mt-3 text-sm min-h-[20px] ${
          isSuccess ? "text-success" : "text-danger"
        }`}
      >
        {message}
      </div>
    </div>
  );
}
