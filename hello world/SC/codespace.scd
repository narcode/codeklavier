// code space
~path = thisProcess.nowExecutingPath.dirname


// evaluate one from below, not both \\\

// OPTION 1: to load internal toy pinao sampler (i.e. midi loopback):
(~path ++ "/CodeKlavier_hello_world_v_sampler.scd").load;
{2.do{(~path ++ "/toypiano_sampler.scd").load; 2.wait;};}.fork;

// OPTION 2: to play with Robot Toy Piano instrument (i.e. midiout):
(~path ++ "/CodeKlavier_hello_world_v_sampler.scd").load;


//
