// import { $fetch } from 'ohmyfetch'
export const useApi = (info?: RequestInfo, options: any = {}): Promise<unknown> => {
  const route = useRoute()
  const config = useRuntimeConfig()
  const requestHeaders = useRequestHeaders()
  console.log('using api...')
  return $fetch(info ?? route.fullPath, {
    ...options,
    headers: {
      ...options?.headers ?? {},
      ...requestHeaders,
      accept: 'application/json',
      host: '127.0.0.1:4000'
    }
  }).then(resp => {
    return resp
  })
}
