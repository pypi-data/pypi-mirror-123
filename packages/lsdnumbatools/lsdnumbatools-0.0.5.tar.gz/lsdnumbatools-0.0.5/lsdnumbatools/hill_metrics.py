import numba as nb
import numpy as np
import math as m
import lsdnumbatools as lsdnb

@nb.jit(nopython = True,cache = True)
def hillshading(arr,dx,dy,ncols,nrows,HSarray,zenith_rad,azimuth_rad, z_factor):
  """
  Slow and basic imnplementation of the hillshading algorithm present in LSDTT c++ algorithmath.
  This is basically just to train myself before optimization/parrallelization with numba
  BG, from DAV-SWDG-SMM codes
  """

  for i in range(nrows):
    for j in range(ncols):

      if arr[i, j] != -9999:

        dzdx = (((arr[i, j+1] + 2*arr[i+1, j] + arr[i+1, j+1]) -
                (arr[i-1, j-1] + 2*arr[i-1, j] + arr[i-1, j+1]))
                / (8 * dx))
        dzdy = (((arr[i-1, j+1] + 2*arr[i, j+1] + arr[i+1, j+1]) -
                (arr[i-1, j-1] + 2*arr[i, j-1] + arr[i+1, j-1]))
                / (8 * dy))

        slope_rad = np.arctan(z_factor * np.sqrt((dzdx * dzdx) + (dzdy * dzdy)))

        if (dzdx != 0):
          aspect_rad = np.arctan2(dzdy, (dzdx*-1))
          if (aspect_rad < 0):
            aspect_rad = 2 * np.pi + aspect_rad

        else:
          if (dzdy > 0):
            aspect_rad = np.pi / 2
          elif (dzdy < 0):
            aspect_rad = 2 * np.pi - np.pi / 2
          else:
            aspect_rad = aspect_rad

        HSarray[i, j] = 255.0 * ((np.cos(zenith_rad) * np.cos(slope_rad)) +
                        (np.sin(zenith_rad) * np.sin(slope_rad) *
                        np.cos(azimuth_rad - aspect_rad)))
        # Necessary?
        if (HSarray[i, j] < 0):
          HSarray[i, j] = 0



# the following function is 
# //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# // calculate_polyfit_surface_metrics
# //
# // This routine houses the code to fit a 6 term polynomial (z =ax^2 + by^2 + cxy
# // + dx + ey + f) to a surface, and then use the derivatives of this to
# // calculate various useful geometric properties such as slope and curvature.
# //
# // The surface is fitted to all the points that lie within circular
# // neighbourhood that is defined by the designated window radius.  The user also
# // inputs a binary raster, which tells the program which rasters it wants to
# // create (label as "true" to produce them, "false" to ignore them. This has 8
# // elements, as listed below:
# //        0 -> Elevation (smoothed by surface fitting)
# //        1 -> Slope
# //        2 -> Aspect
# //        3 -> Curvature
# //        4 -> Planform Curvature
# //        5 -> Profile Curvature
# //        6 -> Tangential Curvature
# //        7 -> Stationary point classification (1=peak, 2=depression, 3=saddle)
# // The program returns a vector of LSDRasters.  For options marked "false" in
# // boolean input raster, the returned LSDRaster houses a blank raster, as this
# // metric has not been calculated.  The desired LSDRaster can be retrieved from
# // the output vector by using the cell reference shown in the list above i.e. it
# // is the same as the reference in the input binary vector.
# //
# // DTM 28/03/2014
# //=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# vector<LSDRaster> LSDRaster::calculate_polyfit_surface_metrics(float window_radius, vector<int> raster_selection)
# {
#   Array2D<float> void_array(1,1,NoDataValue);
#   LSDRaster VOID(1,1,NoDataValue,NoDataValue,NoDataValue,NoDataValue,void_array,GeoReferencingStrings);

#   // catch if the supplied window radius is less than the data resolution and
#   // set it to equal the data resolution - SWDG
#   if (window_radius < sqrt(2)*DataResolution)
#   {
#     cout << "Supplied window radius: " << window_radius << " is less than the data resolution * sqrt(2), i.e. the diagonal of a single grid cell: " <<
#     sqrt(2)*DataResolution << ".\nWindow radius has been set to sqrt(2) * data resolution." << endl;
#     window_radius = sqrt(2)*DataResolution;
#   }
#   // this fits a polynomial surface over a kernel window. First, perpare the
#   // kernel
#   int kr = int(ceil(window_radius/DataResolution));  // Set radius of kernel
#   int kw=2*kr+1;                                     // width of kernel

