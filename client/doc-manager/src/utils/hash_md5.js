
import CryptoJS from 'crypto-js'

const getFileHashCode = (fileName) => {
  const hash = CryptoJS.MD5(fileName)
  return hash.toString(CryptoJS.enc.Hex)
}

export { getFileHashCode }