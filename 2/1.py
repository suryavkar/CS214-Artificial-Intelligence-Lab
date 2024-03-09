import numpy as np
import matplotlib as plt
import time
import argparse

class blockworld():
    def __init__(self, init_state, goal_state, num_stacks = 3):
        self.init_state = init_state
        self.goal_state = goal_state
        self.num_stacks = num_stacks
        self.nodes_explored = 1

    def move_gen(self, curr_state):
        possible_states = []
        for stack in range(self.num_stacks):
            if len(curr_state[stack+1]) > 0:
                tmp = curr_state
                for pos in curr_state:
                    if pos != (stack+1):
                        dic = tmp.copy()
                        dic[stack+1] = curr_state[stack+1][1:]
                        dic[pos] = [curr_state[stack+1][0]] + curr_state[pos]
                        
                        if dic not in possible_states:
                            possible_states.append(dic)
        return possible_states

    def best_state(self,curr_state, states, heuristic_fn = 1):
        best_state = {}
        if heuristic_fn == 1:
            hf = eval('self.h'+str(heuristic_fn))
            # print(hf(curr_state))
            for state in states:
                # print(hf(state))
                if hf(state) > hf(curr_state):
                    self.nodes_explored += 1
                    best_state = state
                    return best_state
            return curr_state
        
        elif heuristic_fn == 2:
            hf = eval('self.h'+str(heuristic_fn))
            # print(hf(curr_state))
            for state in states:
                # print(hf(state))
                if hf(state) > hf(curr_state):
                    self.nodes_explored += 1
                    best_state = state
                    return best_state
            return curr_state
        
        elif heuristic_fn == 3:
            hf = eval('self.h'+str(heuristic_fn))
            # print(hf(curr_state))
            for state in states:
                # print(hf(state))
                if hf(state) > hf(curr_state):
                    self.nodes_explored += 1
                    best_state = state
                    return best_state
            return curr_state

    def h1(self, state):
        """
        If any block of a stack from the current state is not in the corresponding block of the same stack from 
        the goal state, we subtract 1 from the cost. If the blocks match, we add 1 to the cost. We loop over all 
        the stacks and check using this logic to find the final cost.
        """
        cost = 0
        for pos in self.goal_state:
            index = -1
            while index >= -len(self.goal_state[pos]):
                if index < -len(state[pos]) or len(state[pos]) == 0:
                    break
                if self.goal_state[pos][index] == state[pos][index]:
                    cost += 1
                else:
                    cost -= 1
                index -= 1

            while index >= -len(self.goal_state[pos]):
                cost -= 1
                index -= 1
        return cost

    def h2(self, state):
        """
        If any block of a stack from the current state is not in the corresponding block of the same 
        stack from the goal state, we subtract the height of the block in that stack from the cost. 
        If the blocks match, we add the height of the block in that stack to the cost. We loop over 
        all the stacks and check using this logic to find the final cost.
        """
        cost = 0
        for pos in self.goal_state:
            index = -1
            while index >= -len(state[pos]):
                if index < -len(self.goal_state[pos]) or len(self.goal_state[pos]) == 0:
                    break
                if self.goal_state[pos][index] == state[pos][index]:
                    cost += abs(index)
                else:
                    cost -= abs(index)
                index -= 1

            while index >= -len(state[pos]):
                cost -= abs(index)
                index -= 1
        return cost

    def h3(self, state):
        """
        If the configuration of an entire pile on which a block is resting on is correct, 
        1 is added to the cost for every block in that pile or else 1 is subtracted from 
        the cost for every block in that pile. This logic looks at the correctness of the 
        relative position of the block rather than the individual position.
        """
        cost = 0
        for pos in self.goal_state:
            index = -1
            while index >= -len(state[pos]):
                if index < -len(self.goal_state[pos]) or len(self.goal_state[pos]) == 0:
                    break
                if self.goal_state[pos][index:] == state[pos][index:]:
                    cost += abs(index)-1
                else:
                    cost -= abs(index)-1
                index -= 1

            while index >= -len(state[pos]):
                cost -= abs(index)-1
                index -= 1
        return cost

    def Solved(self,curr_state):
        if self.goal_state == curr_state:
            return True
        return False



if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',metavar='input',required=True,choices={'1','2'},help='the input to choose')
    parser.add_argument('-hf','--hf',metavar='heuristic function',required=True,choices={'1','2','3'},help='the heuristic function to choose')
    args = parser.parse_args()

    if args.input == '1':
        init_state =  {1: ['A','B','C','D'], 2:['E','F'],3:[]}
        goal_state = {1:[],2:[],3:['D','C','F','B','E','A']}

    elif args.input == '2':
        init_state =  {1: ['A','B','C','D'], 2:['E','F'],3:[]}
        goal_state = {1: ['A','E','B','C','D'], 2:['F'],3:[]}

    print(f"\nStarting state: {init_state}\n")
    bw = blockworld(init_state, goal_state)
    curr_state = init_state
    while not bw.Solved(curr_state):
        next_states = bw.move_gen(curr_state)
        best_state = bw.best_state(curr_state,next_states,int(args.hf))
        print(f"Next possible states: \n{next_states}")
        print("Best State:", best_state,'\n')
        # break
        if curr_state == best_state:
            print("-"*50)
            print("Goal is UNREACHABLE using this heuristic function.\n")
            break
        else:
            curr_state = best_state
    
    if curr_state == goal_state:
        print("-"*50)
        print("Goal is REACHABLE using this heuristic function.\n")
    
    print("Final State:", curr_state)
    print("Goal State:", goal_state)
    print(f"\nNodes explored = {bw.nodes_explored}")
    print(f"Time taken = {(time.time()-start_time)*1000} ms")