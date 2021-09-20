import axios from 'axios'
const config = require('./common.json')

const path = `${config.BASEURL}/receipts`

const getAll = () => {
    const request = axios.get(path)
    return request.then(r => r.data)
  }


const create = async newReceipt => {
  const response = await axios.post(path, newReceipt)
  return response.data
}

// eslint-disable-next-line import/no-anonymous-default-export
export default { getAll, create }
