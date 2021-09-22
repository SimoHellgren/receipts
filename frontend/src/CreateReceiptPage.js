import { useState } from 'react'
import { useField } from './hooks'
import receiptservice from './services/receipts'

/**
 * A convenience component for adding products onto a receipt,
 * though I'm not entirely sure whether it really is convenient
 * or just convoluted.
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
      
      
      const newReceiptLines = products.map((p,i) => {
        const item = {
          linenumber: i+1, // start linenumbers from 1 
          product_id: p.name,
          amount: p.price
        }
        return item
      })
      
      const receipt = receiptservice.create(newReceipt)
    
      receipt.then(r => {
        receiptservice.create_receiptlines(r.id, newReceiptLines)
      })
  

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
  
export default CreateReceiptPage