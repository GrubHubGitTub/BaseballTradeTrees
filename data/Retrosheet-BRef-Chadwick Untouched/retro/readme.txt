Here's the format of each record in the transaction database.
 
  primary-date,
  time,
  approximate-indicator,
  secondary-date,
  approximate-indicator (for secondary-date),
  transaction-ID,
  player,
  type,
  from-team,
  from-league,
  to-team,
  to-league,
  draft-type,
  draft-round,
  pick-number,
  info
 
primary-date - "yyyymmdd"
       Where:
         yyyy - is the year
         mm - is a two-digit month (01-12)
         dd - is a two-digit day (01-31)
       A "00" in the day field means that that level of precision is
       not known.
       A "0000" in the month AND day field means that the transaction
       occurred sometime prior to the start of the season.  Such a
       transaction could have taken place in the latter part of the
       previous year as well.
time - an optional one digit time indicator:
       empty (default) - transaction occurred before all games
       1 - transaction occurred after the from-team's first or only
           game of the day and before the to-team's last or only game
           of the day.
       2 - transaction occurred after all games
       this field may also be used in off-season transactions to
       establish an order between different transactions involving the
       same players.
approximate-indicator - "@" if the date is approximate.
       This field is not set simply if the month or day is not known.
       It is only used if some information is provided (a non-zero month
       or day) which is only a guess.
secondary-date - "yyyymmdd"
       Same format as above.
       At present this is used for "Da" types to indicate the player's
       signing date (the primary-date field for these transactions
       contains the date of the start of the draft).
transaction-id - a number identifying the transaction
player - One of the following:
         an eight character player ID
         a string containing the first and last name of players
         who haven't reached the major leagues
         empty (no player is associated with the record)
type - one of the following
         A  - assigned from one team to another without compensation
         C  - conditional deal
         Cr - returned to original team after conditional deal
         D  - rule 5 draft pick
         Da - amateur draft pick
         Df - first year draft pick
         Dm - minor league draft pick
         Dn - selected in amateur draft but did not sign
         Dr - returned to original team after draft selection
         Ds - special draft pick
         Dv - amateur draft pick voided
         F  - free agent signing
         Fa - amateur free agent signing
         Fb - amateur free agent "bonus baby" signing under the 1953-57
              rule requiring player to stay on ML roster
         Fc - free agent compensation pick
         Fg - free agent granted
         Fo - free agent signing with first ML team
         Fv - free agent signing voided
         Hb  - went on the bereavement list
         Hbr - came off the bereavement list
         Hd  - declared ineligible
         Hdr - reinistated from the ineligible list
         Hf  - demoted to the minor league
         Hfr - promoted from the minor league
         Hh  - held out
         Hhr - ended hold out
         Hi  - went on the disabled list
         Hir - came off the disabled list
         Hm  - went into military service
         Hmr - returned from military service
         Hs  - suspended
         Hsr - reinstated after a suspension
         Hu  - unavailable but not on DL
         Hur - returned from being unavailable
         Hv  - voluntarity retired
         Hvr - unretired
         J  - jumped teams
         Jr - returned to original team after jumping
         L  - loaned to another team
         Lr - returned to original team after loan
         M  - obtained rights when entering into working agreement with
              minor league team
         Mr - rights returned when working agreement with minor league
              team ended
         P  - purchase
         Pr - returned to original team after purchase
         Pv - purchase voided
         R  - release
         T  - trade
         Tn - traded but refused to report
         Tp - added to trade (usually because one of the original
              players refused to report or retired)
         Tr - returned to original team after trade
         Tv - trade voided
         U  - unknown (could have been two separate transactions)
         Vg - player assigned to league control
         V  - player purchased or assigned to team from league
         W  - waiver pick
         Wf - first year waiver pick
         Wr - returned to original team after waiver pick
         Wv - waiver pick voided
         X  - expansion draft
         Xe - premium phase of expansion draft
         Xm - either the 1960 AL minor league expansion draft or
              the premium phase of the 1961 NL draft 
         Xp - added as expansion pick at a later date
         Xr - returned to original team after expansion draft
         Z  - voluntarily retired
         Zr - returned from voluntarily retired list
from-team - either a three character major league team abbreviation
            or the name of an independent minor league team indicating
            where the player came from.  Some transactions (for example,
            "Da" will not have a from-team (or league).
from-league - either a two character major league abbreviation or the
              name of a minor league in parenthesis.
to-team - either a three character major league team abbreviation
          or the name of an independent minor league team indicating
          where the player went to.  Some transactions (for example,
          "Fg" will not have a to-team (or league).
to-league - either a two character major league abbreviation or the
            name of a minor league in parenthesis.
draft-type - (Da, Dn and Dv types only) the type of amateur draft
             The default is the regular draft
             S - secondary phase (or secondary phase delayed)
             A - secondary phase active
             L - American Legion
             D - Dominican draft
draft-round - (Da, Dn and Dv types only) the round of the amateur draft
             that the player was selected in
pick-number - For expansion drafts, this contain the number of the pick.
              For amateur drafts, this will contain the number of the
              selection for first round picks.
info - This contain information associated with the transaction.  For
       trades, this field could contain money sent in addition to
       players.  For player sales, this could contain the sale amount.
 
If a "F" transaction has both a from and a to team, there will be no
corresponding "Fg" transactions.  These two-team "F" transactions are
used in eras where players were not reserved and so were free to sign
with whoever those at the end of each contract.
 
