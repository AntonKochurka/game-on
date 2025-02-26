import { ReactNode } from "react";
import { Header } from "./header";

export const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="min-h-screen bg-gray-950 relative overflow-x-hidden">
      <div
        className="fixed -top-96 -left-96 w-[1200px] h-[1200px] bg-radial-gradient(from 60% 50% at 50% 50%, 
        rgba(16, 185, 129, 0.15) 0%, transparent 70%)"
      />

      <div
        className="fixed -top-48 -right-96 w-[1000px] h-[1000px] bg-radial-gradient(from 30% 50% at 50% 50%, 
        rgba(34, 211, 238, 0.1) 0%, transparent 70%)"
      />

      <Header />

      <main className="relative z-10 pt-32 pb-24">
        <div className="max-w-8xl mx-auto px-6">{children}</div>
      </main>

      <div className="absolute inset-0 pointer-events-none">
        <div className="h-full mx-auto max-w-8xl px-6 grid grid-cols-12 gap-6 opacity-5">
          {Array.from({ length: 12 }).map((_, i) => (
            <div
              key={i}
              className="h-full bg-gradient-to-b from-emerald-400/30 to-transparent"
            />
          ))}
        </div>
      </div>
    </div>
  );
};
