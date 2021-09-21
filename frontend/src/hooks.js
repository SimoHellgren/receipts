import { useState } from 'react'


export const useField = (type, initValue) => {
    const [value, setValue] = useState(initValue)
  
    const onChange = (event) => {
      setValue(event.target.value)
    }
  
    const reset = () => setValue(initValue)
  
    return {
      type,
      value,
      onChange,
      reset
    }
  }