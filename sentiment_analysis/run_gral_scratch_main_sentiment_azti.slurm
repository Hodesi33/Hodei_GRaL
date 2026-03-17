#!/usr/bin/env bash
#SBATCH --partition=GPU-ilara
#SBATCH --job-name=GRaL_run
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --output=./log/GRaL_run_%j.out
#SBATCH --error=./log/GRaL_run_%j.err
#SBATCH --mem=40GB
#SBATCH --time=10:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=hsanz004@ikasle.ehu.eus

module load Miniforge3
source /home/hsanz004/Hodei_GRaL/venv/bin/activate

python main_sentiment.py