#   Array2D<float> data_kernel(kw,kw,NoDataValue);
#   Array2D<float> x_kernel(kw,kw,NoDataValue);
#   Array2D<float> y_kernel(kw,kw,NoDataValue);
#   Array2D<int> mask(kw,kw,0);

#   // reset the a,b,c,d,e and f matrices (the coefficient matrices)
#   Array2D<float> temp_coef(NRows,NCols,NoDataValue);
#   Array2D<float> elevation_raster, slope_raster, aspect_raster, curvature_raster, planform_curvature_raster,
#                   profile_curvature_raster, tangential_curvature_raster, classification_raster,
#                   s1_raster, s2_raster, s3_raster;
#   // Copy across raster template into the desired array containers
#   if(raster_selection[0]==1)  elevation_raster = temp_coef.copy();
#   if(raster_selection[1]==1)  slope_raster = temp_coef.copy();
#   if(raster_selection[2]==1)  aspect_raster = temp_coef.copy();
#   if(raster_selection[3]==1)  curvature_raster = temp_coef.copy();
#   if(raster_selection[4]==1)  planform_curvature_raster = temp_coef.copy();
#   if(raster_selection[5]==1)  profile_curvature_raster = temp_coef.copy();
#   if(raster_selection[6]==1)  tangential_curvature_raster = temp_coef.copy();
#   if(raster_selection[7]==1)  classification_raster = temp_coef.copy();

#   //float a,b,c,d,e,f;

#   // scale kernel window to resolution of DEM, and translate coordinates to be
#   // centred on cell of interest (the centre cell)
#   float x,y,zeta,radial_dist;
#   for(int i=0;i<kw;++i)
#   {
#     for(int j=0;j<kw;++j)
#     {
#       x_kernel[i][j]=(i-kr)*DataResolution;
#       y_kernel[i][j]=(j-kr)*DataResolution;
#       // Build circular mask
#       // distance from centre to this point.
#       radial_dist = sqrt(y_kernel[i][j]*y_kernel[i][j] + x_kernel[i][j]*x_kernel[i][j]);

#       //if (floor(radial_dist) <= window_radius)
#       if (radial_dist <= window_radius)
#       {
#         mask[i][j] = 1;
#       }
#     }
#   }
#   // FIT POLYNOMIAL SURFACE BY LEAST SQUARES REGRESSION AND USE COEFFICIENTS TO
#   // DETERMINE TOPOGRAPHIC METRICS
#   // Have N simultaneous linear equations, and N unknowns.
#   // => b = Ax, where x is a 1xN array containing the coefficients we need for
#   // surface fitting.
#   // A is constructed using different combinations of x and y, thus we only need
#   // to compute this once, since the window size does not change.
#   // For 2nd order surface fitting, there are 6 coefficients, therefore A is a
#   // 6x6 matrix
#   Array2D<float> A(6,6,0.0);
#   for (int i=0; i<kw; ++i)
#   {
#     for (int j=0; j<kw; ++j)
#     {
#       if (mask[i][j] == 1)
#       {
#         x = x_kernel[i][j];
#         y = y_kernel[i][j];

#         // Generate matrix A
#         A[0][0] += pow(x,4);
#         A[0][1] += pow(x,2)*pow(y,2);
#         A[0][2] += pow(x,3)*y;
#         A[0][3] += pow(x,3);
#         A[0][4] += pow(x,2)*y;
#         A[0][5] += pow(x,2);
#         A[1][0] += pow(x,2)*pow(y,2);
#         A[1][1] += pow(y,4);
#         A[1][2] += x*pow(y,3);
#         A[1][3] += x*pow(y,2);
#         A[1][4] += pow(y,3);
#         A[1][5] += pow(y,2);
#         A[2][0] += pow(x,3)*y;
#         A[2][1] += x*pow(y,3);
#         A[2][2] += pow(x,2)*pow(y,2);
#         A[2][3] += pow(x,2)*y;
#         A[2][4] += x*pow(y,2);
#         A[2][5] += x*y;
#         A[3][0] += pow(x,3);
#         A[3][1] += x*pow(y,2);
#         A[3][2] += pow(x,2)*y;
#         A[3][3] += pow(x,2);
#         A[3][4] += x*y;
#         A[3][5] += x;
#         A[4][0] += pow(x,2)*y;
#         A[4][1] += pow(y,3);
#         A[4][2] += x*pow(y,2);
#         A[4][3] += x*y;
#         A[4][4] += pow(y,2);
#         A[4][5] += y;
#         A[5][0] += pow(x,2);
#         A[5][1] += pow(y,2);
#         A[5][2] += x*y;
#         A[5][3] += x;
#         A[5][4] += y;
#         A[5][5] += 1;
#       }
#     }
#   }

