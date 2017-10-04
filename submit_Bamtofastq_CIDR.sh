#!/usr/bin/env bash

for i in {0..10}
do
	echo "sbatch /fh/fast/stanford_j/Xiaoyu/HPC/code/Bamtofastq_CIDR.py $i"	
	sbatch /fh/fast/stanford_j/Xiaoyu/HPC/code/Bamtofastq_CIDR.py $i
	sleep 1s
done

