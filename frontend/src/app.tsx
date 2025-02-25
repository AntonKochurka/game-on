import { Provider } from "react-redux";
import { RouterProvider } from "@tanstack/react-router";

import store from "./core/redux";
import router from "./core/utils/router";

const App = () => {
  return (
    <Provider store={store}>
      <RouterProvider router={router}/>
    </Provider>
  )
}

export default App;