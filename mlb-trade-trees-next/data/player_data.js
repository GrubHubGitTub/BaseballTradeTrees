export const player_data = [

    { retro_id: "bichb001",
      mlbid: "666182",
      name: "Poopy Bumbum",
      HOF: "HOF/ empty string",
      debut_date: "first game date",
      last_date: "last game date or empty",
      latest_tree: "null or tree_id to link",
      trades: [
        {from_team: "TOR",
        from_franch: "TOR",
        transac_id: "retro",
        tree_id:"poops1",
        largest_tree_id: "retroid to link easily",
        tree_total_stats: {WAR: 1,
          IP: 2,
          etc: 3,},
        tree_details: {
                tree_id: "poops1",
                tree_display:[{
                id: "root",
                parentId: "",
                }, {id:1, parentId: "root"}],
                
              }
        },
        {from_team: "TOR",
        from_franch: "TOR",
        transac_id: "retro",
        tree_id:"poops3",
        largest_tree_id: "retroid to link easily",
        last_RS_tranasction: "",
        tree_total_stats: {WAR: 1,
          IP: 2,
          etc: 3,},
        tree_details: {
                tree_id: "poops3",
                tree_display:[{
                id: 1,
                parentId: "",
                name:"poopy",
                transaction_id:"123",
                trade_out_stats: [
                  {'id': 'songd101', 'name': 'Don Songer', "Batting stats":{}, "Pitching Stats": {}, "Awards": {}, "Playoffs":{}, 
                  "Allstar":{} },
                  {'id': 'may-b101', 'name': 'Buckshot May','WARout': "0.0", 'G out': 0, 'PA out': 0.0, 'IP out': 0.0, 'Salary out': 0.0} 
                ],
                trade_in_stats: [
                  {'id': 'may-b101', 'name': 'Buckshot May','WARout': 0.0, 'G in': 0, 'PA in': 0.0, 'IP in': 0.0, 'Salary in': 0.0},
                  {'id': 'songd101', 'name': 'Don Songer','WARout': 0.53, 'G out': 98, 'PA out': 46.0, 'IP out': 457.0, 'salary out': 0.0},

                ],
                trade_stats:"total in and out for transaction"
                },

                {id:2,
                parentId: 1,
                name:"bumbum",
                trade_out_stats: [
                  {'id': 'songd101', 'name': 'Other Poopy','WARout': "0.53", 'G out': 98, 'PA out': 46.0, 'IP out': 457.0, 'salary out': 0.0},
                  {'id': 'may-b101', 'name': 'BumBum','WARout': "0.0", 'G out': 0, 'PA out': 0.0, 'IP out': 0.0, 'Salary out': 0.0} 
                ],
                trade_in_stats: [
                  {'id': 'may-b101', 'name': 'Other Poopy','WARout': 0.0, 'G in': 0, 'PA in': 0.0, 'IP in': 0.0, 'Salary in': 0.0},
                  {'id': 'songd101', 'name': 'BumBum','WARout': 0.53, 'G out': 98, 'PA out': 46.0, 'IP out': 457.0, 'salary out': 0.0},

                ],
              }],
                
              }
        }
      ]
    }
  ]
  