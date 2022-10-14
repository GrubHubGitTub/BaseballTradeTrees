// import { NextResponse } from 'next/server'
// import { NextRequest } from 'next/server'
// import player_search from "./data/player_search.json"

// export function middleware(req={NextRequest}) {
//     var randomplayer = player_search[Math.floor(Math.random()*player_search.length)]
//     // var randomid = randompage.trades[Math.floor(Math.random()*randompage.trades.length)].tree_id
//     var pid = randomplayer.retro_id
//   const url = req.nextUrl.clone()   
//   if (url.pathname === '/random') {
//     url.pathname = `/players/${pid}/`
//     return NextResponse.redirect(url)   
//   } 
// }