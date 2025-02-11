import type { BaseQueryFn } from '@reduxjs/toolkit/query'
import axios, { AxiosError, AxiosRequestConfig } from 'axios'

const api = axios.create({
    withCredentials: true,
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.request.use((config) => {
    console.log('[ Request ]', config.url);
    return config;
});
  
api.interceptors.response.use((response) => {
    console.log('[ Response ]', response.status, response.data);
    return response;
});

const apiBaseQuery =
  (
    { baseUrl }: { baseUrl: string } = { baseUrl: api.defaults.baseURL! },
  ): BaseQueryFn<
    {
      url: string
      method?: AxiosRequestConfig['method']
      data?: AxiosRequestConfig['data']
      params?: AxiosRequestConfig['params']
      headers?: AxiosRequestConfig['headers']
    },
    unknown,
    unknown
  > =>
  async ({ url, method, data, params, headers }) => {
    try {
      const result = await api({
        url: baseUrl + url,
        method,
        data,
        params,
        headers,
      })

      return { data: result.data }
    } catch (axiosError) {
      const err = axiosError as AxiosError
      return {
        error: {
          status: err.response?.status,
          data: err.response?.data || err.message,
        },
      }
    }
  }

export default {api, apiBaseQuery};