let a = [|1;2;3|];;
let b = [|8;2;5|];;
let c = [|1;2;3;4;5;6;19;8;4|];;

let is_sorted a = 
  let b = Array.copy a in 
  Array.sort compare b;
  if a = b then true else false;;

let findfoo dict word =
  let rec binary_search dict word i = 
    if Array.length dict = 1 && dict.(0) = word
      then i
    else if Array.length dict = 1 
      then -1
    else
      let mid = (Array.length dict) / 2 in 
      let left = Array.sub dict 0 mid in
      let right = Array.sub dict mid ((Array.length dict) - 1) in
      if word < dict.(mid)
      then binary_search left word i-1
      else binary_search right word i+1 in
binary_search dict word ((Array.length dict) - 1) / 2;;

let find dict word = 
  let rec binary_search a value low high =
    if a = [||] then -1 
    else if high = low then
      if a.(low) = value then
        low
      else
        -1
    else let mid = (low + high) / 2 in
      if a.(mid) > value then
        binary_search a value low (mid - 1)
      else if a.(mid) < value then
        binary_search a value (mid + 1) high
      else
        mid in
  binary_search dict word 0 ((Array.length dict) - 1);;

find [|"a"; "b"; "c"|] "b";;
find [|"g"|] "g";;
find [|"a"; "b"; "c"|] "c";;
find [|"b"; "c"; "d"; "e"; "f"; "g"; "h"; "i"; "j"; "k"|] "e";;
find [|"a"; "b"; "c"|] "d";;
