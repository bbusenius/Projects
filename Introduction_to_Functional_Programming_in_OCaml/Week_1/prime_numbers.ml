let rec gcd n m = 
  if m = 0
  then n
  else gcd m (n mod m);;

let multiple_upto n r =
  let rec helper n r d = 
    if r < 2
    then false
    else if n mod d == 0
    then true
    else if d >= r
    then false
    else
      helper n r (d+1) in
  helper n r 2;;

let is_prime n = 
  let rec helper n i = 
    if ((n mod i = 0) && (n <> 2) && (n <> i)) || n < 2
    then false
    else 
    if i < integer_square_root n
    then helper n (i + 1) 
    else
      true in
  helper n 2;;
