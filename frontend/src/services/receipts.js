import axios from 'axios'
const config = require('./common.json')

const path = `${config.BASEURL}/receipts`

const getAll = () => {
    const response = axios.get(path)
    return response.then(r => r.data)
  }


const create = async newReceipt => {
  const response = await axios.post(path, newReceipt)
  return response.data
}

const create_receiptlines = async (receipt_id, lines) => {
  const response = await axios.post(`${path}/${receipt_id}/lines`, lines)
  return response.data
}

// eslint-disable-next-line import/no-anonymous-default-export
export default { getAll, create, create_receiptlines }
