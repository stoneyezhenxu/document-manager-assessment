
import { useNavigate } from 'react-router-dom'
import styles from './index.module.css'
const ErrorPage = () => {
  const navigate = useNavigate()

  return (
    <div className={styles.ErrorCard}>
      <h1> Error 404 Page !</h1>
      <div> If you've already Login, Just go back to <span onClick={() => navigate('/')}>Dashboard Page</span></div>
      <div>If you haven't register account,  Go to <span onClick={() => navigate('/register')}>Register Page </span></div>
      <div>If you haven't Login,  Go to <span onClick={() => navigate('/login')}>Login page</span> </div>
    </div>
  )
}


export default ErrorPage