#   // Move window over DEM, fitting 2nd order polynomial surface to the
#   // elevations within the window.
#   //cout << "\n\tRunning 2nd order polynomial fitting" << endl;
#   //cout << "\t\tDEM size = " << NRows << " x " << NCols << endl;
#   int ndv_present = 0;

#   for(int i=0;i<NRows;++i)
#   {
#     //cout << "\tRow = " << i+1 << " / " << NRows << "    \r";
#     for(int j=0;j<NCols;++j)
#     {
#       // Avoid edges
#       if((i-kr < 0) || (i+kr+1 > NRows) || (j-kr < 0) || (j+kr+1 > NCols) || RasterData[i][j]==NoDataValue)
#       {
#         if(raster_selection[0]==1)  elevation_raster[i][j] = NoDataValue;
#         if(raster_selection[1]==1)  slope_raster[i][j] = NoDataValue;
#         if(raster_selection[2]==1)  aspect_raster[i][j] = NoDataValue;
#         if(raster_selection[3]==1)  curvature_raster[i][j] = NoDataValue;
#         if(raster_selection[4]==1)  planform_curvature_raster[i][j] = NoDataValue;
#         if(raster_selection[5]==1)  profile_curvature_raster[i][j] = NoDataValue;
#         if(raster_selection[6]==1)  tangential_curvature_raster[i][j] = NoDataValue;
#         if(raster_selection[7]==1)  classification_raster[i][j] = NoDataValue;
#       }
#       else
#       {
#       // clip DEM
#         //zeta_sampler=zeta.copy();
#         for(int i_kernel=0;i_kernel<kw;++i_kernel)
#         {
#           for(int j_kernel=0;j_kernel<kw;++j_kernel)
#           {
#             data_kernel[i_kernel][j_kernel] = RasterData[i-kr+i_kernel][j-kr+j_kernel];
#             // check for nodata values nearby
#             if(data_kernel[i_kernel][j_kernel]==NoDataValue)
#             {
#               ndv_present=1;
#             }
#           }
#         }
#         // Fit polynomial surface, avoiding nodata values
#         // ==================> Could change this,
#         // as can fit polynomial surface as long as there are 6 data points.
#         if(ndv_present == 0)  // test for nodata values within the selection
#         {
#           Array1D<float> bb(6,0.0);
#           Array1D<float> coeffs(6);
#           for (int krow=0; krow<kw; ++krow)
#           {
#             for (int kcol=0; kcol<kw; ++kcol)
#             {
#               if (mask[krow][kcol] == 1)
#               {
#                 x = x_kernel[krow][kcol];
#                 y = y_kernel[krow][kcol];
#                 zeta = data_kernel[krow][kcol];
#                 // Generate vector bb
#                 bb[0] += zeta*x*x;
#                 bb[1] += zeta*y*y;
#                 bb[2] += zeta*x*y;
#                 bb[3] += zeta*x;
#                 bb[4] += zeta*y;
#                 bb[5] += zeta;
#               }    // end mask
#             }      // end kernal column
#           }        // end kernal row
#           // Solve matrix equations using LU decomposition using the TNT JAMA
#           // package:
#           // A.coefs = b, where coefs is the coefficients vector.
#           LU<float> sol_A(A);  // Create LU object
#           coeffs = sol_A.solve(bb);

#           float a=coeffs[0];
#           float b=coeffs[1];
#           float c=coeffs[2];
#           float d=coeffs[3];
#           float e=coeffs[4];
#           float f=coeffs[5];

#           // Now calculate the required topographic metrics
#           if(raster_selection[0]==1)  elevation_raster[i][j] = f;

#           // note that the kernal translates coordinates so the derivative terms
#           // containing x or y go to zero because x = 0 and y = 0 in the transformed coordinates.
#           if(raster_selection[1]==1)  slope_raster[i][j] = sqrt(d*d+e*e);

