import React, { useState, useEffect } from 'react'
import { useField } from './hooks'
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
  }, [])

  return (
    <div>
      <h2>Products</h2>
      {products.map(p => <p key={p.id}>{p.name} / {p.id}</p>)}
    </div>
  )

}

/**
 * A component for adding an individual product onto a receipt
 */
const ProductInput = ({data: [product, onChange]}) => {
  return (<div>
    <label>name: </label><input type="text" name="name" value={product.name} onChange={onChange}/>
    <label>price: </label><input type="text" name="price" value={product.price} onChange={onChange}/>
  </div>)
}

const CreateReceiptPage = () => {
  const {reset: resetReceiptDatetime, ...receiptDatetime} = useField('datetime-local', '')
  const {reset: resetReceiptStore, ...receiptStore} = useField('text', '')
  const {reset: resetReceiptTotal, ...receiptTotal} = useField('number', 0)
  const {reset: resetReceiptPaymentmethod, ...receiptPaymentmethod} = useField('text', '')

  const emptyProduct = {name: "", price: 0}
  const [products, setProducts] = useState([emptyProduct])


  const addProduct = () => {
    setProducts([...products, {...emptyProduct}])
  }
  
  const handleChange = (index, event) => {
    let newProducts = [...products]
    newProducts[index][event.target.name] = event.target.value
  
    setProducts(newProducts)
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    const newReceipt = {
      datetime: receiptDatetime.value,
      store_id: receiptStore.value,
      paymentmethod_id: receiptPaymentmethod.value,
      total: receiptTotal.value
    }

    const result = receiptservice.create(newReceipt)

    console.log(result)

    resetReceiptDatetime()
    resetReceiptStore()
    resetReceiptTotal()
    resetReceiptPaymentmethod()
    setProducts([{...emptyProduct}])
  }

  return (<div>
    <h2>Create Receipt</h2>
    <form onSubmit={handleSubmit}>
      
      <div>Datetime: <input {...receiptDatetime}/></div>
      <div>Store: <input {...receiptStore}/> </div>
      <div>Total: <input {...receiptTotal}/></div>
      <div>Payment method: <input {...receiptPaymentmethod}/></div>

      <h3>Products:</h3>
      <button type="button" onClick={addProduct}>Add product</button>
      {products.map((p, i) => (
        <ProductInput key={i} data={[p, e => handleChange(i,e)]}/>
      ))}

      <div></div>
      <input type="submit" value="Submit"/>
    </form>

    </div>)
}


const routes = [
  {
    path: '/',
    exact: true,
    main: () => <ReceiptPage/>
  },

  {
    path: '/products',
    exact: true,
    main: () => <ProductPage/>
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
