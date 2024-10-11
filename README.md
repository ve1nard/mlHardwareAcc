# Hardware Accelerator for Machine Learning

Deep Neural Networks (DNNs) have become an attractive field of in terest in most artificial 
intelligence applications such as computer vision, speech recognition, image and video processing,
and robotics. DNNs show state-of-the-art performance and accuracy in the context of many complex
real-life applications; however, this results in a high computational load that many general-purpose 
hardware architectures are not able to handle. Therefore, a great interest has been developed in
designing hardware accelerators specifically tailored for DNNs. The desired result of such an endeavor is the
development of a cheap and energy-efficient hardware accelerator with high computational accuracy.

## Assigned tasks 

There were three main tasks to be completed by the
end of the research. 
1. The first task was to develop accurate and approximate multiply-accumulate hardware for Deep Learning accelerators.
In essence, the tasks consisted of researching various multiplication and addition algorithms, implementing them in hardware,
and combining them to get a complete Multiply Accumulate (MAC) block.
2.  After building the MAC block, the second task was to combine multiple of these units together to build a whole Multiply
 Acumulate (MAC) Array Template. For this purpose, multiple dataflow paradigms had to be investigated and the most efficient one
had to be chosen for implementation.
3.  Lastly, it was necessary to develop weight memory architecture and interface it with the MAC array. This task
revolved around developing an on-chip memory block and connecting it to both an off-chip memory and the neural processing array.

## Results achieved 
With regard to the first task, various multiplication algorithms were studied and implemented. After completing the theoretical
overview of different multiplication algorithms, it was decided to focus on the two most used ones, including the Wallace Tree 
and the Booth multiplier. Further research showed that combining the two and producing the modified Booth-Wallace Tree multiplier
would produce even better results. 

After building the MAC unit, different dataflow architectures, including weight stationary, input stationary, and output stationary,
were studied. As a result, a single-buffer weight stationary array was designed with further plans of implementing a double-buffer 
structure to reduce the idle time of the MAC units. The third task is still in the process of completion. Before starting the implementation
of on-chip weights storage, it was necessary to study the inner workings of various memory architectures, including SRAM, DRAM,
and BRAM. Currently, the ways of interfacing with Block RAM available on 2 FPGA boards are being investigated.

## Knowledge gained

Throughout the course of the research, a comprehensive understanding of the architecture of the Multiply Accumulate unit
was gained. This research helped in understanding differences in the performance of various multiplication algorithms for both signed and unsigned
numbers. Building a complete MAC array allowed to see various dataflow techniques in practice and understand their benefits in comparison to one
another. Challenges in designing the required hardware resulted in a better understanding of the RTL synthesis since it was very helpful to see the
synthesized diagrams and fix the design accordingly. Finally, the knowledge gained about different memory architectures will be very useful in the future
for the implementation of weight memory architecture.

## Conclusion 
This research was a great experience both in theoretical and practical terms since a considerable amount of time was spent on both
studying and using gained knowledge to implement the designs. The hope is to continue this research, work on further accomplishments of the tasks, and
finally build a working prototype of the hardware accelerator.
