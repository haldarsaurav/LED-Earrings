// Two-pocket desk dock fit study. A separate USB-C PCB and real pogo pins are required.
// Board/case dimensions refer to earring_tray.scad. Units: mm.
$fn = 48;
dock_w = 74;
dock_h = 58;
dock_t = 10;
corner_r = 5;
pocket_w = 26.6;
pocket_h = 40.6;
pocket_depth = 2.3;
pocket_left = [5.4, 42.0];
pocket_bottom = 8.7;
board_origin_offset = 1.3; // board origin relative to pocket outer edge
pad_x = [5, 12, 19];
pad_y = 36;

module rounded_plate(w,h,r,depth) {
    linear_extrude(height=depth)
        hull() for (x=[r,w-r],y=[r,h-r]) translate([x,y]) circle(r=r);
}

difference() {
    rounded_plate(dock_w,dock_h,corner_r,dock_t);
    for (left=pocket_left) {
        translate([left,pocket_bottom,dock_t-pocket_depth])
            rounded_plate(pocket_w,pocket_h,3.3,pocket_depth+0.1);
        // Two spring-pin bores in each pocket. NO UPDI contact in gift dock.
        // Pin body diameter and protrusion must be changed to purchased pins.
        for (x=[pad_x[0],pad_x[1]])
            translate([left+board_origin_offset+x,
                       pocket_bottom+board_origin_offset+pad_y,-0.1])
                cylinder(d=1.8,h=dock_t+0.2);
    }
    // Internal wire space under the two pockets. Connect both chargers to
    // one correctly rated 5 V USB-C input on a SEPARATE dock PCB.
    translate([11,22,-0.1]) cube([52,15,4.1]);
    // Rear cable exit; adjust to selected USB-C connector.
    translate([31,dock_h-6,0]) cube([12,7,5]);
}

// Decorative raised wave: shallow enough to avoid touching pocket rims.
for (i=[0:11])
    translate([20+i*3,3.5+sin(i*22)*0.7,dock_t]) sphere(d=0.55);
