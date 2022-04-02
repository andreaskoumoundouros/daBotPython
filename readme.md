# Info for starting and mainting bot python process
https://pm2.keymetrics.io/docs/usage/quick-start/

## Numa node err
If you get the numa node error returning -1 use:
```bash
for a in /sys/bus/pci/devices/*; do echo 0 | sudo tee -a $a/numa_node; done
```
