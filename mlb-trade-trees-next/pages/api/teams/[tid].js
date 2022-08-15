import { team_data } from '../../../data/team_data'

export default ({ query: { tid } }, res) => {
    const filtered = team_data.filter((t) => t.team_id === tid )

    if (filtered.length > 0) {
        res.status(200).json(filtered[0])
      } else {
        res.status(404).json({ message: `User with id: ${ tid } not found.` })
      }
    }