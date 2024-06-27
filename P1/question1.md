# Question 1
Question: Now delete the router and its links to the bridges (figure 2). How can we route packets from
one subnet to another? Explain your solution.  
(Including the rules in the root namespace, no implementation is required)

Answer: If the router and its links to the bridges are deleted, you can still route packets between the two subnets by using the root namespace to perform routing functions. This involves setting up static routes and enabling IP forwarding in the root namespace. Here's how you can achieve this:  
1) **Enable IP Forwarding in the Root Namespace** (This allows the Linux kernel to forward packets between interfaces)  
   ``sudo sysctl -w net.ipv4.ip_forward=1``
2) **Add Static Routes** (We need to add static routes in the root namespace to direct traffic from one subnet to another via the bridges)
   * Add a route for the 172.0.0.0/24 subnet to be routed through the interface connected to br1  
     ``sudo ip route add 172.0.0.0/24 dev br1``
   * Add a route for the 10.10.0.0/24 subnet to be routed through the interface connected to br2  
     ``sudo ip route add 10.10.0.0/24 dev br2``
3) **Configure default routes to point to the bridge interface IP addresses**  
   Let's consider an example where a node in '**br1**' (172.0.0.2/24) needs to communicate with a node in '**br2**' (10.10.0.2/24)
   * in source node (172.0.0.2) default gateway should point to the bridge interface, which now acts as the route to other subnets.  
     ``ip netns exec ns1 ip route add default via 172.0.0.1``
   * in destination node (10.10.0.2)  
     ``ip netns exec ns3 ip route add default via 10.10.0.1``
