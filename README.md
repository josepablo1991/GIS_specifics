# GIS_specifics

The well-known simplification algorithm can easily be modified to work solely on the z component. After this transformation we can rely on a standard implementation of the DP algorithm and mark those vertices which the algorithm will normally drop along the line. In these drop cases the elevation could in a follow-on step be replaced by a linearly interpolated value for a smoother z development. Furthermore 3D-features can be simplified in respect to vertices that show little variation in z.
