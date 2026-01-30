//
// HERE we define network parameters for Montecarlo Simulation
//
package resource_allocator.simulations;
import resource_allocator.modules.*;

network System
{
    parameters:
        //number of Terminals
        int N;
        int K;

        @display("bgb=604,394");
    submodules:
        oracle: Oracle {
            @display("p=28,32");
        }

        gs: GS {
            parameters:
                terminal_counter = parent.N;
                @display("p=493,187");
        }

        st: Satellite {
            @display("p=295,187");
        }

        t[N]: Terminal {
            parameters:
                K = parent.K;
                @display("p=103,187");
        }

    connections:
        //connection between satellite and GS
        gs.gs_io$o --> st.s_iogs$i;
        st.s_iogs$o --> gs.gs_io$i;

        //connections between terminals and satellite
        for i=0..N-1 {
            t[i].t_io$o --> st.s_iot$i++;
            st.s_iot$o++ --> t[i].t_io$i;
        }

}
