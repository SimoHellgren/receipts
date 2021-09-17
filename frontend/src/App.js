import React, {useState, useEffect} from 'react'
import axios from 'axios'

const APIRUL = 'http://localhost:8000/'

const get_one_receipt = () => {
  const request = axios.get(APIRUL + "receipts")
  return request.then(r => r.data[0])
}

const Receipt = ({receipt}) => {
  
  return (<div style={{whiteSpace: "break-spaces", fontFamily: "monospace"}}>
    <h2>Result: {receipt.id}</h2>
    <p>{receipt.reprint}</p>
  </div>
  )
}


function App() {
  const [receipt, setReceipt] = useState({})

  useEffect( () => {
    get_one_receipt().then(r => setReceipt(r))
  }, [])

  console.log(receipt.reprint)

  return <Receipt receipt={receipt}/>
}

export default App;
