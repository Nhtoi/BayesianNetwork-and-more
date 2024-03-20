import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import numpy as np
from pgmpy.inference import VariableElimination

#Kevin Ruiz - 3/1/2024

def construct_bayesian_network():
    # Define Bayesian network structure
    bayesian_network = BayesianNetwork([('Rain', 'Maintenance'), ('Rain', 'Train'), ('Maintenance', 'Train'), ('Train', 'Appointment')])
    
    # Define Conditional Probability Distributions
    cpd_rain = TabularCPD('Rain', 3, [[0.7],[0.2],[0.1]], 
                          state_names = {'Rain': ['none', 'light', 'heavy']})


    cpd_maintenance = TabularCPD('Maintenance', 2, [[0.4, 0.2, 0.1],
                                                    [0.6, 0.8, 0.9]], 
                        ['Rain'], [3],
                         state_names = {'Rain': ['none', 'light', 'heavy'], 
                                  'Maintenance': ['yes', 'no']})
                                  
    cpd_train = TabularCPD('Train', 2, [[0.8, 0.9 ,0.6, 0.7, 0.4, 0.5 ],
                                        [0.2, 0.1, 0.4, 0.3, 0.6, 0.5]],
                        ['Rain','Maintenance'], [3 , 2],
                            state_names = {'Rain': ['none', 'light', 'heavy'], 
                                         'Maintenance': ['yes', 'no'], 
                                         'Train': ['on time', 'delayed']})

    cpd_appointment = TabularCPD('Appointment', 2, [[0.9, 0.6],
                                                    [0.1, 0.4]],
                        ['Train'], [2], 
                        state_names = {'Train': ['on time', 'delayed'], 
                                     'Appointment': ['attend', 'miss']})


    bayesian_network.add_cpds(cpd_rain, cpd_maintenance, cpd_train, cpd_appointment)

    
    return bayesian_network


def visualize_bayesian_network(bayesian_network):
    # Create a NetworkX graph
    nx_bayesian_network = nx.DiGraph()

    # Add nodes
    for node in bayesian_network.nodes:
        nx_bayesian_network.add_node(node)

    # Add edges
    for edge in bayesian_network.edges:
        nx_bayesian_network.add_edge(*edge)

    # Visualize the Bayesian network
    pos = nx.spring_layout(nx_bayesian_network)
    nx.draw(nx_bayesian_network, pos, with_labels=True, arrowsize=20, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold")
    plt.title("Bayesian Network")
    plt.show()


def inference(bayesian_network, queries):
    # Perform inference on the Bayesian network
    for query in queries:
        query_variable = query[0]
        evidence = query[1]
        inference = VariableElimination(bayesian_network)
        print(f"P({query_variable} | {', '.join(evidence.keys())}) =", inference.query(variables=[query_variable], evidence=evidence))

def markov_chain_simulation(initial_state, transition_matrix, steps):
    # Simulate Markov chain
    current_state = initial_state
    for _ in range(steps):
        current_state = np.dot(current_state, transition_matrix)
    return current_state

if __name__ == "__main__":
    # Question 1: Construct and visualize the Bayesian network
    bayesian_network = construct_bayesian_network()
    visualize_bayesian_network(bayesian_network)

    # Question 2: Perform inferences
    queries = [ ('Maintenance', {'Rain': 'heavy'}), ('Appointment', {'Rain': 'none', 'Maintenance': 'no'})]
    inference(bayesian_network, queries)

    # Question 3: Markov chain simulation
    initial_state = np.array([1, 0])
    transition_matrix = np.array([[0.9, 0.1], [0.5, 0.5]])
    steps = 10
    final_state = markov_chain_simulation(initial_state, transition_matrix, steps)
    print(f"Probability distribution of 'attend' and 'miss' ten days later: {final_state}")