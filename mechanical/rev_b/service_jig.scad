// Three-pin home-programming fixture, geometry study only. Units: mm.
// Earring sits rear-side toward three spring contacts. Verify the final
// board/tray outline, pad order and actual pogo pin drawings before use.
$fn = 48;
jig_w = 38;
jig_h = 54;
base = 7;
pocket_w = 28.6;
pocket_h = 44.6;
pocket_depth = 2.4;
pocket_x = 4.7;
pocket_y = 4.7;
board_offset = 1.3;
pad_y = 39.5;
service_pad_x = [10,16,22]; // P2 GND, P3 UPDI, P4 VTG_3V45
pin_bore_d = 1.8;           // change to measured purchased spring-pin body

module rounded_plate(w,h,r,z) {
    linear_extrude(height=z)
        hull() for (x=[r,w-r],y=[r,h-r]) translate([x,y]) circle(r=r);
}

difference() {
    rounded_plate(jig_w,jig_h,4,base);
    translate([pocket_x,pocket_y,base-pocket_depth])
        rounded_plate(pocket_w,pocket_h,3.2,pocket_depth+0.1);
    for (x=service_pad_x)
        translate([pocket_x+board_offset+x,
                   pocket_y+board_offset+pad_y,-0.1])
            cylinder(d=pin_bore_d,h=base+0.2);
    // Lead exit points away from the earring.
    translate([12,-0.1,1]) cube([14,6,3]);
}

// A shallow locator references the off-centre hook hole. Omit if the
// finished tray covers the hole; replace with a verified keyed contour.
translate([pocket_x+board_offset+13,
           pocket_y+board_offset+2.7,base-pocket_depth])
    cylinder(d=1.1,h=1.2);
