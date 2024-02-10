import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

//Page
import Home from './pages/Home';
import AddProduct from "./pages/AddProduct";
import UpdateProduct from "./pages/UpdateProduct";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/addProduct",
    element: <AddProduct />
  },
  {
    path: "/updateProduct",
    element: <UpdateProduct />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;