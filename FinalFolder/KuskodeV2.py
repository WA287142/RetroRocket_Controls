# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:05:54 2023

@author: JWKus
"""

import numpy as np
import scipy.spatial.transform as scitrans

# Let the global origin be at the center of the base
# The +x direction shall be towards the right wing of the rocket
# The +y direction shall be towards the nose of the rocket
# The +z direction shall be upwards

# We should always have 6 actuators; the code will probably break if this is changed...
num_acts = 6

def get_inv_kine(x_disp, y_disp, z_disp, ψ, θ, φ, get_out_of_plane=False, deg_input=False, deg_output=False):
    x_disp = float(x_disp)
    y_disp = float(y_disp)
    z_disp = float(z_disp)

    if deg_input:
        ψ = np.deg2rad(float(ψ)/2)
        θ = np.deg2rad(float(θ)/2)
        φ = np.deg2rad(float(φ)/2)
    
    print("angles in kine:", ψ, θ, φ)
    # DCM defining the rotation between the platform frame and base frame
    rot_representation = scitrans.Rotation.from_euler('zxy', [-ψ, θ, φ], degrees=False)
    DCM = rot_representation.as_matrix()
    # Vector pointing from origin of base coordinate system to origin of platform coordinate system
    T_vec = np.vstack([x_disp, y_disp, z_disp])

    # Length of the lever arm (in)
    h_mag = 6.95
    
    # Length of the drive rod (in)
    d_mag = 26.25
    
    ## Instantiates arrays for the vectors:
    # Pointing to the gearbox shaft from the base coordinate system origin
    b_list = []
    # These values are slightly fudged from the CAD (by no more than 0.1") to 
    # preserve symmetry
    b_list.append(np.vstack([+15.1, +18.3, 0]))
    b_list.append(np.vstack([-15.1, +18.3, 0]))
    b_list.append(np.vstack([-23.3, +03.9, 0]))
    b_list.append(np.vstack([-08.3, -22.2, 0]))
    b_list.append(np.vstack([+08.3, -22.2, 0]))
    b_list.append(np.vstack([+23.3, +03.9, 0]))
    
    # Pointing to the platform end of the drive rod from the platform coordinate system origin
    p_list = []
    p_list.append(np.vstack([+03.27, +11.72, 0]))
    p_list.append(np.vstack([-03.27, +11.72, 0]))
    p_list.append(np.vstack([-11.53, -02.60, 0]))
    p_list.append(np.vstack([-08.27, -08.26, 0]))
    p_list.append(np.vstack([+08.27, -08.26, 0]))
    p_list.append(np.vstack([+11.53, -02.60, 0]))
    
    # Pointing to joint between the lever arm and drive rod from the gearbox shaft
    h_list = []
    # Pointing to the platform end of the drive rod from the joint between the lever arm and drive rod
    d_list = []
    # Pointing to the platform end of the drive rod from the gearbox shaft
    l_list = []
    
    # And for the scalar values of motor alignment angle
    β_array = np.zeros(num_acts)
    β_array[0] = np.deg2rad(210)
    β_array[1] = np.deg2rad(330)
    β_array[2] = np.deg2rad(330)
    β_array[3] = np.deg2rad(90)
    β_array[4] = np.deg2rad(90)
    β_array[5] = np.deg2rad(210)
    
    # Squared lengths
    e_array = np.zeros(num_acts)
    f_array = np.zeros(num_acts)
    g_array = np.zeros(num_acts)
    # Lever arm angle
    α_array = np.zeros(num_acts)
    
    # Out-of-rotation-plane angle of the joint between the lever arm and drive rod
    δ_array = np.zeros(num_acts)
    
    # Big loop in which we calculate all of the properties for each leg; one by one
    for i in range(num_acts):
        # Assumes a platform with 3 pairs of actuators with each pair spaced evenly
        # Actuators within a pair are antiparallel
        
        # Visual conceptualization below:
        '''
                1_________0
               /           \
              /             \
             /               \
            /                 \
           /                   \
           2                   5
            \                 /
             \               /
              \             /
               3___________4
        '''
        
        # Transforming p into the base frame
        p_list[i] = DCM @ p_list[i]
        
        # Finding the l vector
        l_list.append(T_vec + p_list[i] - b_list[i])
        
        # Calculates the squared lengths e, f, g
        e_array[i] = 2 * h_mag * l_list[i][2, 0]
        f_array[i] = 2 * h_mag * ( np.cos( β_array[i] ) * l_list[i][0, 0] + np.sin( β_array[i] ) * l_list[i][1, 0] )
        g_array[i] = np.linalg.norm( l_list[i] ) ** 2 - ( d_mag  ** 2 - h_mag ** 2 )
        # And the lever arm angle, α
        α_array[i] = np.arcsin( g_array[i] / np.sqrt( e_array[i] ** 2 + f_array[i] ** 2 ) ) - np.arctan2( f_array[i], e_array[i] )
        
        # Return None if there are NaN values detected or any motor angles exceed 45° (pi/4)
        if np.isnan(α_array[i]) or abs(α_array[i]) > np.pi/4:
            return [-99999]

        # Flip the sign of α if it corresponds to one of the "left-handed" actuators
        if i % 2 == 1:
            α_array[i] *= -1
        
        # Change values to degrees if desired
        if deg_output:
            α_array[i] = np.rad2deg(α_array[i])
        
        ### Determination of the angle at the level arm and drive rod joint.
        '''
        Note! This formulation assumes that the motor shafts lie purely in the
        horizontal plane. Any deviation of the motor shaft from the horizontal 
        will require a vector other than k_hat to create a proper normal from the
        plane in which the shaft rotates.
        '''
        if get_out_of_plane:
                
            # Calculation of lever arm vector by motor positions and shaft rotations
            h_i = np.vstack([np.cos( β_array[i] ) * np.cos( α_array[i] ) * h_mag,
                             np.sin( β_array[i] ) * np.cos( α_array[i] ) * h_mag, 
                             np.sin( α_array[i] ) * h_mag])
            h_list.append( h_i )
            
            # Calculation of the drive rod vector by using the fact that l = d + h
            d_i = l_list[i] - h_list[i]
            d_list.append( d_i )
            
            ### Finding a vector which is normal to the shaft's plane of rotation
            # k_hat in the base frame (assuming that the motors are mounted parallel to
            # the floor) will always be in the plane of rotation of h.
            k_hat = np.hstack( [0, 0, 1] )
            n_vec = np.vstack(np.cross( np.hstack( h_list[i] ), k_hat ) )
            # In other words, n points along the shaft itself.
            
            # The out-of-plane angle measured at the drive rod / lever arm joint.
            # Positive is 'outwards' (angled away from the platform) and vice versa
            δ_array[i] = np.pi/2 - np.arccos( np.dot( np.hstack(d_list[i]) , np.hstack(n_vec) ) / 
                                              np.linalg.norm( d_list[i] ) / 
                                              np.linalg.norm( n_vec ) )

        # End of main loop
    
    if get_out_of_plane:
        return α_array, δ_array
    else:
        return α_array
