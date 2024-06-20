# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_node> <destination_node>"
    exit 1
fi

# Get the node names from the arguments
SOURCE_NODE=$1
DEST_NODE=$2

# Get the IP address of the destination node
case $DEST_NODE in
    node1)
        DEST_IP="172.0.0.2"
        ;;
    node2)
        DEST_IP="172.0.0.3"
        ;;
    node3)
        DEST_IP="10.10.0.2"
        ;;
    node4)
        DEST_IP="10.10.0.3"
        ;;
    router)
        DEST_IP="172.0.0.1"
        ;;
    *)
        echo "Unknown destination node: $DEST_NODE"
        exit 1
        ;;
esac

# Execute the ping command in the source namespace
ip netns exec $SOURCE_NODE ping $DEST_IP -c 3