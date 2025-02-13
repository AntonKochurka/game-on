import { Provider } from "react-redux";
import { createRouter, RouterProvider } from "@tanstack/react-router";
import store from "./core/redux";

import { routeTree } from './routeTree.gen'

const router = createRouter({ routeTree })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

const App = () => {
  return (
    <Provider store={store}>
      <RouterProvider router={router}/>
    </Provider>
  )
}

export default App;