//
// HERE we define network parameters for Montecarlo Simulation
//
package resource_allocator.simulations;
import resource_allocator.modules.*;

network System{

	parameters:
	    //number of Terminals
	    int N;

 	submodules:
 	    	gs: GS{
 	    	};
 	    	
 			st: Satellite{
 			};
 			
 			t[N]: Terminal{
 			};
 	
 	connections:
 		//connection between satellite and GS
 		gs.gs_io <-->  st.s_iogs; 	
 		
 		//connections between terminals and satellite
 		for i = 0 .. N-1{
 			t[i].t_io <--> st.s_iot++;
 		}

}