# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            next_v = util.Counter() # temp values to store next step values (batch update)
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state): # check for TERMINAL_STATE
                    next_v[state] = self.mdp.getReward(state,'exit','')
                    continue
                # if not TERMINAL_STATE, find V*
                v_s = float('-inf')
                possible_actions = self.mdp.getPossibleActions(state)
                # loop over all possible actions and select V* as the max Q(s,a)
                for action in possible_actions:
                    q_s_a = self.computeQValueFromValues(state,action)
                    if q_s_a > v_s:
                        v_s = q_s_a
                next_v[state] = v_s
            self.values = next_v


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        next_state_prob_list = self.mdp.getTransitionStatesAndProbs(state,action)
        q_s_a = 0
        for next_state,prob_s_a in next_state_prob_list:
            reward = self.mdp.getReward(state,action,next_state)
            q_s_a += prob_s_a * (reward + self.discount * self.values[next_state])
        return q_s_a

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possible_actions = self.mdp.getPossibleActions(state)
        best_action = None
        v_star = float('-inf')
        for action in possible_actions:
            q_s_a = self.computeQValueFromValues(state,action)
            if q_s_a > v_star:
                v_star = q_s_a
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
