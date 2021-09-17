import React, {useState, useEffect} from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom'

import Receipt from './components/Receipt'
import receiptservice from './services/receipts'
import productservice from './services/products'


const ReceiptPage = () => {
  const [receipts, setReceipts] = useState([])
  
  const sortByDate = (a,b) => {
    if (a.datetime < b.datetime) return -1
    if (a.datetime > b.datetime) return 1
    return 0
  }
  
  useEffect( () => {
    // filter out receipts where date has not been parsed, because null dates screw up order
    // I'll promise to handle the problem more elegantly later :)
    receiptservice.getAll().then(r => setReceipts(r.filter(e => e.datetime !== null).sort(sortByDate).reverse()))
  }, [])
  
  
  return <div>
    <h2>Receipts</h2>
    {receipts.map(r => <Receipt key={r.id} receipt={r}/>)}
  </div>
}

const ProductPage = () => {
  const [products, setProducts] = useState([])

  useEffect(() => {
    productservice.getAll().then(p => setProducts(p))
  })

  return (
    <div>
      <h2>Products</h2>
      {products.map(p => <p>{p.id}</p>)}
    </div>
  )

}

const routes = [
  {
    path: '/',
    exact: true,
    menu: <div>Home</div>,
    main: () => <ReceiptPage/>
  },

  {
    path: '/products',
    exact: true,
    menu: <div>Products</div>,
    main: () => <ProductPage/>
  }
]

function App() {
  const padding = {padding: 5}
  return (
    <Router>
    <div>
      <Link to="/" style={padding}>Home</Link>
      <Link to="/products" style={padding}>Products</Link>
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
