Run the script 
``` bash ./your-cli.py my_hostname [memory_limit_in_mb] ```

After running this script and entering the new bash, executing "ps" may encounter the error.
just try mount -t proc proc /proc and then run "ps" again.
