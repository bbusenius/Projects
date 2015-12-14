let find_DEPRECATED a w = 
  let rec loop i = 
    if a = [||] || (i = 0 && a.(i) <> w)
    then None
    else if a.(i) = w 
    then Some i
    else loop (i - 1) in
  loop (Array.length a - 1);;

let find a w = 
  let rec loop i = 
    if i >= Array.length a then None
    else if a.(i) = w then Some i
    else loop (i + 1) in
  loop 0;;

let default_int_DEPRECATED i =
  match i with
  | None -> 0
  | Some n -> n;;

let default_int = function None -> 0 | Some n -> n;;

let merge a b = 
  match (a, b) with 
  | (None, None) -> None
  | (Some x, None) -> Some x 
  | (None, Some x) -> Some x 
  | (Some x, Some y) -> Some (x + y)

