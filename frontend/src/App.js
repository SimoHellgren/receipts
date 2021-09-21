import React from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom'

import ReceiptsPage from './ReceiptsPage'
import ProductsPage from './ProductsPage'
import CreateReceiptPage from './CreateReceiptPage'

const routes = [
  {
    path: '/',
    exact: true,
    main: () => <ReceiptsPage/>
  },

  {
    path: '/products',
    exact: true,
    main: () => <ProductsPage/>
  },

  {
    path: '/receipts/create',
    exact: true,
    main: () => <CreateReceiptPage/>
  }
]

function App() {
  const padding = {padding: 5}
  return (
    <Router>
    <div>
      <Link to="/" style={padding}>Home</Link>
      <Link to="/products" style={padding}>Products</Link>
      <Link to="/receipts/create" style={padding}>Create Receipt</Link>
    </div>
    <div>
      <Switch>
        {routes.map((route, index) => (
          <Route 
            key={index}
            path={route.path}
            exact={route.exact}
            children={route.main}
          />
        )
          )}
      </Switch>
    </div>
    </Router>
  )
}

export default App;
