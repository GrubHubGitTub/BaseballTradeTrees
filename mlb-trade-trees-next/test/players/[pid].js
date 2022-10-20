// const { connectToDatabase } = require('../../../lib/mongodb');

// export default async ({ query: { pid } }, res) => {
//     let { db } = await connectToDatabase();
//     const players = await db
//     .collection("TreeInfo")
//     .find({})
//     // .sort({ metacritic: -1 })
//     // .limit(10)
//     .toArray();
    
//     const filtered = players.filter((p) => p.retro_id === pid || p.mlbid === pid)
//     if (filtered.length > 0) {
//         res.status(200).json(filtered[0])
//       } else {
//         res.status(404).json({ message: `User with id: ${ pid } not found.` })
//       }
//     }
