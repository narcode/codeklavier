// code space
~path = thisProcess.nowExecutingPath.dirname
(~path ++ "/CodeKlavier_hello_world_v3.scd").load;
{2.do{(~path ++ "/toypiano_sampler.scd").load; 2.wait;};}.fork;

//
