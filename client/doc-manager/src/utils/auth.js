const TOKEN_NAME = 'FilesAuthToken'

// get token
const getToken = () => localStorage.getItem(TOKEN_NAME)
// set token
const setToken = (value) => localStorage.setItem(TOKEN_NAME, value)
// delete token
const removeToken = () => localStorage.removeItem(TOKEN_NAME)
// is_login  
const isAuth = () => !!getToken()



export { TOKEN_NAME, getToken, setToken, removeToken, isAuth }