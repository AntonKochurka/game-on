import { createRootRoute, createRouter, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

const rootRoute = createRootRoute({
    component: () => (
        <>
            <Outlet />
            <TanStackRouterDevtools />
        </>
    )
});

const routeTree = rootRoute.addChildren([])
const router = createRouter({ routeTree });

export default router;