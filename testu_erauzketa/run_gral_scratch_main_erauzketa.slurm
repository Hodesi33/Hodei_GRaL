#!/usr/bin/env bash
#SBATCH --account=hitz-exclusive
#SBATCH --partition=hitz-exclusive
#SBATCH --job-name=GRaL_run
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --constraint=a100-sxm4
#SBATCH --output=./log/GRaL_run_%j.out
#SBATCH --error=./log/GRaL_run_%j.err

#SBATCH --constraint=a100-sxm4
#SBATCH --mem=40GB
#SBATCH --time=05:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=hsanz004@ikasle.ehu.eus

module load Miniforge3
source /dipc/hodesi33/GRaL-a/venv/bin/activate

python main_erauzketa.py
