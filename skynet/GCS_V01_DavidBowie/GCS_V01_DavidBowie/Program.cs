/**
 * Authors: Larson Dean Brandstetter, Adam Wulfing
 * Version: 0.1 "David Bowie"
 * Date: 7/24/2020
 * 
 * This software is designed for the ground station prototype designed by Chad Dunbar
 * Final Version to be adjusted for future considerations and projects
 * TO DO:
 *      -Separate Menu Display and Tracking Display, threading
 *      -Display Current GPS and Iridium Data
 *      -Display Targeting Data
 *      -Adjust Delays for Targeting
 *      -Create Methods to contain connections and variables
 *      -Create Cutdown Command
 *      -Thread Tracker to allow for user input during tracking
 *      -Prepare code for a distributalbe version to be named (potentially: "MSGC Universal Tracking Software", "BOBCATS" acronym?)
 *          -Change Outputs to Degrees to allow use with various microcontrollers/motors
 *          -Allow for user input to connect to independent MySQL servers
 *          -Show names of devices connected on COM ports
 *          -Live Video/Imaging
 *          
 *          
 */

using System;
using System.IO.Ports;
using System.Threading;
using System.Threading.Tasks;
using System.Data.SqlClient;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.Sql;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Runtime.CompilerServices;
//using System.Windows.Forms;
using MySql.Data.MySqlClient;



namespace GCS_V01_DavidBowie
{
    class Program
    {

