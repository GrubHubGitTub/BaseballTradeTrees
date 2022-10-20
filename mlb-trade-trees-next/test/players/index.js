// // import player_data from '../../../data/output.json'
// const { connectToDatabase } = require('../../../lib/mongodb');
// const ObjectId = require('mongodb').ObjectId;

// export default async (req, res) => {
//     let { db } = await connectToDatabase();
//     const players = await db
//     .collection("TreeInfo")
//     .find({})
//     // .sort({ metacritic: -1 })
//     .limit(100)
//     .toArray();
//     res.status(200).json(players)
//   }