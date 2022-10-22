    // import tree_data from "../../../data/all_parent_trees.json"
    
    // export default function handler (req, res) {
    //     console.log(req.body)
    //     const team = req.body.team.toLowerCase()
        

    //     const filtered = tree_data.filter(tree => {
    //         return tree.from_team.team_name.toLowerCase().includes(team);
    //     })
    //     if (filtered.length > 0) {
    //         res.status(200).json({ data: filtered })
    //     }else{
    //         res.status(404).json({ message: `No trees with this team name found` })
    //     }

    //     // const WAR = req.query.war;
        
        
    //     // if (filtered.length > 0) {
    //     //     res.status(200).json(filtered)
    //     // } else {
    //     //     res.status(404).json({ message: `Tree with id: ${ WAR } not found.` })
    //     // }
    // }
