//
// HERE we define network parameters for Montecarlo Simulation
//
package resource_allocator.simulations;
import resource_allocator.modules.*;

network System{

	parameters:
	    //number of Terminals
	    int N;
	    int K; 

 	submodules:
 	    	gs: GS{
 	    	    parameters:
 	    	        terminal_counter = parent.N;
 	    	};
 	    	
 			st: Satellite{
 			};
 			
 			t[N]: Terminal{
 			};
 	
 	connections:
 		//connection between satellite and GS
 		gs.gs_io$o --> st.s_iogs$i;
		st.s_iogs$o --> gs.gs_io$i;	
 		
 		//connections between terminals and satellite
 		for i = 0 .. N-1{
 			t[i].t_io$o --> st.s_iot$i++;
    		st.s_iot$o++ --> t[i].t_io$i;
 		}

}