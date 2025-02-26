import { createFileRoute } from '@tanstack/react-router'
import { Layout } from '../../components/layout'

export const Route = createFileRoute('/teams/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <Layout><div>Hello "/teams/"!</div></Layout>
}
