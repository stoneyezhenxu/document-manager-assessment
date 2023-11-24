
import React, { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import AuthRoute from './compoment/AuthRoute'


const Home = lazy(() => import('./pages/Home'))
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const UploadFile = lazy(() => import('./pages/UploadFile'))
const FileVersionDetails = lazy(() => import('./pages/FileVersionDetails'))
const ErrorPage = lazy(() => import('./pages/ErrorPage'))



const Routers = () => {
  return (

    <Suspense fallback={<div>Loading...</div>}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={(<AuthRoute><Home /></AuthRoute>)} />
          <Route path='*' element={<ErrorPage />} />
          <Route path='/error' element={<ErrorPage />} />
          <Route path="/files/*" element={(<AuthRoute><FileVersionDetails /> </AuthRoute>)} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/upload" element={(<AuthRoute><UploadFile /></AuthRoute>)} />
          <Route path="/details" element={(<AuthRoute><FileVersionDetails /></AuthRoute>)} />
        </Routes>
      </BrowserRouter>
    </Suspense>

  )
}



export default Routers