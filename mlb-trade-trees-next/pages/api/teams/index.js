import { team_data } from '../../../data/team_data'

export default (req, res) => {
    res.status(200).json(team_data)
  }