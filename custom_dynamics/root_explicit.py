from typing import Union
import casadi as cas
from bioptim import (
        OptimalControlProgram,
        NonLinearProgram,
        ConfigureProblem,
        DynamicsFunctions,
    )


def root_explicit_dynamic(
    states: Union[cas.MX, cas.SX],
    controls: Union[cas.MX, cas.SX],
    parameters: Union[cas.MX, cas.SX],
    nlp: NonLinearProgram,
) -> tuple:
    """
    Parameters
    ----------
    states: Union[MX, SX]
        The state of the system
    controls: Union[MX, SX]
        The controls of the system
    parameters: Union[MX, SX]
        The parameters acting on the system
    nlp: NonLinearProgram
        A reference to the phase

    Returns
    -------
    The derivative of the states in the tuple[Union[MX, SX]] format
    """

    DynamicsFunctions.apply_parameters(parameters, nlp)
    q = DynamicsFunctions.get(nlp.states["q"], states)
    qdot = DynamicsFunctions.get(nlp.states["qdot"], states)
    nb_root = nlp.model.nbRoot()

    qddot_joints = DynamicsFunctions.get(nlp.controls["qddot"], controls)[nb_root:]
    mass_matrix = nlp.model.massMatrixInverse(q).to_mx()
    mass_matrix_inverse = nlp.model.massMatrixInverse(q).to_mx()
    nl_effects = nlp.model.NonLinearEffect(q, qdot).to_mx()
    qddot_root = mass_matrix_inverse[:nb_root, :nb_root] @ \
                 (-mass_matrix[:nb_root, nb_root:] @ qddot_joints - nl_effects[:nb_root])

    return qdot, cas.vertcat(qddot_root, qddot_joints)


def custom_configure_root_explicit(ocp: OptimalControlProgram, nlp: NonLinearProgram):
    """
    Tell the program which variables are states and controls.
    The user is expected to use the ConfigureProblem.configure_xxx functions.

    Parameters
    ----------
    ocp: OptimalControlProgram
        A reference to the ocp
    nlp: NonLinearProgram
        A reference to the phase
    """

    ConfigureProblem.configure_q(nlp, as_states=True, as_controls=False)
    ConfigureProblem.configure_qdot(nlp, as_states=True, as_controls=False)
    ConfigureProblem.configure_qddot(nlp, as_states=False, as_controls=True)
    ConfigureProblem.configure_dynamics_function(ocp, nlp, root_explicit_dynamic)