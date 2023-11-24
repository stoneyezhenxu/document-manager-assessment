import { Navigate, useLocation } from 'react-router-dom'
import { message } from 'antd'
import { isAuth } from '../../utils'

const AuthRoute = ({ children }) => {
    const isLogin = isAuth()
    const location = useLocation()
    if (!isLogin) {
        message.info('Please Login to get an authorization!')
        return (
            <Navigate to="/login" state={{ from: location }} />
        )
    }
    return children
}
export default AuthRoute