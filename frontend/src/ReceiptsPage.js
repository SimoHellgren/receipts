import { useState, useEffect } from "react"
import Receipt from './components/Receipt'
import receiptservice from './services/receipts'


const ReceiptsPage = () => {
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
  
export default ReceiptsPage