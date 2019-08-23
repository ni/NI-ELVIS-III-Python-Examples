## Understanding Gaps

### Analog Input

The following figure illustrates the gap between sequential n samples acquisitions when using the Analog Input API. 

<p align="center"><img src="../docs/resource/nsample.png"/></p>

In the previous figure, the x-axis represents time and the y-axis represents amplitude. The waveform in blue represents the signal that the hardware acquires. Gaps in the acquired signal exist between sequential calls of the Analog Input (n samples) API. During the gap, the hardware does not acquire any signal. The duration of the gap between acquisitions is software dependent and varies from iteration to iteration.

Note: You need to choose an FPGA personality that supports N samples I/O mode to perform n samples read operations. 

If you want to create a continuous acquisition without data loss, specify **Analog input (continuous)** for I/O mode. The following figure illustrates a continuous acquisition:

<p align="center"><img src="../docs/resource/continuousSample.png"/></p>

Note: Continuous mode is not available yet.

### Related Information

[1 Sample, N Samples, and Continuous Modes](./1_Sample_N_Samples_and_Continuous_Modes.md)

[I/O Connectors (ELVIS III)](http://www.ni.com/documentation/en/ni-elvis-iii/latest/controlio/controlio/)