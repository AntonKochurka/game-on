import { createFileRoute } from '@tanstack/react-router'
import { Layout } from '../../components/layout'

export const Route = createFileRoute('/tournaments/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <Layout><div>Hello "/tournaments/"!</div></Layout>
}
