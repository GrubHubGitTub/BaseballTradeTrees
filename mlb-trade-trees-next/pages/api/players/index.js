import player_data from '../../../data/output.json'

export default (req, res) => {
    res.status(200).json(player_data["player_data"])
  }