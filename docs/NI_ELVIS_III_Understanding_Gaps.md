## Understanding Gaps

### Analog Input

The following figure illustrates the gap between sequential n samples acquisitions when using the Analog Input API. 

![](docs/resource/nsample.png)

In the previous figure, the x-axis represents time and the y-axis represents amplitude. The waveform in blue represents the signal that the hardware acquires. Gaps in the acquired signal exist between sequential calls of the Analog Input (n samples) API. During the gap, the hardware does not acquire any signal. The duration of the gap between acquisitions is software dependent and varies from iteration to iteration.

Note: You need to choose an FPGA personality that supports n samples I/O mode to perform n samples read operations. 
