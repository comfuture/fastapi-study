import accepts from 'accepts'
import httpProxy from 'http-proxy'
import { defineMiddleware } from 'h3'
import type { IncomingMessage as HttpIncomingMessage, ServerResponse } from 'http'
import { $fetch } from 'ohmyfetch'

const proxy = httpProxy.createProxyServer({})

export default defineMiddleware(async (req, res, nuxt) => {
  if (accepts(req).type(['html', 'json']) === 'json') {
    const r = await $fetch(`http://127.0.0.1:4000${req.url}`)
    res.writeHead(200, 'OK', {'Content-Type': 'application/json'})
    res.end(JSON.stringify(r))
  }
  nuxt()
})
