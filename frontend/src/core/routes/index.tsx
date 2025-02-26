import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "../components/layout";

export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Layout>
      <div className="text-center space-y-8 mb-24">
        <h1 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-500 leading-tight">
          Dominate the Arena
        </h1>
        <p className="text-xl text-gray-200 max-w-2xl mx-auto">
          Join millions of players worldwide in the ultimate cyber gaming
          experience. Compete, stream, and climb the leaderboards.
        </p>
      </div>
    </Layout>
  );
}
