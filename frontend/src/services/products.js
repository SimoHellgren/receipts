import axios from 'axios'
const config = require('./common.json')


const getAll = () => {
    const request = axios.get(config.BASEURL + "products")
    return request.then(r => r.data)
  }


// eslint-disable-next-line import/no-anonymous-default-export
export default { getAll }
