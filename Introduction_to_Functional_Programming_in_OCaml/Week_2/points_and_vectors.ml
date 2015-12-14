type point  = { x : float; y : float; z : float }
type dpoint = { dx : float; dy : float; dz : float }
type physical_object = { position : point; velocity : dpoint }

let move p dp =
  {x = p.x +. dp.dx; y = p.y +. dp.dy; z = p.z +. dp.dz};;

let next obj =
  {position = move obj.position obj.velocity; velocity = obj.velocity}

let ap n : float =
  if n >= 0. then n else n *. -1.0;;

let point_dist p1 p2 =
  let size = 2. in
  sqrt((p2.x -. p1.x) ** size +. 
       (p2.y -. p1.z) ** size +. 
       (p2.z -. p1.z) ** size);;

let will_collide_soon p1 p2 =
  let size = 2. in
  let p1 = next p1 in 
  let p2 = next p2 in
  point_dist p1.position p2.position < size;;


will_collide_soon
  {position = {x = 1.035; y = 1.400; z = 0.226};
   velocity = {dx = 0.901; dy = 0.297; dz = -0.474}}
  {position = {x = 0.674; y = 0.435; z = -0.473};
   velocity = {dx = 0.220; dy = 0.840; dz = -0.948}};;
