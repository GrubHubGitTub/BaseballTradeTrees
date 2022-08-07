import { player_data } from '../../../data/player_data'

export default (req, res) => {
    res.status(200).json(player_data)
  }