#           if(raster_selection[2]==1)
#           {
#             if(d==0 && e==0) aspect_raster[i][j] = NoDataValue;
#             else if(d==0 && e>0) aspect_raster[i][j] = 90;
#             else if(d==0 && e<0) aspect_raster[i][j] = 270;
#             else
#             {
#               aspect_raster[i][j] = 270. - (180./M_PI)*atan(e/d) + 90.*(d/abs(d));
#               if(aspect_raster[i][j] > 360.0) aspect_raster[i][j] -= 360;
#             }
#           }

#           if(raster_selection[3]==1)  curvature_raster[i][j] = 2*a+2*b;

#           if(raster_selection[4]==1 || raster_selection[5]==1 || raster_selection[6]==1 || raster_selection[7]==1)
#           {
#             float fx, fy, fxx, fyy, fxy, p, q;
#             fx = d;
#             fy = e;
#             fxx = 2*a;
#             fyy = 2*b;
#             fxy = c;
#             p = fx*fx + fy*fy;
#             q = p + 1;

#             if (raster_selection[4]==1)
#             {
#               if (q > 0)  planform_curvature_raster[i][j] = (fxx*fy*fy - 2*fxy*fx*fy + fyy*fx*fx)/(sqrt(q*q*q));
#               else        planform_curvature_raster[i][j] = NoDataValue;
#             }
#             if(raster_selection[5]==1)
#             {
#               if((q*q*q > 0) && ((p*sqrt(q*q*q)) != 0))    profile_curvature_raster[i][j] = (fxx*fx*fx + 2*fxy*fx*fy + fyy*fy*fy)/(p*sqrt(q*q*q));
#               else                                         profile_curvature_raster[i][j] = NoDataValue;
#             }
#             if(raster_selection[6]==1)
#             {
#               if( q>0 && (p*sqrt(q))!=0) tangential_curvature_raster[i][j] = (fxx*fy*fy - 2*fxy*fx*fy + fyy*fx*fx)/(p*sqrt(q));
#               else                       tangential_curvature_raster[i][j] = NoDataValue;
#             }
#             if(raster_selection[7]==1)
#             {
#               float slope = sqrt(d*d + e*e);
#               if (slope < 0.1)
#               {
#                 if (fxx < 0 && fyy < 0 && fxy*fxy < fxx*fxx)      classification_raster[i][j] = 1;// Conditions for peak
#                 else if (fxx > 0 && fyy > 0 && fxy*fxy < fxx*fyy) classification_raster[i][j] = 2;// Conditions for a depression
#                 else if (fxx*fyy < 0 || fxy*fxy > fxx*fyy)        classification_raster[i][j] = 3;// Conditions for a saddle
#                 else classification_raster[i][j] = 0;
#               }
#             }
#           }
#         }         // end if statement for no data value
#         ndv_present = 0;
#       }
#     }
#   }
#   // Now create LSDRasters and load into output vector
#   vector<LSDRaster> output_rasters_temp(8,VOID);
#   vector<LSDRaster> raster_output = output_rasters_temp;
#   if(raster_selection[0]==1)
#   {
#     LSDRaster Elevation(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,elevation_raster,GeoReferencingStrings);
#     raster_output[0] = Elevation;
#   }
#   if(raster_selection[1]==1)
#   {
#     LSDRaster Slope(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,slope_raster,GeoReferencingStrings);
#     raster_output[1] = Slope;
#   }
#   if(raster_selection[2]==1)
#   {
#     LSDRaster Aspect(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,aspect_raster,GeoReferencingStrings);
#     raster_output[2] = Aspect;
#   }
#   if(raster_selection[3]==1)
#   {
#     LSDRaster Curvature(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,curvature_raster,GeoReferencingStrings);
#     raster_output[3] = Curvature;
#   }
#   if(raster_selection[4]==1)
#   {
#     LSDRaster PlCurvature(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,planform_curvature_raster,GeoReferencingStrings);
#     raster_output[4] = PlCurvature;
#   }
#   if(raster_selection[5]==1)
#   {
#     LSDRaster PrCurvature(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,profile_curvature_raster,GeoReferencingStrings);
#     raster_output[5] = PrCurvature;
#   }
#   if(raster_selection[6]==1)
#   {
#     LSDRaster TanCurvature(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,tangential_curvature_raster,GeoReferencingStrings);
#     raster_output[6] = TanCurvature;
#   }
#   if(raster_selection[7]==1)
#   {
#     LSDRaster Class(NRows,NCols,XMinimum,YMinimum,DataResolution,NoDataValue,classification_raster,GeoReferencingStrings);
#     raster_output[7] = Class;
#   }
#   return raster_output;
# }



















































# end of file