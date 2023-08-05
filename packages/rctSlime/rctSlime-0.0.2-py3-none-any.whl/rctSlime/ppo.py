import torch
import torch.nn as nn
import os
from rctSlime.network import PolicyNetwork


DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Config2:
    def __init__(self, in_dict):
        for k, v in in_dict.items():
            setattr(self, k, v)

    def add_config(self, name, value):
        setattr(self, name, value)

# artchitecture parameters
num_layers = 3
num_heads = 1
embedding_dim = 16  # each of the values is mapped to the 16 dims
observation_shape = 512
action_space = 4

# learner parameters
batch_size = 256
solved_reward = 1 # stop training is average reward is greater than solved reward
log_interval = 100 # print log every these many steps
max_episodes = int(5e+4)  # max training episodes
max_timesteps = 2000000  # maximum time steps in one episode
update_timestep = 64  # update policy every these many steps
lr = 0.002  # learning rate
gamma = 0.99  # discount factor
k_epochs = 4  # update policy every n timesteps
eps_clip = 0.2  # clip parameter for rctSlime
random_seed = 4

def ppo_model_config():
    config = Config2(dict(

                num_layers=num_layers,
                num_head=num_heads,
                embedding_dim=embedding_dim,
                input_dim=observation_shape,
                num_actions=action_space,

                batch_size=batch_size,
                solved_reward=solved_reward,
                log_interval=log_interval,
                max_episodes=max_episodes,
                max_timesteps=max_timesteps,
                update_timestep=update_timestep,
                lr=lr,
                gamma=gamma,
                k_epochs=k_epochs,
                eps_clip=eps_clip,
                seed=random_seed
            ))

    return config

ppo_config = ppo_model_config()

class PPO:
    def __init__(self, config=ppo_config):
        self.lr = config.lr
        self.gamma = config.gamma
        self.eps_clip = config.eps_clip
        self.k_epochs = config.k_epochs
        self.policy = PolicyNetwork(config, config.input_dim[0]).to(DEVICE)
        self.optimizer = torch.optim.Adam(self.policy.parameters(),
                                          lr=self.lr)
        self.policy_old = PolicyNetwork(config, config.input_dim[0]).to(DEVICE)
        self.mse_loss = nn.MSELoss()


    def load_model(self, model_path, model_name):
        if os.path.exists(model_path + model_name):
            path = model_path + model_name
            map_location = DEVICE
            self.policy.load_state_dict(torch.load(path, map_location=map_location))
            print("Successfully load the model: {}".format(path))

    def eval_model(self, model_path, model_name):
        self.load_model(model_path, model_name)
        self.policy.eval()
        print('Successfully start eval model')

    def update(self, memory):
        # monte carlo estimate of state rewards
        rewards = []
        dis_rew = 0
        for rew in reversed(memory.rewards):
            dis_rew = rew + (self.gamma * dis_rew)
            rewards.append(dis_rew)
        rewards = rewards[::-1]

        # normalizing the rewards
        rewards = torch.tensor(rewards).to(DEVICE)
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-5)

        # convert list to tensor
        old_states = torch.stack(memory.states).to(DEVICE).detach()
        old_states = old_states[0]
        old_actions = torch.stack(memory.actions).to(DEVICE).detach()
        old_logprobs = torch.stack(memory.logprobs).to(DEVICE).detach()

        # print('*** old_states.size()', old_states.size())

        # optimize policy for k-epochs
        for _ in range(self.k_epochs):
            # evaluating the old states
            log_probs, state_values, dist_entropy = self.policy.evaluate(old_states, old_actions)
            # find the ratio r(theta) = (pi_theta / pi_theta_old)
            ratios = torch.exp(log_probs / old_logprobs.detach())
            # finding surrogate loss
            rewards = rewards.unsqueeze(-1)
            advantages = rewards - state_values.detach()
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            loss = -torch.min(surr1, surr2) + 0.5 * self.mse_loss(state_values, rewards) - 0.01 * dist_entropy

            # take a gradient step
            self.optimizer.zero_grad()
            loss.mean().backward()
            self.optimizer.step()

        # copy new weights into old policy
        self.policy_old.load_state_dict(self.policy.state_dict())



