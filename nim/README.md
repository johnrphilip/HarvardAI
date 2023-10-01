Summary of Learning in NimAI Application
The NimAI application is a representation of a game where the AI learns to make optimal moves using Q-learning, a model-free reinforcement learning algorithm. The core learning revolves around understanding the principles of Q-learning, exploration vs exploitation, and implementing these concepts in Python.

Core Concepts Learned:
1. Q-Learning:
Definition: Q-learning is a model-free reinforcement learning algorithm used to find the optimal action-selection policy for a given finite Markov decision process.
Application: In this application, Q-learning is used to update the Q-values of (state, action) pairs, allowing the AI to learn the optimal moves over time.
2. Exploration vs Exploitation:
Definition: Exploration is the act of choosing a random action to discover its effects, while exploitation is choosing the best-known action based on current knowledge.
Application: The AI decides whether to explore or exploit based on the epsilon value. If a random number is less than epsilon, it explores; otherwise, it exploits its knowledge.
3. State and Action Representation:
Definition: States represent different situations in the game, and actions represent the possible moves that can be made from a state.
Application: In NimAI, states are represented by the tuple of remaining piles, and actions are represented by a tuple (i, j), indicating removing j items from pile i.
4. Updating Q-values:
Definition: Q-values are updated based on the reward received for an action and the maximum future reward from the new state, adjusted by a learning rate alpha.
Application: The application uses the Q-learning update rule to adjust the Q-values, allowing the AI to learn the value of different actions in various states over time.
5. Choosing Actions:
Definition: Actions are chosen based on either exploration or exploitation.
Application: The AI uses the choose_action method to decide its next move, considering whether to explore a new action or exploit its current knowledge to make the best-known move.
