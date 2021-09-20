import axios from 'axios'
const config = require('./common.json')


const getAll = () => {
    const request = axios.get(config.BASEURL + "receipts")
    return request.then(r => r.data)
  }


const create = async newReceipt => {
  const response = await axios.post(`${config.BASEURL}receipts/`, newReceipt)
  return response.data
}

// eslint-disable-next-line import/no-anonymous-default-export
export default { getAll, create }
