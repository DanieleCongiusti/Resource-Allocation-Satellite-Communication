//This NED file model Satellite
package resource_allocator.modules;


simple Satellite
{
    parameters:
        //space for parameters

	gates:
	    // provide one input gate for each terminal
	    inout 	s_iot[];
	    //gate for GS communication
	    inout   s_iogs;
}
