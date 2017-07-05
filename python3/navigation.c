//
//  main.c
//  592
//
//  Created by Diwakar Posam on 4/25/17.
//  Copyright © 2017 Diwakar Posam. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
 
#define R 6371
#define TO_RAD (3.1415926536 / 180)


struct gps {
    double lat;
    double lng;
    int timestamp; //whats the units for this time value
};

struct coord_and_bearing {
    double lat;
    double lng;
    double bear;
    int index;
};

struct dist_bearing{
    double dist;
    double bear;
};

struct points{
    double lat;
    double lng;
};

////////////////////////////////
struct points* cmd_to_points(int argc, char *argv[]);
struct gps example_get_func(void);
struct dist_bearing FindDistance(double latHome, double lonHome, double latDest, double lonDest);
void Navigation(struct points struct_array[], int size);
struct coord_and_bearing NextCoordinate(struct points struct_array[], int size, int coord_done, int coord_position);
struct coord_and_bearing GetBearing(double next_lat, double next_lng);
int GetDirection(double bearing, double lat, double lng, double lat3, double lng3);
///////////////////////////////

int main(int argc, char *argv[]) {
    int num_of_coords = argc - 1;
    if (num_of_coords & 1) {
	printf("Warning: cmd line was given odd number of coordinates.\n");
	num_of_coords -= 1;
    }
    num_of_coords >>= 1;

    struct points *struct_array = cmd_to_points(num_of_coords, argv);

    Navigation(struct_array, num_of_coords);

    free(struct_array);
    return 0;

}


// Takes a list of float arguments passed through the command line (as characters)
// and turns it into an array of coords.
struct points* cmd_to_points(int num_of_coords, char *argv[]) {
    struct points* coords = malloc(num_of_coords * sizeof(struct points));


    for (int i = 0; i < num_of_coords; ++i) {
	coords[i].lat = atof(argv[(i<<1)+1]);
	coords[i].lng = atof(argv[(i<<1)+2]);
    }


    return coords;
}


struct gps example_get_func(void) {

    struct gps coordinate;
    
    coordinate.lat = 30.01;
    coordinate.lng = 35.01;
    coordinate.timestamp = 60;
    
    return coordinate;
}


struct dist_bearing FindDistance(double latHome, double lonHome, double latDest, double lonDest) {

        struct dist_bearing tmp;
 
      static const double pi_d180 = 3.1415926535897932384626433832795 / 180;
      static const double d180_pi = 180 / 3.1415926535897932384626433832795;

      //static const double R = 6371.0; // better to make FP to avoid the need to convert

      //Keep the parameters passed to the function immutable
      double latHomeTmp = pi_d180 * (latHome);
      double latDestTmp = pi_d180 * (latDest);
      double differenceLon = pi_d180 * (lonDest - lonHome);
      double differenceLat = pi_d180 * (latDest - latHome);

      double a = sin(differenceLat / 2.) * sin(differenceLat / 2.)
          + cos(latHomeTmp) * cos(latDestTmp) * sin(differenceLon / 2.)
              * sin(differenceLon / 2.);

      double c = 2 * atan2(sqrt(a), sqrt(1 - a));
      double Distance = R * c;
      tmp.dist = Distance*1000; // in meters

      double RadBearing = atan2(sin(differenceLon) * cos(latDestTmp),
          cos(latHomeTmp) * sin(latDestTmp)
              - sin(latHomeTmp) * cos(latDestTmp) * cos(differenceLon));

      double DegBearing = RadBearing * d180_pi;

//      if (DegBearing < 0) DegBearing = 360 + DegBearing;
    
      tmp.bear = DegBearing;
      
      return tmp;
}


void Navigation(struct points path_coord[], int size) {

    struct coord_and_bearing next_coordinate; //next coordinate and expected bearing
    struct coord_and_bearing CaB; //current coordinate and current bearing
    struct dist_bearing get_d_b; //distance and bearing
    
    double expected_bear;
    double tolerance = 100;
    double lat3, lng3;
    
    int index;
    int direction;
    
    
    
    repeat_next_coordinate:

    next_coordinate = NextCoordinate( path_coord, size, 0, -1);
    
    //find the point after next_coordinate
    //need it to calculate direction
    
    if(next_coordinate.index == -1000) {
        printf("user is at destination ");
        //exit
    }
    
    else if(next_coordinate.index == -999) {
        printf("error could not calculate next vertice");
        //exit
    }
    
    else {
        printf("closest coordinate: %lf %lf gotten from map\n", next_coordinate.lat, next_coordinate.lng);
    
        expected_bear = next_coordinate.bear;
        
        sleep(1);
        CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); // returns current location and current bearing
        
        //if bearing out of tolerance then report user as lost
        if((CaB.bear - expected_bear) > tolerance) {
            printf("user lost, bearing out of range");
            //exit
        }
        
        //if bearing within tolerance
        else {
            
            check_again:
            
                sleep(1);
                CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); // returns current location and current bearing

                //check distance between current and next coord
                get_d_b = FindDistance(CaB.lat, CaB.lng, next_coordinate.lat, next_coordinate.lng);
            
                if(get_d_b.dist > 10) {
                
                    next_coordinate = NextCoordinate( path_coord, size, 0, -1);
                    
                    if(next_coordinate.lat == -1000 && next_coordinate.lng == -1000) {
                        printf("user is at destination ");
                    }
                    
                    else {
                    
                        CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); //contains current coordinate and bearing to dest point
                        
                        if((CaB.bear - expected_bear) > tolerance) {
                            printf("user lost, bearing out of range");
                            //exit
                        }
                        
                        else {
                            get_d_b = FindDistance(CaB.lat, CaB.lng, next_coordinate.lat, next_coordinate.lng);
                        }
                    goto check_again;
                    }
                
                }
            
                //once close enough to next coordinate signal user whether to go straight left or right
                else {
                    //signal user
                    if(next_coordinate.index < (size-1) ) {//if not end point index then find next coord using next index
                        index = next_coordinate.index + 1;
    
                        lat3 = path_coord[index].lat;
                        lng3 = path_coord[index].lng;
        
                        //spits out direction
                        //0 = straight 1 = left 2 = right
                        direction = GetDirection( next_coordinate.bear, next_coordinate.lat, next_coordinate.lng, lat3, lng3 );
    
                        if(direction == 0) {
                            printf("go straight  \n");
                        }
        
                        else if(direction == 1) {
                            printf("take a  left in less than 10 meters \n");
                        }
        
                        else if(direction == 2) {
                            printf("take a right in less than 10 meters \n");
                        }
                    }
                    
                    //might be unable to match exact user gps location to that of final coordinate
                    //so just check if distance is small enough to see if user is close to the point
                    if(get_d_b.dist <= 1) {//if within 1 meters to destination assume reached
                        if(next_coordinate.index == size - 1){
                        printf("reached destination, navigation ends here"); //reached end destination
                        //EXIT FUNCTION****************************************************************
                        }
                        
                        else {
                            printf("reached coordinate, calculating next coordinate"); //reached one of the vertice coordinate
                            next_coordinate = NextCoordinate(path_coord, size, 1, next_coordinate.index);
                            sleep(1);
                            goto repeat_next_coordinate;
                            
                        }
                    }
                    
                    else {

                        goto check_again;
                        
                    }
                    
                }
        }
            
    }
    
}

