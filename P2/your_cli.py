import os
import sys
import subprocess
import ctypes
import urllib.request
import tarfile

# Define the clone flags
CLONE_NEWNS = 0x00020000
CLONE_NEWUTS = 0x04000000
CLONE_NEWIPC = 0x08000000
CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
CLONE_NEWUSER = 0x10000000
STACK_SIZE = 1024 * 1024

# C function to clone process
libc = ctypes.CDLL("libc.so.6", use_errno=True)


def setup_root_filesystem(root_path):
    # Ensure the root filesystem directory exists
    os.makedirs(root_path, exist_ok=True)

    # URL of the Ubuntu 20.04 root filesystem tarball
    tarball_url = "https://partner-images.canonical.com/core/focal/current/ubuntu-focal-core-cloudimg-amd64-root.tar.gz"
    tarball_name = "ubuntu-focal-core-cloudimg-amd64-root.tar.gz"

    # Download the tarball
    print("Downloading the root filesystem tarball...")
    urllib.request.urlretrieve(tarball_url, tarball_name)

    # Extract the tarball to the root filesystem directory
    print("Extracting the root filesystem tarball...")
    with tarfile.open(tarball_name, "r:gz") as tar:
        tar.extractall(path=root_path)

    # Clean up the tarball
    print("Cleaning up...")
    os.remove(tarball_name)

    print(f"Root filesystem setup completed at {root_path}")


def set_hostname(hostname):
    libc.sethostname(hostname.encode(), len(hostname))


def create_filesystem(root_path):
    os.makedirs(root_path, exist_ok=True)
    # Bind mount the root filesystem
    os.system(f'mount --bind {root_path} {root_path}')
    os.chroot(root_path)
    os.chdir('/')


def set_memory_limit(container_pid, memory_limit):
    cgroup_path = f'/sys/fs/cgroup/memory/my_container_{container_pid}'
    os.makedirs(cgroup_path, exist_ok=True)
    with open(f'{cgroup_path}/memory.limit_in_bytes', 'w') as f:
        f.write(str(memory_limit * 1024 * 1024))
    with open(f'{cgroup_path}/tasks', 'w') as f:
        f.write(str(container_pid))


def run_container(hostname, root_path, memory_limit):
    # Set hostname
    set_hostname(hostname)
    
    # Create isolated filesystem
    create_filesystem(root_path)

    # Start bash
    os.execvp('/bin/bash', ['/bin/bash'])


def child_func(hostname, root_path, memory_limit):
    # Create new namespaces
    if libc.unshare(CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNET) != 0:
        print(f'Error: {ctypes.get_errno()}')
        sys.exit(1)

    pid = os.fork()
    if pid == 0:
        # This is the child process in the new PID namespace
        run_container(hostname, root_path, memory_limit)
    else:
        # Set memory limit
        if memory_limit:
            set_memory_limit(pid, memory_limit)
        os.waitpid(pid, 0)  # Wait for the container to exit


def main():
    if len(sys.argv) < 2:
        print("Usage: your-cli <hostname> [memory_limit_in_mb]")
        sys.exit(1)

    hostname = sys.argv[1]
    root_path = '/path/to/root/filesystem'
    memory_limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    stack = ctypes.create_string_buffer(STACK_SIZE)

    # Clone the current process
    child_pid = libc.clone(
        child_func(hostname, root_path, memory_limit),
        ctypes.byref(stack, STACK_SIZE),
        CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWPID
    )




if __name__ == "__main__":
    main()
