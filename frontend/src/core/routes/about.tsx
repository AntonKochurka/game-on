import { createFileRoute } from '@tanstack/react-router'
import { Layout } from '../components/layout'

export const Route = createFileRoute('/about')({
  component: RouteComponent,
})

function RouteComponent() {
  return <Layout><div>Hello "/about"!</div></Layout>
}
