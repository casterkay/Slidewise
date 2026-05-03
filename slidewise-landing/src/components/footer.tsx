import Link from "next/link";

export function Footer() {
  return (
    <footer className="py-8 border-t border-border">
      <div className="max-w-[1120px] mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <span className="text-sm text-text-tertiary">Slidewise</span>
        <ul className="flex gap-6 list-none">
          <li>
            <Link href="#how-it-works" className="text-sm text-text-tertiary no-underline hover:text-text transition-colors duration-200">
              How it works
            </Link>
          </li>
          <li>
            <Link href="#features" className="text-sm text-text-tertiary no-underline hover:text-text transition-colors duration-200">
              Features
            </Link>
          </li>
          <li>
            <Link href="#waitlist" className="text-sm text-text-tertiary no-underline hover:text-text transition-colors duration-200">
              Waitlist
            </Link>
          </li>
        </ul>
      </div>
    </footer>
  );
}
