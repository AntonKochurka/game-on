import { Link, useRouterState } from "@tanstack/react-router";

export const Header = () => {
  const { location } = useRouterState();

  return (
    <header className="fixed w-full z-50 backdrop-blur-xl bg-gray-950/85 border-b border-emerald-400/10">
      <nav className="max-w-8xl mx-auto px-6">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center gap-4">
            <Link to="/" className="relative group flex items-center gap-3">
              <div
                className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center 
                                border border-emerald-400/30 group-hover:border-emerald-400/50 transition-all"
              >
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              </div>
              <span
                className="text-2xl font-bold bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 
                                bg-clip-text text-transparent tracking-tighter"
              >
                GAME<span className="text-emerald-400">ON</span>
              </span>
            </Link>
          </div>

          <div className="flex items-center gap-10">
            <nav className="hidden lg:flex items-center gap-8">
              {["Tournaments", "Teams", "About"].map((item) => {
                const path = `/${item.toLowerCase()}`;
                const isActive = location.pathname === path;

                return (
                  <Link
                    key={item}
                    to={path}
                    className={`text-sm font-semibold transition-all duration-300 group ${
                      isActive
                        ? "text-emerald-300"
                        : "text-gray-400 hover:text-emerald-300"
                    }`}
                  >
                    {item}
                    <div
                      className={`h-0.5 bg-gradient-to-r from-emerald-400/0 via-emerald-400 to-emerald-400/0 
                                            w-0 group-hover:w-full transition-all duration-500 ${
                                              isActive ? "w-full" : ""
                                            }`}
                    />
                  </Link>
                );
              })}
            </nav>

            <button
              className="relative overflow-hidden px-8 py-3 rounded-full bg-gradient-to-r 
                            from-emerald-500/30 to-cyan-500/20 border border-emerald-400/20 hover:border-emerald-400/40 
                            backdrop-blur-lg transition-all hover:gap-4 group"
            >
              <span
                className="bg-gradient-to-r from-emerald-400 to-cyan-300 bg-clip-text text-transparent 
                                font-bold text-sm"
              >
                Join Arena
              </span>
              <div
                className="absolute inset-0 bg-gradient-to-r from-emerald-400/5 to-cyan-300/5 
                                opacity-0 group-hover:opacity-100 transition-all"
              />
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
};
