import { Nav } from "@/components/nav";
import { Hero } from "@/components/hero";
import { HowItWorks } from "@/components/how-it-works";
import { UseCases } from "@/components/use-cases";
import { Features } from "@/components/features";
import { AgentSkill } from "@/components/agent-skill";
import { FinalCTA } from "@/components/final-cta";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <HowItWorks />
        <UseCases />
        <Features />
        <AgentSkill />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}
