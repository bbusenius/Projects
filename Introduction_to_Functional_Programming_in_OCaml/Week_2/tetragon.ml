type point2D = int * int
type tetragon = (point2D * point2D * point2D * point2D)

let pairwise_distinct (lup, rup, llp, rlp) =
  let a, b, c, d = (lup, rup, llp, rlp) in 
  a <> b && a <> c && a <> d && 
  b <> a && b <> c && b <> d &&
  c <> a && c <> b && c <> d &&
  d <> a && d <> b && d <> c;; 

let get_coordinate point2d xy =
  let (x, y) = point2d in
  if xy = "x"
  then x
  else y;;  

let wellformed (lup, rup, llp, rlp) =
  let lup, rup, llp, rlp = (lup, rup, llp, rlp) in
  get_coordinate lup "x" < get_coordinate rup "x" && 
  get_coordinate lup "x" < get_coordinate rlp "x" &&
  get_coordinate llp "x" < get_coordinate rup "x" &&
  get_coordinate llp "x" < get_coordinate rlp "x" &&
  get_coordinate lup "y" > get_coordinate llp "y" && 
  get_coordinate rup "y" > get_coordinate rlp "y";; 

let rotate_point (x, y) : point2D =
  let x, y = (y, x * -1) in (x, y);;

let reorder x = 
  let perm(a,b,c,d)=(d,a,b,c)
  and swap(a,b,c,d)=(b,a,c,d) in
  let rec find l = function
     | x::t when wellformed x -> x 
     | x::t -> find (swap x::perm x::l) t
     | [] -> find [] l in
  find [] [x];;

let rotate_tetragon tetragon : tetragon =
  let (lup, rup, llp, rlp) = tetragon in 
  reorder (rotate_point(lup), rotate_point(rup), rotate_point(llp), rotate_point(rlp));;


pairwise_distinct ((0, 1), (2, 3), (4, 5), (6, 7));;

rotate_point (2, 3) ;;
