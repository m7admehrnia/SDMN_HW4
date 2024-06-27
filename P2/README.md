Run the script: ./your-cli.py my_hostname [memory_limit_in_mb].

After running this script and entering the new bash, executing the command "ps" may encounter the error.
just try mount -t proc proc /proc in the this bash and run "ps" again.
