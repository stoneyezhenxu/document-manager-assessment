import axios from 'axios'
import { getToken, removeToken } from './auth'

const accessToken = 'a5c328ce13cbc28f79e344ac8925462b22ff13b8'
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
        // config.headers.Authorization = getToken()

        config.headers.Authorization = `Token ${accessToken}`
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