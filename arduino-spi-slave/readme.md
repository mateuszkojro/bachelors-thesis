# Arduino SPI slave

This turns arduino into an spi server responding with the sent messages, `spi_slave.ino` contains implementation based on [1]

## Pinout

Pinout for Arduino UNO [2]:

| Pin | Purpose |
| --- | --------|
| 11  | MOSI    |
| 12  | MISO    |
| 13  | SCLK    |
| GND | CE0     |

## References

[1] <https://arduino.stackexchange.com/questions/89090/how-to-make-an-arduino-act-reliably-as-an-spi-slave>
[2] <https://www.makerguides.com/master-slave-spi-communication-arduino/>