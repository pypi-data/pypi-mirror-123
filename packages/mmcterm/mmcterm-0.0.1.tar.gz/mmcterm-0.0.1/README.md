# mmcterm

Terminal for the custom "serial over IPMB" protocol used by DESY MMC.

## Usage

```
$ mmcterm [-h] [-v] [-c CHANNEL] [-l] [-d] [-i] mch_addr mmc_addr

DESY MMC Serial over IPMB console

positional arguments:
  mch_addr              IP address or hostname of MCH
  mmc_addr              IPMB-L address of MMC

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CHANNEL, --channel CHANNEL
                        console channel
  -l, --list            list available channels
  -d, --debug           pyipmi debug mode
  -i, --ipmitool        make pyipmi use ipmitool instead of native rmcp
```
