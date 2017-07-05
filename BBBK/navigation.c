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

#define Not_On_Path -2
#define left -1
#define straight 0
#define right 1
#define End_Destination 2
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

struct points {
    double lat;
    double lng;
};

////////////////////////////////
struct gps getGPS(void);
//void SendMyoDirection(int direction);
struct dist_bearing FindDistance(double latHome, double lonHome, double latDest, double lonDest);
void Navigation(struct points struct_array[], int size);
struct coord_and_bearing NextCoordinate(struct points struct_array[], int size, int coord_done, int coord_position);
struct coord_and_bearing GetBearing(double next_lat, double next_lng);
int GetDirection(struct points path_coord[], int size, int index);
///////////////////////////////



int main(void) {

    struct points *array = malloc(10 * sizeof (struct points));

    FILE *fp;
    fp = fopen ("vertices.csv", "r");
    int index = 0;
    while( fscanf(fp, "%lf %lf", &array[index].lat, &array[index].lng) == 2 )
      index++;

    Navigation(array, index);

    fclose(fp);


  return 0;
}

struct gps getGPS(void) {

    struct gps tmp;
	//printf("Getting GPS\n");
    system("./GetGPSData > user_loc.txt");
	//printf("Got GPS\n");
    FILE *fp;

    fp = fopen ("user_loc.txt", "r");

    if(fp == NULL) {
        perror("Failed to open user_location.txt file");
        tmp.lat = -1;
        tmp.lng = -1;
        tmp.timestamp = -1;
    }

    else {

        fscanf(fp, "%lf %lf %d", &tmp.lat, &tmp.lng, &tmp.timestamp);
	printf("%lf %lf %d\n", tmp.lat, tmp.lng, tmp.timestamp);
    }

    fclose(fp);


    return tmp;
}

