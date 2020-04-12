import gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make('MountainCar-v0')
env.reset()

LEARNING_RATE = 0.1
DISCOUNT = 0.95
ITERATIONS = 20000

SHOW_EVERY = 500

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

epsilon = 0.5
START_EPSILON_DECAY = 1
END_EPSILON_DECAY = ITERATIONS // 2

epsilon_decay_value = epsilon/(END_EPSILON_DECAY - START_EPSILON_DECAY)

q_table = np.random.uniform(low=-2, high=0, size=DISCRETE_OS_SIZE + [env.action_space.n])

i_rewards = []
aggr_i_rewards = {'i': [], 'avg': [], 'min': [], 'max': []}


def make_state_discrete(state):
    d_s = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(d_s.astype(np.int))


for iteration in range(ITERATIONS):
    i_reward = 0
    if iteration % SHOW_EVERY == 0:
        print(iteration)
        render = True
    else:
        render = False

    discrete_state = make_state_discrete(env.reset())
    done = False
    while not done:

        if np.random.random() > epsilon:
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, env.action_space.n)

        new_state, reward, done, _ = env.step(action)
        i_reward += reward

        new_discrete_state = make_state_discrete(new_state)

        if render:
            env.render()

        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action, )]

            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state+(action, )] = new_q

        elif new_state[0] >= env.goal_position:
            print(f"We made it on iteration: "+str(iteration))
            q_table[discrete_state + (action, )] = 0

        discrete_state = new_discrete_state

    if END_EPSILON_DECAY >= iteration >= START_EPSILON_DECAY:
        epsilon -= epsilon_decay_value

    i_rewards.append(i_reward)

    if not iteration % SHOW_EVERY:  # same as if not iteration % SHOW_EVERY == 0
        avg_reward = sum(i_rewards[-SHOW_EVERY:])/len(i_rewards[-SHOW_EVERY:])
        aggr_i_rewards['i'].append(iteration)
        aggr_i_rewards['avg'].append(avg_reward)
        aggr_i_rewards['min'].append(min(i_rewards[-SHOW_EVERY:]))
        aggr_i_rewards['max'].append(max(i_rewards[-SHOW_EVERY:]))

        print(f"Iteration: {iteration} avg: {avg_reward}"
              f" min: {min(i_rewards[-SHOW_EVERY:])}"
              f" max: {max(i_rewards[-SHOW_EVERY:])}")


env.close()


plt.plot(aggr_i_rewards['i'], aggr_i_rewards['avg'], label='avg')
plt.plot(aggr_i_rewards['i'], aggr_i_rewards['min'], label='min')
plt.plot(aggr_i_rewards['i'], aggr_i_rewards['max'], label='max')
plt.legend(loc=4)
plt.show()

