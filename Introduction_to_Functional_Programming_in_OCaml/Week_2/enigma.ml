let exchange k = 
  let s = string_of_int k in
  let s1 = Char.escaped(String.get s 0) in
  let s2 = Char.escaped(String.get s 1) in
  int_of_string (s2 ^ s1);;

let is_valid_answer (grand_father_age, grand_son_age) =
  if grand_son_age * 4 = grand_father_age && (exchange grand_father_age) * 3 = exchange grand_son_age
  then true
  else false;;

let get_age answer person =
  let grand_father_age, grand_son_age = answer in 
  if person = "gf"
  then grand_father_age
  else grand_son_age;;

let find answer = 
  let rec helper gsa = 
    let gfa = gsa * 4 in
    if gfa > get_age answer "gf"
    then (-1, -1)
    else if is_valid_answer((gfa, gsa))
    then (gfa, gsa)
    else helper (gsa + 1) in
  helper (get_age answer "gs");;
