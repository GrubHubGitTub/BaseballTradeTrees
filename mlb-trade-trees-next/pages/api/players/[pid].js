import { player_data } from '../../../data/player_data'

export default ({ query: { pid } }, res) => {
    const filtered = player_data.filter((p) => p.retro_id === pid || p.mlbid === pid)
    if (filtered.length > 0) {
        res.status(200).json(filtered[0])
      } else {
        res.status(404).json({ message: `User with id: ${ pid } not found.` })
      }
    }
