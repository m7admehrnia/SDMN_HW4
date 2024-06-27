# Question2  
Question: What if the namespaces are on different servers (virtual machine or physical server) that can see each other in layer 2 (figure 3)? Explain your solution. 
(Including the rules on the servers, no implementation is required)

Answer: You can route packets between the subnets by leveraging routing and bridging at the server level. Here’s how you can achieve this:
1) **Enable IP Forwarding on Both Servers**  
   ``sudo sysctl -w net.ipv4.ip_forward=1``
2) **Connect Bridges to Physical Interfaces**  
ensure the bridges on each server are connected to the physical network interface cards (NICs) that provide Layer 2 connectivity between the servers.  
    * server 1 (assuming eth0 is the interface connected to the shared Layer 2 network)  
      ``sudo ip link set eth0 master br1``   
      ``sudo ip link set eth0 up``
    * server 2  
      ``sudo ip link set eth0 master br2``   
      ``sudo ip link set eth0 up``
3) **Add Static Routes on Each Server**  
   Configure each server to know the route to the other subnet via the bridge interfaces (switch).
   * server 1  
     ``sudo ip route add 10.10.0.0/24 dev br1``
   * sever 2  
     ``sudo ip route add 172.0.0.0/24 dev br2``
4) **Configure Default Gateways in Each Namespace**  
   Set up default routes in each namespace to use the bridge IP addresses as gateways.
   * server 1 (node1 & node2)  
     ``ip netns exec node1 ip route add default via 172.0.0.1``  
     ``ip netns exec node2 ip route add default via 172.0.0.1``
   * server 2 (node3 & node4)  
     ``ip netns exec node3 ip route add default via 10.10.0.1``  
     ``ip netns exec node4 ip route add default via 10.10.0.1``
     
This setup ensures that each namespace can communicate with any other namespace, even if they reside on different servers.
