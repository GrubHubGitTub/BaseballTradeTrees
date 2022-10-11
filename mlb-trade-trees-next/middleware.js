import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'
import player_data from "./data/output.json"

export function middleware(req={NextRequest}) {
    var randompage = player_data[Math.floor(Math.random()*player_data.length)]
    var randomid = randompage.trades[Math.floor(Math.random()*randompage.trades.length)].tree_id
    var pid = randomid.slice(0,8)
  const url = req.nextUrl.clone()   
  if (url.pathname === '/random') {
    url.pathname = `/players/${pid}`
    return NextResponse.redirect(url)   
  } 
}