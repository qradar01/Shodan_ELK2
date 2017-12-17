# Shodan_ELK2
#This is my most recent project that aims to serve as a sort of local plugin for log stash. 
#My next step(s) are to integrate other data sources and/or rewrite this in JRuby and see if I can get it published
#in the elastic master build as a plugin.
# In terms of further reading, I would recommend referring to a recently published paper called "A Toolset for Intrusion and Insider Threat Detection" by Markus Ring, Sarah Wunderlich, Dominik Grudl, Dieter Landes, and Andreas Hotho. This paper introduces the "Coburg Utility Framework," or CUF, which is described as a pipes and filters architecture commonly applied to software that deals with handling and processing data streams. The data mining workflow in M.Ring et al's paper is as follows: Input -> Preprocessing -> Clustering -> Visualize -> Output.

# I wasn't sure exactly what to call the source code I wrote, but thanks to the CUF now have a clearer picture of how my pre-input plugin filter should integrate into an ELK-based realtime data analytics engine. Futher development should angle to introduce another function that references IP-based reputation ranking.
