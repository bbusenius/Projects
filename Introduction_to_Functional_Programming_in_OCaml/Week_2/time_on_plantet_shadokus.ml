type date =
  { year : int; month : int; day : int;
    hour : int; minute : int }

let the_origin_of_time =
  { year = 1; month = 1; day = 1;
    hour = 0; minute = 0 }

let wellformed date =
  date.year >= 1 && 
  date.month >= 1 && date.month <= 5 && 
  date.day >= 1 && date.day <= 4 && 
  date.hour >= 0 && date.hour <= 2 && 
  date.minute >= 0 && date.minute <= 1;;

let next date =
  let a = {year = date.year; month = date.month; day = date.day; 
           hour = date.hour; minute = date.minute + 1} in 
  let b = {year = date.year; month = date.month; day = date.day; 
           hour = date.hour + 1; minute = 0} in 
  let c  = {year = date.year; month = date.month; day = date.day + 1; 
            hour = 0; minute = 0} in
  let d  = {year = date.year; month = date.month + 1; day = 1; 
            hour = 0; minute = 0} in
  let e  = {year = date.year + 1; month = 0; day = 0; 
            hour = 0; minute = 0} in 
  if wellformed a
  then a
  else if wellformed b
  then b
  else if wellformed c
  then c
  else if wellformed d
  then d
  else e;;

let of_int minutes =  
  let rec oi date = function 
    | 0 -> date 
    | m -> oi (next date) (m-1) in 
  oi the_origin_of_time minutes;;

of_int 151;;
