// code space
~path = thisProcess.nowExecutingPath.dirname
(~path ++ "/SC/CodeKlavier_hello_world_v3.scd").load;
{2.do{(~path ++ "/SC/toypiano_sampler.scd").load; 2.wait;};}.fork;
