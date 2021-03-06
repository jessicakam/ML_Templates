# 2017/07/29

from data_preprocessing import DataPreProcessing
from data_postprocessing import DataPostProcessing
import random
import math
import pandas as pd
import matplotlib.pyplot as plt

class RandomSelection(DataPreProcessing, DataPostProcessing):
    def importDataset(self, csv_file):
        self.dataset = pd.read_csv(csv_file)
   
    def implement(self, N, d):
        self.ads_selected = []
        self.total_reward = 0
        for n in range(0, N):
            ad = random.randrange(d)
            self.ads_selected.append(ad)
            reward = self.dataset.values[n, ad]
            self.total_reward = self.total_reward + reward
        
    def visualizeResults(self, title, xlabel, ylabel):
        plt.hist(self.ads_selected)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    
class UCB(RandomSelection):
    def implement(self, N, d):
        self.ads_selected = []
        numbers_of_selections = [0] * d
        sums_of_rewards = [0] * d
        self.total_reward = 0
        for n in range(0, N):
            ad = 0
            max_upper_bound = 0
            for i in range(0, d):
                if (numbers_of_selections[i] > 0):
                    average_reward = sums_of_rewards[i] / numbers_of_selections[i]
                    delta_i = math.sqrt(3/2 * math.log(n + 1) / numbers_of_selections[i])
                    upper_bound = average_reward + delta_i
                else:
                    upper_bound = 1e400
                if upper_bound > max_upper_bound:
                    max_upper_bound = upper_bound
                    ad = i
            self.ads_selected.append(ad)
            numbers_of_selections[ad] = numbers_of_selections[ad] + 1
            reward = self.dataset.values[n, ad]
            sums_of_rewards[ad] = sums_of_rewards[ad] + reward
            self.total_reward = self.total_reward + reward

class ThompsonSampling(RandomSelection):
    def implement(self, N, d):
        self.ads_selected = []
        numbers_of_rewards_1 = [0] * d
        numbers_of_rewards_0 = [0] * d
        self.total_reward = 0
        for n in range(0, N):
            ad = 0
            max_random = 0
            for i in range(0, d):
                random_beta = random.betavariate(numbers_of_rewards_1[i] + 1, numbers_of_rewards_0[i] + 1)
                if random_beta > max_random:
                    max_random = random_beta
                    ad = i
            self.ads_selected.append(ad)
            reward = self.dataset.values[n, ad]
            if reward == 1:
                numbers_of_rewards_1[ad] = numbers_of_rewards_1[ad] + 1
            else:
                numbers_of_rewards_0[ad] = numbers_of_rewards_0[ad] + 1
            self.total_reward = self.total_reward + reward