        static SerialPort _serialPort;
        static bool _continue;
        static void Main(string[] args)
        {
            Console.WriteLine("David Bowie Ground Station");
            Console.WriteLine("Connecting to Arduino...");
            // Finding COM port associated with the Arduino Uno

            //_serialPort = new SerialPort();

            String s;
            long j = 0;
            int flag;
            string[] COMPORTS;
            string SELECTEDCOM = "";
            int k;



            while (true)
            {
                Console.WriteLine("Searching Ports...");
                while (true)
                {
                    int i = 1;
                    string[] ports = SerialPort.GetPortNames();
                    foreach (string port in ports)
                    {
                        Console.WriteLine(i + ": " + port);
                        i++;
                    }
                    COMPORTS = ports;
                    k = i;
                    if (i != 1)
                    {
                        break;
                    }
                }
                Console.Write("Select Port from List: ");
                s = Console.ReadLine();
                try
                {
                    j = Int64.Parse(s);
                }
                catch (FormatException)
                {
                    Console.WriteLine("Must be a number from the list, try again.");
                    goto COMINPUT;
                }
                flag = 0;
                switch (j)
                {
                    case 1:
                        if (k > 1)
                        {
                            Console.WriteLine(COMPORTS[0] + " SELECTED");
                            SELECTEDCOM = COMPORTS[0];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    case 2:
                        if (k > 2)
                        {
                            Console.WriteLine(COMPORTS[1] + " SELECTED");
                            SELECTEDCOM = COMPORTS[1];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    case 3:
                        if (k > 3)
                        {
                            Console.WriteLine(COMPORTS[2] + " SELECTED");
                            SELECTEDCOM = COMPORTS[2];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    case 4:
                        if (k > 4)
                        {
                            Console.WriteLine(COMPORTS[3] + " SELECTED");
                            SELECTEDCOM = COMPORTS[3];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    case 5:
                        if (k > 5)
                        {
                            Console.WriteLine(COMPORTS[4] + " SELECTED");
                            SELECTEDCOM = COMPORTS[4];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    case 6:
                        if (k > 6)
                        {
                            Console.WriteLine(COMPORTS[5] + " SELECTED");
                            SELECTEDCOM = COMPORTS[5];
                        }
                        else
                        {
                            goto default;
                        }
                        break;
                    default:
                        flag = 1;
                        Console.WriteLine("COM Port is not available, Please try again");
                        break;
                }
                if (flag == 0)
                {
                    break;
                }
                COMINPUT:;
            }

            // Connecting to Arduino
            Thread readThread = new Thread(Read);

            _serialPort = new SerialPort();
            _serialPort.PortName = SELECTEDCOM;
            _serialPort.BaudRate = 9600;

            _serialPort.Open();
            _continue = true;


            double lat = 0, lon = 0, alt = 0, bear = 0, sun = 0, blat = 0, blon = 0, balt = 0, dlat = 0, dlon = 0, x = 0, y = 0, az = 0, elev = 0, dist = 0, los = 0;
            int azstep = 0, elevstep = 0, bearstep = 0, sunstep = 0;
            String iridium = "300234065065560";

            Console.Write("ENTER LAT: ");
            lat = Convert.ToDouble(Console.ReadLine());
            Console.Write("ENTER LON: ");
            lon = Convert.ToDouble(Console.ReadLine());
            Console.Write("ENTER ALT: ");
            alt = Convert.ToDouble(Console.ReadLine());


            // Input Center Bearing from Sun Table
            Console.Write("ENTER BEAR: ");
            bear = Convert.ToDouble(Console.ReadLine());
            Console.Write("ENTER SUN ELEV: ");
            sun = Convert.ToDouble(Console.ReadLine());
            Console.Write("ENTER IMEI: ");
            iridium = Console.ReadLine();


            // Tracking Loop
            int dispcount = 0;
            while (true)
            {
                // Get Irridium Information
                String serv = @"Data Source=eclipse.rci.montana.edu; Initial Catalog=freemanproject; User Id=antenna; Password=tracker";
                //SqlConnection sqlCon = new SqlConnection(iridium);
                using var con = new MySqlConnection(serv);
                {
                    String queryString = "select gps_fltDate,gps_time,gps_lat,gps_long,gps_alt from gps where gps_IMEI = " + iridium + " order by pri_key DESC LIMIT 1";
                    con.Open();
                    using var cmd = new MySqlCommand(queryString, con);
                    using MySqlDataReader rdr = cmd.ExecuteReader();
                    while (rdr.Read())
                    {
                        //Console.WriteLine(rdr.GetString(0) + rdr.GetString(1) + rdr.GetString(2) + rdr.GetString(3) + rdr.GetString(4));
                        blat = Convert.ToDouble(rdr.GetString(2));
                        blon = Convert.ToDouble(rdr.GetString(3));
                        balt = Convert.ToDouble(rdr.GetString(4));
                    }
                    con.Close();

                }
                //iridServConn(serv,iridium);

                // Calculate Balloon Azmuth
                dlat = ToRad(blat - lat);
                dlon = ToRad(blon - lon);
                y = Math.Sin(dlon) * Math.Cos(ToRad(blat));
                x = Math.Cos(ToRad(lat)) * Math.Sin(ToRad(blat)) - Math.Sin(ToRad(lat)) * Math.Cos(ToRad(blat)) * Math.Cos(dlat);
                az = ToDeg(Math.Atan2(y, x));

                // Calculate Balloon Elevation
                dist = haversine(lat, lon, blat, blon);
                elev = ToDeg(Math.Atan2(balt - alt, dist));
                los = lineofsight(balt, alt, dist);

                // Output to Arduino
                //Converting 360 circle to + and - 180 circle
                /*if (az > 0 && az < 180)
                {
                    azstep = Convert.ToInt32(az * 1137.778);
                }
                else if(az >= 180 && az < 360)
                {
                    az = (az - 180);
                    azstep = -(Convert.ToInt32(az * 1137.778));
                    Console.WriteLine(azstep);
                }
                if (elev > 0 && elev < 180)
                {
                    elevstep = Convert.ToInt32(elev * 1137.778);
                }
                else if (elev >= 180 && elev < 360)
                {
                    elev = (elev - 180);
                    elevstep = -(Convert.ToInt32(elev * 1137.778));
                    Console.WriteLine(elevstep);
                }
                if (sun > 0 && sun < 180)
                {
                    sunstep = Convert.ToInt32(sun * 1137.778);
                }
                else if (sun >= 180 && sun < 360)
                {
                    sun = (sun - 180);
                    sunstep = -(Convert.ToInt32(sun * 1137.778));
                }*/
                if (bear >= 0 && bear < 180)
                {
                    bearstep = Convert.ToInt32(bear * 1137.778);
                }
                else if (bear >= 180 && bear < 360)
                {
                    bear = (bear - 360);
                    bearstep = (Convert.ToInt32(bear * 1137.778));
                }
                azstep = (Convert.ToInt32((az - 5) * 1137.778));
                elevstep = Convert.ToInt32((elev + 5) * 1137.778);
                //bearstep = Convert.ToInt32(bear * 1137.778);
                sunstep = Convert.ToInt32(sun * 1137.778);
                //Console.WriteLine("AZIMUTH: " + az);
                //Console.WriteLine("ELEVATION: " + elev);
                //Console.WriteLine("LOS: " + los);
                if (dispcount == 0)
                {
                    Console.Write("bearing: " + bear);
                    Console.WriteLine(" BEAR: " + bearstep);
                    _serialPort.WriteLine("B" + bearstep);
                    dispcount = 1;
                    var t = Task.Run(async delegate
                    {
                        await Task.Delay(2000);
                        return 42;
                    });
                    t.Wait();
                }
                else if (dispcount == 1)
                {
                    Console.Write("sun elevation" + sun);
                    Console.WriteLine(" SUN: " + sunstep);
                    _serialPort.WriteLine("S" + sunstep);
                    dispcount = 2;
                    var t = Task.Run(async delegate
                    {
                        await Task.Delay(2000);
                        return 42;
                    });
                    t.Wait();
                    while (true)
                    {
                        Console.Write("Press Enter To Track: ");
                        String startT = Console.ReadLine();
                        break;
                    }
                }
                else if (dispcount == 2)
                {
                    Console.Write("azimuth" + az);
                    Console.WriteLine(" STEPAZ: " + azstep);
                    _serialPort.WriteLine("P" + azstep);
                    dispcount = 3;
                    var t = Task.Run(async delegate
                    {
                        await Task.Delay(8000);
                        return 42;
                    });
                    t.Wait();
                }
                else if (dispcount == 3)
                {
                    Console.Write("elevation" + elev);
                    Console.WriteLine(" STEPELEV: " + elevstep);
                    _serialPort.WriteLine("T" + elevstep);
                    dispcount = 2;
                    var t = Task.Run(async delegate
                    {
                        await Task.Delay(8000);
                        return 42;
                    });
                    t.Wait();
                }
            }


            Console.ReadLine();
        }
        public static void Read()
        {
            while (_continue)
            {
                try
                {
                    string message = _serialPort.ReadLine();
                    Console.WriteLine(message);
                }
                catch (TimeoutException) { }
            }
        }
        public static double ToRad(double val)
        {
            return (Math.PI / 180) * val;
        }
        public static double ToDeg(double val)
        {
            return (180 / Math.PI) * val;
        }
        public static double haversine(double lat, double lon, double blat, double blon)
        {
            double R = 6371;
            double dlat = ToRad(blat - lat);
            double dlon = ToRad(blon - lon);
            double a = Math.Sin(dlat / 2) * Math.Sin(dlat / 2) + Math.Cos(ToRad(lat)) * Math.Cos(ToRad(blat)) * Math.Sin(dlon / 2) * Math.Sin(dlon / 2);
            double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
            double d = R * c;

            return d * 3280.839895;
        }
        public static double lineofsight(double balt, double alt, double dist)
        {
            double dalt = balt - alt;
            double num = 3.2808;
            return Math.Sqrt(Math.Pow(dist / num, 2) + Math.Pow(dalt / num, 2)) / 1000;
        }
        private void iridServConn(String connectionString, String IMEI)
        {


        }
    }
}
