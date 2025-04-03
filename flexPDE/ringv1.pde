

Title 'Rotating Ring Magnet'  


Coordinates 
	CARTESIAN3
   

Variables  

    A { z-component of Vector Magnetic Potential }  


Definitions  

    mu = 1

    S = 0             { current density }  

    Px = 0             { Magnetization components }  

    Py = 0  

    P = vector(Px,Py) { Magnetization vector }  

    H = (curl(A)-P)/mu { Magnetic field }    

    y0 = 8             { Size parameter }  
    
    ! Geometric Constants
    roomRadius = 40
    roomHeight = 100
    
    rodRadius = 5
    rodHeight = 80
    
    ringInnerR = 15
    ringOuterR = 20
    ringHeight = 5
    
    phimax = 360 degrees


Materials

'Magnet' : Py = 10

'Other'  : mu = 5000

 
Initial values  

     A = 0

   
Equations     

     A : curl(H) + S = 0  
     
   

BOUNDARIES

   Region 1   ! Outer region, e.g., vacuum or air

     start(-40,0)

     natural(A) = 0 line to (60,0)  ! Natural boundary condition along the x-axis

     value(A) = 0 line to (60,100) to (-40,100) to close  ! Zero value boundary along the y-axis

   

   Region 2   ! Another material region (e.g., non-magnetic material)

     use material 'Other'

     start(0,0)

     line to (15,0) to (15,100) to (0,100) to close  ! Defining a polygonal boundary

   

   Region 3   ! Permanent magnet region

     use material 'Magnet'

     start(20,50)

     line to (30,50) to (30,60) to (20,60) to close  ! Defining the boundary of the magnet's shape



Monitors  

   contour(A)


   

Plots  

   grid(x,y,z)  

   vector(dy(A),-dx(A)) as 'FLUX DENSITY B'  

   vector((dy(A)-Px)/mu, (-dx(A)-Py)/mu) as 'MAGNETIC FIELD H'  

   contour(A) as 'Az MAGNETIC POTENTIAL'  

   surface(A) as 'Az MAGNETIC POTENTIAL'  

   

End  

  
