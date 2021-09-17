import React, {useState, useEffect} from 'react'
import axios from 'axios'

const APIRUL = 'http://localhost:8000/'

const get_one_receipt = () => {
  const request = axios.get(APIRUL + "receipts")
  return request.then(r => r.data[0])
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
    <button onClick={handleClick}>Show details</button>
    <p style={reprintStyle}>{receipt.reprint}</p>
  </div>
  )
}


function App() {
  const [receipt, setReceipt] = useState({})

  useEffect( () => {
    get_one_receipt().then(r => setReceipt(r))
  }, [])

  return <Receipt receipt={receipt}/>
}

export default App;