//void SendMyoDirection(int direction) {
//    char minustwo[] = "python myoband.py -2"; //not on path
//    char minusone[] = "python myoband.py -1"; //take a left
//    char zero[]     = "python myoband.py 0"; //go straight
//    char one[]      = "python myoband.py 1"; //take a right
//    char two[]      = "python myoband.py 2"; //reached destination
//
//    if(direction == -2) {
//        system(minustwo);
//    }
//
//    else if(direction == -1) {
//        system(minusone);
//    }
//
//    else if(direction == 0) {
//        system(zero);
//    }
//
//    else if(direction == 1) {
//        system(one);
//    }
//
//    else if(direction == 2) {
//        system(two);
//    }
//
//
//}


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
    

    int index;
    int direction;
    int counter = 0;
    int counter1 = 0;
    int counter2 = 0;

    //find next coordinate based on users location
    repeat_next_coordinate:


    next_coordinate = NextCoordinate( path_coord, size, 0, -1);
    printf("Start here:\n");
        //if gps coordinate is not valid then keep retrying until we get good gps value
    if(next_coordinate.index == -500) {
        printf("Error could not calculate next vertice retrying to get valid user coordinate location\n");
        sleep(10);
        counter = counter + 1;

        if(counter > 10000) {
            printf("ended function here 1\n");
            //SendMyoDirection(Not_On_Path);
            return;
        }

        goto repeat_next_coordinate;
    }

    //got a good coordinate so now continue
    else {
        printf("closest coordinate %lf %lf coordinate number %d out of total index %d\n", next_coordinate.lat, next_coordinate.lng, next_coordinate.index, size-1 );

        expected_bear = next_coordinate.bear;

        //sleep(1);
        CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); // returns current location and current bearing

        //if bearing out of tolerance then report user as lost
        if((CaB.bear - expected_bear) > tolerance) {
            //SendMyoDirection(Not_On_Path);
            printf("user lost, bearing out of range ended function here 2\n");
            return;
            //exit
        }

       //if bearing within tolerance
        else {
            printf("Within bearing\n"); 
            check_again:

                //sleep(1);
                CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); // returns current location and current bearing
                if(CaB.lat == 0 && CaB.lng == 0) {
                    counter1 = counter1 + 1;

                    if(counter1  > 10000) {
                        //SendMyoDirection(Not_On_Path);
                        printf("ended function here 3\n");
                        return; //exit function
                    }

                    goto check_again;
                }

                printf(" 2. %lf %lf  and next coordinate %lf %lf go to vertice # %d \n", CaB.lat, CaB.lng, next_coordinate.lat, next_coordinate.lng, next_coordinate.index-1 );
                //check distance between current and next coord
                get_d_b = FindDistance(CaB.lat, CaB.lng, next_coordinate.lat, next_coordinate.lng);
                printf("3. distance is %lf\n", get_d_b.dist);
                //if further than 10 meters away check user location and if he is on path ie bearing
                if(get_d_b.dist > 20) {
                    printf(" 4a. More than 20m from next vertice\n");
                    repeat_again_if_not_good_gps:

                        CaB = GetBearing(next_coordinate.lat, next_coordinate.lng); //contains current coordinate and bearing to dest point

                        if(CaB.lat == 0 && CaB.lng == 0) {
                            counter2 = counter2 + 1;

                            if(counter2  > 10000) {
                                //SendMyoDirection(Not_On_Path);
                                printf("ended function here 4\n");
                                return; //exit function
                            }

                            goto repeat_again_if_not_good_gps;
                        }

                        get_d_b = FindDistance(CaB.lat, CaB.lng, next_coordinate.lat, next_coordinate.lng);

                        if((CaB.bear - expected_bear) > tolerance) {
                            //SendMyoDirection(Not_On_Path);
                             printf("user lost, bearing out of range \n");
                            return;
                        }
                    printf("4b. Within bearing 2\n");
                    goto check_again;

                }

                //once close enough to next coordinate signal user whether to go straight left or right
                else {
                printf(" 5. Within 20 m to next vertice\n");
                
                    //signal user if his next coordinate is not destination point
                    if(next_coordinate.index < (size-1) ) {//if not end point index then find next coord using next index
                        index = next_coordinate.index + 1;

                        //lat3 = path_coord[index].lat;
                        //lng3 = path_coord[index].lng;

                        //spits out direction
                        //0 = straight 1 = left 2 = right
                        direction = GetDirection(path_coord, size, next_coordinate.index);

                        if(direction == 0) {
                            //SendMyoDirection(straight);
                            printf("go straight nav \n");
                        }

                        else if(direction == -1) {
                            //SendMyoDirection(left);
                            printf("take a  left in less than 10 meters nav \n");
                        }

                        else if(direction == 1) {
                            //SendMyoDirection(right);
                            printf("take a right in less than 10 meters nav \n");
                        }
                    }

                    //might be unable to match exact user gps location to that of final coordinate
                    //so just check if distance is small enough to see if user is close to the point


                    if(get_d_b.dist <= 10) {//if within 1 meters to destination assume reached ie last point on map
                        printf("Within 10m to vertice and index is %d\n", next_coordinate.index);
                        if(next_coordinate.index == size - 1){
                        printf("reached destination leave from navigation.c function here \n"); //reached end destination
                        //SendMyoDirection(End_Destination);
                        return;
                        }

                        else {

                            printf("reached vertice, calculating next vertice, follow ur given direction as posted above previously\n"); //reached one of the vertice coordinate
                            next_coordinate = NextCoordinate(path_coord, size, 1, next_coordinate.index);

                            //sleep(1);
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
        int dex = -500;
        int ignore;
        int max = -1;

        double lat, lng;
        double bear = -500;
        double next_lat = -500, next_lng = -500; //-500 treated as null
        double smallest_d = 1000000;


        current_coordinate = getGPS(); //gets current user location from sensor group
	printf("Got GPS Next co-ordinate from NextCoordinate function\n");
        //if zero the gps coordinates are invalid
        if(current_coordinate.lat == 0 && current_coordinate.lng == 0) {
            tmp.lat = -500;
            tmp.lng = -500;
            tmp.bear = -500;
            tmp.index = -500;
            return tmp;
        }

        //if good gps coordinate
        //global_iteration_remove = global_iteration_remove + 1;

        ignore = 0;

        if(coord_done == 1) {
            ignore_paths[num] = coord_position;
            num = num + 1;

            tmp.lat = -499; //useless data
            tmp.lng = -499;
            tmp.bear = -499;
            tmp.index = -499;

            return tmp;

        }

        //find highest vertice index the user has reached so far
        for(i=0; i<num; i++) {
            if(max < ignore_paths[i]) {
                max = ignore_paths[i];
            }
        }

        if(coord_done == 0) {
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
                if( (get_d_b.dist < smallest_d) && (ignore == 0) && (i > max)  ) {

                    smallest_d = get_d_b.dist;
                    next_lat = lat;
                    next_lng = lng;
                    bear = get_d_b.bear;
                    dex = i;

                }

                ignore = 0;
            }



            if(next_lat != -500 && next_lng != -500) {
                tmp.lat = next_lat;
                tmp.lng = next_lng;
                tmp.bear = bear;
                tmp.index = dex;

               printf("user location %lf %lf %d closest index is %d from NextCoordinate\n", current_coordinate.lat, current_coordinate.lng, current_coordinate.timestamp, tmp.index);
                return tmp;
            }



            //if no next_coordinate is found
            else {
                printf(" should exit file, error next vertice could not be calculated using -500 line 366 coord_and_bearing \n" );
                //exit
                tmp.lat = -1000;
                tmp.lng = -1000;
                tmp.bear = 0;
                tmp.index = -999;

                return tmp;
            }
        }

        return tmp;

}


struct coord_and_bearing GetBearing(double next_lat, double next_lng) { //returns current user location and bearing

    struct coord_and_bearing tmp;
    struct gps current_coordinate;
    struct dist_bearing get_d_b;



    current_coordinate = getGPS();
    //printf("Got GPS co-ordinate from GetBearing\n");

 //gets current user location from sensor group
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
int GetDirection(struct points path_coord[], int size, int index) {

    int tmp;
    
    struct points before;
    struct points to;
    struct points after;
    
    struct dist_bearing from_d_b;
    struct dist_bearing to_d_b;
    
    double difference;
    
    double min_tolerance, max_tolerance; //can be changed depending on how sharp the turns are

    min_tolerance = 55;
    max_tolerance = 125;
    
    if(index == (size-1) || index == 0) { //if at beginning point or last end point
                                        //just tell user to go straight
            tmp = 0; //tell user to just go straight
            return tmp;

    }
    
    else {
    
        before = path_coord[index - 1];
        to = path_coord[index];
        after = path_coord[index + 1];
        
        from_d_b = FindDistance(before.lat, before.lng, to.lat, to.lng);
        to_d_b = FindDistance(to.lat, to.lng, after.lat, after.lng);
        
        printf("user bear = %lf, next point bear = %lf \n", from_d_b.bear, to_d_b.bear);

        difference = to_d_b.bear - from_d_b.bear;
        
        if(difference >= min_tolerance && difference <= max_tolerance) {
            printf("tmp = 1, take a right\n");
            tmp = 1; //right
        }
        
        else if(difference >= -max_tolerance && difference <= -min_tolerance) { //between -125 and -55 its left
            printf("tmp = -1 take a left\n");
            tmp = -1; //left

        }
        
        else { //straight
            printf("tmp = 0 take a straight\n");
            tmp = 0;
        }
        
        return tmp;
    }
    
}
