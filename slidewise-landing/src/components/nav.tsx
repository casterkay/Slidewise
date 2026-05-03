import Link from "next/link";

export function Nav() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 py-4 bg-white/72 backdrop-blur-[20px] backdrop-saturate-[180%] border-b border-border transition-colors duration-200">
      <div className="max-w-[1120px] mx-auto px-6 flex items-center justify-between">
        <Link href="#" className="flex items-center gap-2 font-bold text-lg text-text no-underline">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center text-white">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="5 3 19 12 5 21 5 3" />
            </svg>
          </div>
          Slidewise
        </Link>
        <ul className="flex items-center gap-8 list-none">
          <li className="hidden md:block">
            <Link href="#how-it-works" className="text-sm font-medium text-text-secondary no-underline hover:text-text transition-colors duration-200">
              How it works
            </Link>
          </li>
          <li className="hidden md:block">
            <Link href="#use-cases" className="text-sm font-medium text-text-secondary no-underline hover:text-text transition-colors duration-200">
              Use cases
            </Link>
          </li>
          <li className="hidden md:block">
            <Link href="#features" className="text-sm font-medium text-text-secondary no-underline hover:text-text transition-colors duration-200">
              Features
            </Link>
          </li>
          <li>
            <Link
              href="#waitlist"
              className="text-sm font-semibold text-primary bg-primary-light px-4 py-2 rounded-full no-underline hover:bg-primary hover:text-white transition-all duration-200"
            >
              Join Waitlist
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
