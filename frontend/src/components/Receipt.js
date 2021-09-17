import React, {useState} from 'react'

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

export default Receipt