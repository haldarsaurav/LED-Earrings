// Rear tray study for one 26 x 42 mm PCB. Units: mm.
// Export an STL from OpenSCAD after adjusting measured hardware dimensions.
$fn = 48;
board_w = 26;
board_h = 42;
board_t = 0.8;
wall = 1.0;
base = 1.2;
cavity_depth = 6.8;
clearance = 0.25;
corner_r = 2.0;
hook_x = 13;
hook_y = 2.7;
hook_d = 1.5;
pad_y = 39.5;
pad_x = [4, 10, 16, 22]; // dock contacts first two; final two for UPDI + VTG

module rounded_plate(w, h, r, height) {
    linear_extrude(height=height)
        hull()
            for (x=[r, w-r], y=[r, h-r]) translate([x,y]) circle(r=r);
}

module tray() {
    difference() {
        translate([-wall,-wall,0])
            rounded_plate(board_w+2*wall, board_h+2*wall, corner_r+wall,
                          base+cavity_depth+board_t);
        // Rear component and cell cavity; board rests at its top edge.
        translate([-clearance,-clearance,base])
            rounded_plate(board_w+2*clearance,board_h+2*clearance,
                          corner_r+clearance,cavity_depth+board_t+1);
        // Mechanical hook passes through board and tray base.
        translate([hook_x,hook_y,-0.1]) cylinder(d=hook_d+0.6,h=base+0.2);
        // Rear pogo access wells. Verify diameter with actual contact tip.
        for (x=pad_x) translate([x,pad_y,-0.1]) cylinder(d=2.2,h=base+0.2);
        // Small bottom drainage/inspection slot, away from the battery.
        translate([9,-wall-0.1,1.5]) cube([6,wall+clearance+0.2,2]);
    }
    // Four flexible retention nibs; tune after the first print.
    for (x=[-0.15,board_w-0.55], y=[8,31])
        translate([x,y,base+cavity_depth]) cube([0.7,1.5,0.35]);
}

tray();
