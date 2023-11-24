import axios from 'axios'
import { getToken, removeToken } from './auth'

export const axiosAPI = axios.create({
    baseURL: process.env.REACT_APP_URL
})

// request interceptors
axiosAPI.interceptors.request.use((config) => {
    const { url } = config

    if (
        url.startsWith('/api')
        && !url.startsWith('/api/login')
        && !url.startsWith('/api/register')
    ) {
        config.headers.Authorization = `Token ${getToken()}`

    }


    return config
})

// response interceptors
axiosAPI.interceptors.response.use((response) => {
    const { status } = response.data

    if (status === 400) {
        removeToken()
    }

    return response
})