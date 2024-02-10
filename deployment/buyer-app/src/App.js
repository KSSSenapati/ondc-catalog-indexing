import './App.scss';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

//Component
import Header from './components/header';

//Page
import Home from './page/home';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
]);

function App() {
  return (
    <>
      <Header />
      <RouterProvider router={router} />
    </>
  );
}

export default App;
