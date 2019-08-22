## 1 Sample, N Samples, and Continuous Modes

The Python ELVIS III API provides functions for you to perform three I/O modes of signal acquisition and generation: 1 sample, n samples, and continuous. Use the following table to learn about these modes.

Note: N sample is available only for analog signals. Continuous mode is not available yet.

<table>
    <thead>
        <tr>
            <th>Operation</th>
            <th>I/O Mode </th>
            <th>Description</th>
            <th>Use Case</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3>Signal Acquisition</td>
            <td>1 Sample</td>
            <td>
                The NI ELVIS III acquires one sample for a channel. This mode uses software-timed acquisition. The sample rate of acquisition depends on the software loop rate on the real-time processor. Various factors can affect this loop rate, such as simultaneous running of multiple programs on the NI ELVIS III target.
            </td>
            <td>Acquiring the most recent value or periodically monitoring low frequency signals, such as the temperature.</td>
        </tr>
        <tr>
            <td>N Samples</td>
            <td>
                The NI ELVIS III acquires a finite number of samples for a channel. This mode has the following characteristics:
                <ul>
                    <li><b>Hardware-timed acquisition</b>—The FPGA target on the NI ELVIS III has a 40 MHz clock, which controls the rate of acquisition. The sample rate depends on the hardware clock, which is faster than a software loop. A hardware clock is more accurate than a software loop. Therefore, you can have accurate control over the acquisition time between each sample.</li>
                    <li><b>Buffered acquisition</b>—FPGA transfers the samples from the FPGA target to an intermediate memory buffer using direct memory access (DMA) before LabVIEW reads these samples on the real-time processor.</li>
                    <li><b>Finite acquisition</b>—Acquires less than 10,000 samples on each channel. <a href="https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md">Gaps</a> in the acquired signal exist between sequential n samples acquisitions.</li>
                </ul>
            </td>
            <td>Acquiring finite high frequency signals, such as an audio signal.</td>
        </tr>
        <tr>
            <td>Continuous</td>
            <td>
                The NI ELVIS III continuously acquires samples for a channel until the acquisition is stopped. This mode has the following characteristics: 
                <ul>
                    <li><b>Hardware-timed acquisition</b>—The FPGA target on the NI ELVIS III has a 40 MHz clock, which controls the rate of acquisition. The sample rate depends on the hardware clock, which is faster than a software loop. A hardware clock is more accurate than a software loop. Therefore, you can have accurate control over the acquisition time between each sample.</li>
                    <li><b>Buffered acquisition</b>—FPGA transfers the samples from the FPGA target to an intermediate memory buffer using direct memory access (DMA) before LabVIEW reads these samples on the real-time processor.</li>
                    <li><b>Continuous acquisition</b>—Continuously acquires samples on each channel at a defined sampling rate until the acquisition is stopped. You can achieve continuous signal acquisition without <a href="https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md">gaps</a> by using this mode.</li>
                </ul>
            </td>
            <td>Continuously acquiring signals for a long period of time.</td>
        </tr>
    </tbody>
    <thead>
        <th></th>
        <th></th>
        <th></th>
        <th></th>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3>Signal Generation</td>
            <td>1 Sample</td>
            <td>
                The NI ELVIS III generates one sample for a channel. This mode uses software-timed generation. The sample rate of generation depends on the software loop rate on the real-time processor. Various factors can affect this loop rate, such as the simultaneous running of multiple programs on the NI ELVIS III target.
            </td>
            <td>Generating the most recent value or generating low frequency signals. For example, generating a known voltage to stimulate a device.</td>
        </tr>
        <tr>
            <td>N Samples</td>
            <td>
                The NI ELVIS III generates a finite number of samples for a channel. This mode has the following characteristics:
                <ul>
                    <li><b>Hardware-timed generation</b>—The FPGA target on the NI ELVIS III has a 40 MHz clock, which controls the rate of generation. The sample rate depends on the hardware clock, which is faster than a software loop. A hardware clock is more accurate than a software loop. Therefore, you can have accurate control over the time between each sample.</li>
                    <li><b>Buffered generation</b>—The real-time processor takes the samples from LabVIEW and places them in an intermediate memory buffer using DMA before FPGA gets the samples from the buffer.</li>
                    <li><b>Finite generation</b>—generates less than 10,000 samples on each channel. <a href="https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md">Gaps</a> in the generated signal exist between sequential n samples generations.</li>
                </ul>
            </td>
            <td>Generating finite time-varying signals, such as an AC sine wave.</td>
        </tr>
        <tr>
            <td>Continuous</td>
            <td>
                The NI ELVIS III continuously generates samples for a channel until the signal generation is stopped. This mode has the following characteristics: 
                <ul>
                    <li><b>Hardware-timed generation</b>—The FPGA target on the NI ELVIS III has a 40 MHz clock, which controls the rate of generation. The sample rate depends on the hardware clock, which is faster than a software loop. A hardware clock is more accurate than a software loop. Therefore, you can have accurate control over the time between each sample.</li> 
                    <li><b>Buffered generation</b>—The real-time processor takes the samples from LabVIEW and places them in an intermediate memory buffer using DMA before FPGA gets the samples from the buffer.</li>
                    <li><b>Continuous generation</b>—Continuously generates samples on each channel at a defined update rate until the generation is stopped. You can achieve continuous signal generation without <a href="https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md">gaps</a> by using this mode.</li>
                </ul>
            </td>
            <td>Continuously generating signals for a long period of time.</td>
        </tr>
    </tbody>
</table>