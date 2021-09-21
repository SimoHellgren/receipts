import { useState, useEffect } from 'react'

import productservice from './services/products'

const ProductsPage = () => {
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

export default ProductsPage