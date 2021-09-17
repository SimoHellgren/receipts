import React, {useState, useEffect} from 'react'
import axios from 'axios'

const APIRUL = 'http://localhost:8000/'

const get_receipts = () => {
  const request = axios.get(APIRUL + "receipts")
  return request.then(r => r.data)
}

const Receipt = ({receipt}) => {
  const [showReprint, setShowReprint] = useState(false)

  const reprintStyle = {display: showReprint ? '' : 'none'}

  const handleClick = () => {
    setShowReprint(!showReprint)
  }

  return (<div style={{whiteSpace: "break-spaces", fontFamily: "monospace"}}>
    <h3>Receipt ID: {receipt.id}</h3>
    <p>Datetime: {receipt.datetime}</p>
    <p>Total: {receipt.total}</p>
    <button onClick={handleClick}>Toggle details</button>
    <p style={reprintStyle}>{receipt.reprint}</p>
  </div>
  )
}


function App() {
  const [receipts, setReceipts] = useState([])
  
  const sortByDate = (a,b) => {
    if (a.datetime < b.datetime) return -1
    if (a.datetime > b.datetime) return 1
    return 0
  }

  useEffect( () => {
    // filter out receipts where date has not been parsed, because null dates screw up order
    // I'll promise to handle the problem more elegantly later :)
    get_receipts().then(r => setReceipts(r.filter(e => e.datetime !== null).sort(sortByDate).reverse()))
  }, [])


  return <div>
    {receipts.map(r => <Receipt key={r.id} receipt={r}/>)}
  </div>
  
}

export default App;
