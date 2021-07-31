from qiskit_optimization import QuadraticProgram
from qiskit import BasicAer
from qiskit_optimization.converters import LinearEqualityToPenalty
from qiskit.algorithms import QAOA, NumPyMinimumEigensolver,  VQE
from qiskit_optimization.algorithms import MinimumEigenOptimizer, RecursiveMinimumEigenOptimizer
from qiskit.utils import algorithm_globals,QuantumInstance
model=QuadraticProgram("boxes_program")
weights=[15., 20., 25.]
model.binary_var(name="x0")
model.binary_var(name="x1")
model.binary_var(name="x2")
# weigh each variable with its weights
model.minimize(linear=[weights[0], weights[1], weights[2]])

# implement constraint
model.linear_constraint(linear={"x0":1, "x1":1,"x2":1}, sense="==",rhs=2, name="number_of_boxes")
print(model.export_as_lp_string())
################
###following lines are not strictly necissary and can be replaced with
#qubo=model
## since the optimizer automatically converts the qubo constraints
###############
#convert constraint to penalty
lineq2penalty = LinearEqualityToPenalty()
qubo = lineq2penalty.convert(model)
#print("model to optimize")
print(qubo.export_as_lp_string())
# convert to ising model
op, offset=qubo.to_ising()
print("offset: {}".format(offset))
print("operator:")
print(op)
#######################
# solving the system exactly
exact_mes=NumPyMinimumEigensolver()
exact=MinimumEigenOptimizer(exact_mes)
exact_result=exact.solve(qubo)
print("exact result:", exact_result)
# solving the system with a quantum simulator
algorithm_globals.random_seed=10598
quantum_instance=QuantumInstance(BasicAer.get_backend("statevector_simulator"), seed_simulator=algorithm_globals.random_seed,
                                 seed_transpiler=algorithm_globals.random_seed)
qaoa_mes=QAOA(quantum_instance=quantum_instance, initial_point=[0.,0.,])
qaoa=MinimumEigenOptimizer(qaoa_mes)
qaoa_result=qaoa.solve(qubo)
print("quantum simulator (QAOA) result:", exact_result)

vqe=VQE(quantum_instance=quantum_instance)
vqe_optimizer = MinimumEigenOptimizer(vqe)

# solve quadratic program
vqe_result = vqe_optimizer.solve(qubo)
print("quantum simulator (VQE) result:", vqe_result)