//argument is full pathing coordinating list and its size
struct coord_and_bearing NextCoordinate (struct points path_coord[], int size, int coord_done, int coord_position) { //returns next destination point and expected bearing

        static int ignore_paths[50];
        static int num = 0;
    
        struct gps current_coordinate;
        struct coord_and_bearing tmp;
        struct dist_bearing get_d_b;
    
        int i, k;
        int dex;
        int ignore;
    
        double lat, lng, bear;
        double next_lat, next_lng;
        double smallest_d = 1000000;
    
    
        current_coordinate = example_get_func(); //gets current user location from sensor group
    
        ignore = 0;
    
        if(coord_done == 1) {
            ignore_paths[num] = coord_position;
            num = num + 1;
        }
    
        //finds closest mapped coordinate to users location
        for( i = 0; i < size; i++) {
        
            lat = path_coord[i].lat;
            lng = path_coord[i].lng;
            
            get_d_b = FindDistance(current_coordinate.lat, current_coordinate.lng, lat, lng);
            
            //checks to see if the coordinate is behind the user
            //set ignore flag high if the coordinate is already passed by user
            for(k = 0; k<num; k++) {
                if(i==ignore_paths[k]) {
                    ignore = 1;
                    break;
                }
            }
        
        
            //ignore vertice i have already reached
            if( (get_d_b.dist < smallest_d) && (ignore == 0) ) {
            
                smallest_d = get_d_b.dist;
                next_lat = lat;
                next_lng = lng;
                bear = get_d_b.bear;
                dex = i;

            }
            
            ignore = 0;
        }
    
    
    
        if(next_lat != 0 && next_lng != 0) { //should be NULL FIX AT END*******************************
            tmp.lat = next_lat;
            tmp.lng = next_lng;
            tmp.bear = bear;
            
            if(dex == (size-1) ) {//checking if the point is the last point in array on the path
                tmp.index = -1000; //already at last point dont need to look at index anymore
            }
            
            else {
                tmp.index = dex;
            }
            
            return tmp;
        }
    

    
        //if no next_coordinate is found
        else {
            printf(" error next vertice could not be calculated" );
            //exit
            tmp.lat = -1000;
            tmp.lng = -1000;
            tmp.bear = 0;
            tmp.index = -999;
            
            return tmp;
            
        }
}

struct coord_and_bearing GetBearing(double next_lat, double next_lng) { //returns current user location and bearing

    struct coord_and_bearing tmp;
    struct gps current_coordinate;
    struct dist_bearing get_d_b;
    
    current_coordinate = example_get_func(); //gets current user location from sensor group
    get_d_b = FindDistance(current_coordinate.lat, current_coordinate.lng, next_lat, next_lng);
    
    tmp.lat = current_coordinate.lat;
    tmp.lng = current_coordinate.lng;
    tmp.bear = get_d_b.bear;
    tmp.index = -1000;
    
    return tmp;
    
    
}

//0 = straight 1 = left 2 = right
//takes in current bearing from user location to next coordinate
//takes in next coordinate
//takes in the coordinate after next coordinate
int GetDirection(double bear, double lat, double lng, double lat3, double lng3) {

    int tmp;
    struct dist_bearing get_d_b;
    double difference;
    double min_tolerance, max_tolerance; //can be changed depending on how sharp the turns are
    
    min_tolerance = 55;
    max_tolerance = 125;
    
    get_d_b = FindDistance(lat, lng, lat3, lng3);
    
    difference = bear - get_d_b.bear;
    
    if(difference >=  min_tolerance && difference <= max_tolerance) {
        tmp = 2; //right
    }
    
    else if(difference >= -max_tolerance && difference <= -min_tolerance) { //between -125 and -55 its left
        tmp = 1; //left
    }
    
    else {
        tmp = 0; //straight
    }
    
    return tmp;
}
