import logging
import os
from collections.abc import Iterable
from itertools import chain, groupby
from operator import attrgetter
from typing import Union

from ada.concepts.levels import FEM, Assembly, Part
from ada.concepts.points import Node
from ada.core.utils import NewLine
from ada.fem import (
    Amplitude,
    Bc,
    Connector,
    ConnectorSection,
    Constraint,
    Csys,
    Elem,
    FemSection,
    FemSet,
    FieldOutput,
    HistOutput,
    Interaction,
    InteractionProperty,
    Load,
    Mass,
    PredefinedField,
    Spring,
    Surface,
)
from ada.fem.interactions import ContactTypes
from ada.fem.steps import (
    Step,
    StepEigen,
    StepEigenComplex,
    StepExplicit,
    StepImplicit,
    StepSteadyState,
)
from ada.fem.utils import convert_ecc_to_mpc, convert_hinges_2_couplings
from ada.materials import Material
from ada.sections import GeneralProperties, Section, SectionCat

from .write_steps import AbaStep

__all__ = ["to_fem"]

log_fin = "Please check your result and input. This is not a validated method of solving this issue"

_aba_bc_map = dict(
    displacement="Displacement/Rotation",
    velocity="Velocity/Angular velocity",
    connector_displacement="Connector displacement",
    connector_velocity="Connector velocity",
)
_valid_aba_bcs = list(_aba_bc_map.values()) + [
    "symmetry/antisymmetry/encastre",
    "displacement/rotation",
    "velocity/angular velocity",
]

_step_types = Union[StepEigen, StepImplicit, StepExplicit, StepSteadyState, StepEigenComplex]


def to_fem(assembly: Assembly, name, analysis_dir=None, metadata=None):
    a = AbaqusWriter(assembly)
    a.write(name, analysis_dir, metadata)
    print(f'Created an Abaqus input deck at "{a.analysis_path}"')


class AbaqusWriter:
    _subr_path = None
    _subroutine = None
    _imperfections = str()
    _node_hist_out = ["UT", "VT", "AT"]
    _con_hist_out = ["CTF", "CVF", "CP", "CU"]
    _rf_node_out = ["RT"]
    analysis_path = None
    parts_and_assemblies = True

    def __init__(self, assembly: Assembly):
        self.assembly = assembly

    def write(self, name, analysis_dir, metadata=None):
        """Build the Abaqus Analysis folder"""
        print("creating: {0}".format(name))

        self.analysis_path = analysis_dir

        for part in self.assembly.get_all_subparts():
            if len(part.fem.elements) + len(part.fem.connectors) == 0:
                continue
            if self.assembly.convert_options.hinges_to_coupling is True:
                convert_hinges_2_couplings(part.fem)

            if self.assembly.convert_options.ecc_to_mpc is True:
                convert_ecc_to_mpc(part.fem)

            self.write_part_bulk(part)

        core_dir = self.analysis_path / r"core_input_files"
        os.makedirs(core_dir)

        # Main Input File
        with open(self.analysis_path / f"{name}.inp", "w") as d:
            d.write(self.main_inp_str)

        # Connector Sections
        with open(core_dir / "connector_sections.inp", "w") as d:
            d.write(self.connector_sections_str)

        # Connectors
        with open(core_dir / "connectors.inp", "w") as d:
            d.write(self.connectors_str if len(self.assembly.fem.connectors) > 0 else "**")

        # Constraints
        with open(core_dir / "constraints.inp", "w") as d:
            d.write(self.constraints_str if len(self.assembly.fem.constraints) > 0 else "**")

        # Assembly data
        with open(core_dir / "assembly_data.inp", "w") as d:
            if len(self.assembly.fem.nodes) > 0:
                assembly_nodes_str = (
                    "*Node\n"
                    + "".join(
                        [
                            f"{no.id:>7}, {no.x:>13.6f}, {no.y:>13.6f}, {no.z:>13.6f}\n"
                            for no in sorted(self.assembly.fem.nodes, key=attrgetter("id"))
                        ]
                    ).rstrip()
                )
            else:
                assembly_nodes_str = "** No Nodes"
            d.write(f"{assembly_nodes_str}\n{self.nsets_str}\n{self.elsets_str}\n{self.surfaces_str}\n")
            d.write(orientations_str(self.assembly, self))

        # Amplitude data
        with open(core_dir / "amplitude_data.inp", "w") as d:
            d.write(self.amplitude_str)

        # Interaction Properties
        with open(core_dir / "interaction_prop.inp", "w") as d:
            d.write(self.int_prop_str)

        # Interactions data
        self.eval_interactions()
        with open(core_dir / "interactions.inp", "a") as d:
            d.write(self.predefined_fields_str)

        # Materials data
        with open(core_dir / "materials.inp", "w") as d:
            d.write(self.materials_str)

        # Boundary Condition data
        with open(core_dir / "bc_data.inp", "w") as d:
            d.write(self.bc_str)

        # Analysis steps
        for step_in in self.assembly.fem.steps:
            self.write_step(step_in)

    def eval_interactions(self):
        if len(self.assembly.fem.steps) > 0:
            initial_step = self.assembly.fem.steps[0]
            if type(initial_step) is StepExplicit:
                for interact in self.assembly.fem.interactions.values():
                    if interact.name not in initial_step.interactions.keys():
                        initial_step.add_interaction(interact)
                        return
        with open(self.analysis_path / "core_input_files/interactions.inp", "w") as d:
            if self.interact_str != "":
                d.write(self.interact_str)
                d.write("\n")

    def write_step(self, step_in: _step_types):
        step_str = AbaStep(step_in).str
        with open(self.analysis_path / "core_input_files" / f"step_{step_in.name}.inp", "w") as d:
            d.write(step_str)
            if "*End Step" not in step_str:
                d.write("*End Step\n")

    def write_part_bulk(self, part_in: Part):
        bulk_path = self.analysis_path / f"bulk_{part_in.name}"
        bulk_file = bulk_path / "aba_bulk.inp"
        os.makedirs(bulk_path, exist_ok=True)

        if part_in.fem.initial_state is not None:
            with open(bulk_file, "w") as d:
                d.write("** This part is replaced by an initial state step")
        else:
            fempart = AbaqusPartWriter(part_in)
            with open(bulk_file, "w") as d:
                d.write(fempart.bulk_str)

    def inst_inp_str(self, part: Part) -> str:
        if part.fem.initial_state is not None:
            import shutil

            istep = part.fem.initial_state
            analysis_name = os.path.basename(istep.initial_state_file.replace(".inp", ""))
            source_dir = os.path.dirname(istep.initial_state_file)
            for f in os.listdir(source_dir):
                if analysis_name in f:
                    dest_file = os.path.join(self.analysis_path, os.path.basename(f))
                    shutil.copy(os.path.join(source_dir, f), dest_file)
            return f"""*Instance, library={analysis_name}, instance={istep.initial_state_part.fem.instance_name}
**
** PREDEFINED FIELD
**
** Name: {part.fem.initial_state.name}   Type: Initial State
*Import, state=yes, update=no
*End Instance"""
        else:
            return f"""**\n*Instance, name={part.fem.instance_name}, part={part.name}\n*End Instance"""

    @property
    def constraint_control(self):
        constraint_ctrl_on = True
        for step in self.assembly.fem.steps:
            if type(step) == StepExplicit:
                constraint_ctrl_on = False
        return "**" if constraint_ctrl_on is False else "*constraint controls, print=yes"

    @property
    def main_inp_str(self):
        """Main input file for Abaqus analysis"""
        from .templates import main_inp_str

        def skip_if_this(p):
            if p.fem.initial_state is not None:
                return False
            return len(p.fem.elements) + len(p.fem.connectors) != 0

        def inst_skip(p):
            if p.fem.initial_state is not None:
                return True
            return len(p.fem.elements) + len(p.fem.connectors) != 0

        part_str = "\n".join(map(part_inp_str, filter(skip_if_this, self.assembly.get_all_subparts())))
        instance_str = "\n".join(map(self.inst_inp_str, filter(inst_skip, self.assembly.get_all_subparts())))
        step_str = (
            "\n".join(list(map(step_inp_str, self.assembly.fem.steps))).rstrip()
            if len(self.assembly.fem.steps) > 0
            else "** No Steps added"
        )
        incl = "*INCLUDE,INPUT=core_input_files"
        ampl_str = f"\n{incl}\\amplitude_data.inp" if self.amplitude_str != "" else "**"
        consec_str = f"\n{incl}\\connector_sections.inp" if self.connector_sections_str != "" else "**"
        int_prop_str = f"{incl}\\interaction_prop.inp" if self.int_prop_str != "" else "**"
        if self.interact_str != "" or self.predefined_fields_str != "":
            interact_str = f"{incl}\\interactions.inp"
        else:
            interact_str = "**"
        mat_str = f"{incl}\\materials.inp" if self.materials_str != "" else "**"
        fix_str = f"{incl}\\bc_data.inp" if self.bc_str != "" else "**"

        return main_inp_str.format(
            part_str=part_str,
            instance_str=instance_str.rstrip(),
            mat_str=mat_str,
            fix_str=fix_str,
            step_str=step_str,
            ampl_str=ampl_str,
            consec_str=consec_str,
            int_prop_str=int_prop_str,
            interact_str=interact_str,
            constr_ctrl=self.constraint_control,
        )

    @property
    def elsets_str(self):
        return (
            "\n".join([aba_set_str(el, self) for el in self.assembly.fem.elsets.values()]).rstrip()
            if len(self.assembly.fem.elsets) > 0
            else "** No element sets"
        )

    @property
    def nsets_str(self):
        return (
            "\n".join([aba_set_str(no, self) for no in self.assembly.fem.nsets.values()]).rstrip()
            if len(self.assembly.fem.nsets) > 0
            else "** No node sets"
        )

    @property
    def materials_str(self):
        return "\n".join([material_str(mat) for mat in self.assembly.materials])

    @property
    def surfaces_str(self):
        return (
            "\n".join([surface_str(s, self) for s in self.assembly.fem.surfaces.values()])
            if len(self.assembly.fem.surfaces) > 0
            else "** No Surfaces"
        )

    @property
    def constraints_str(self):
        return (
            "\n".join([AbaConstraint(c, self).str for c in self.assembly.fem.constraints])
            if len(self.assembly.fem.constraints) > 0
            else "** No Constraints"
        )

    @property
    def connector_sections_str(self):
        return "\n".join([connector_section_str(consec) for consec in self.assembly.fem.connector_sections.values()])

    @property
    def connectors_str(self):
        return "\n".join([connector_str(con, self) for con in self.assembly.fem.connectors.values()])

    @property
    def amplitude_str(self):
        return "\n".join([amplitude_str(ampl) for ampl in self.assembly.fem.amplitudes.values()])

    @property
    def interact_str(self):
        return "\n".join([interaction_str(interact, self) for interact in self.assembly.fem.interactions.values()])

    @property
    def int_prop_str(self):
        iprop_str = "\n".join([interaction_prop_str(iprop) for iprop in self.assembly.fem.intprops.values()])
        smoothings = self.assembly.fem.metadata.get("surf_smoothing", None)
        if smoothings is not None:
            iprop_str += "\n"
            for smooth in smoothings:
                name = smooth["name"]
                iprop_str += f"*Surface Smoothing, name={name}\n"
                iprop_str += smooth["bulk"] + "\n"
        return iprop_str

    @property
    def predefined_fields_str(self):
        def eval_fields(pre_field: PredefinedField):
            return True if pre_field.type != PredefinedField.TYPES.INITIAL_STATE else False

        return "\n".join(
            [
                predefined_field_str(prefield)
                for prefield in filter(eval_fields, self.assembly.fem.predefined_fields.values())
            ]
        )

    @property
    def bc_str(self):
        return "\n".join(
            chain.from_iterable(
                (
                    [bc_str(bc, self) for bc in self.assembly.fem.bcs],
                    [bc_str(bc, self) for p in self.assembly.get_all_parts_in_assembly() for bc in p.fem.bcs],
                )
            )
        )

    def __repr__(self):
        return "AbaqusWriter()"


class AbaqusPartWriter:
    def __init__(self, part: Part):
        self.part = part

    @property
    def bulk_str(self):
        return f"""** Abaqus Part {self.part.name}
** Exported using ADA OpenSim
*NODE
{self.nodes_str}
{self.elements_str}
{self.elsets_str}
{self.nsets_str}
{self.solid_sec_str}
{self.shell_sec_str}
{self.beam_sec_str}
{self.mass_str}
{self.surfaces_str}
{self.constraints_str}
{self.springs_str}""".rstrip()

    @property
    def solid_sec_str(self):
        solid_secs = [AbaSection(sec, self).str for sec in self.part.fem.sections.solids]
        return "\n".join(solid_secs).rstrip() if len(solid_secs) > 0 else "** No solid sections"

    @property
    def shell_sec_str(self):
        shell_secs = [AbaSection(sec, self).str for sec in self.part.fem.sections.shells]
        return "\n".join(shell_secs).rstrip() if len(shell_secs) > 0 else "** No shell sections"

    @property
    def beam_sec_str(self):
        beam_secs = [AbaSection(sec, self).str for sec in self.part.fem.sections.lines]
        return "\n".join(beam_secs).rstrip() if len(beam_secs) > 0 else "** No line sections"

    @property
    def elsets_str(self):
        if len(self.part.fem.elsets) > 0:
            return "\n".join([aba_set_str(el, self) for el in self.part.fem.elsets.values()]).rstrip()
        else:
            return "** No element sets"

    @property
    def nsets_str(self):
        if len(self.part.fem.nsets) > 0:
            return "\n".join([aba_set_str(no, self) for no in self.part.fem.nsets.values()]).rstrip()
        else:
            return "** No node sets"

    @property
    def nodes_str(self):
        f = "{nid:>7}, {x:>13.6f}, {y:>13.6f}, {z:>13.6f}"
        return (
            "\n".join(
                [
                    f.format(nid=no.id, x=no[0], y=no[1], z=no[2])
                    for no in sorted(self.part.fem.nodes, key=attrgetter("id"))
                ]
            ).rstrip()
            if len(self.part.fem.nodes) > 0
            else "** No Nodes"
        )

    @property
    def elements_str(self):
        part_el = self.part.fem.elements
        grouping = groupby(part_el, key=attrgetter("type", "elset"))
        return (
            "".join([els for els in [elwriter(x, elements) for x, elements in grouping] if els is not None]).rstrip()
            if len(self.part.fem.elements) > 0
            else "** No elements"
        )

    @property
    def mass_str(self):
        return (
            "\n".join([mass_str(m) for m in self.part.fem.masses.values()])
            if len(self.part.fem.masses) > 0
            else "** No Masses"
        )

    @property
    def surfaces_str(self):
        if len(self.part.fem.surfaces) > 0:
            return "\n".join([surface_str(s, self) for s in self.part.fem.surfaces.values()])
        else:
            return "** No Surfaces"

    @property
    def constraints_str(self):
        return (
            "\n".join([AbaConstraint(c, self).str for c in self.part.fem.constraints])
            if len(self.part.fem.constraints) > 0
            else "** No Constraints"
        )

    @property
    def springs_str(self):
        return (
            "\n".join([spring_str(c) for c in self.part.fem.springs.values()])
            if len(self.part.fem.springs) > 0
            else "** No Springs"
        )

    @property
    def instance_move_str(self):
        if self.part.fem.metadata["move"] is not None:
            move = self.part.fem.metadata["move"]
            mo_str = "\n " + ", ".join([str(x) for x in move])
        else:
            mo_str = "\n 0.,        0.,           0."

        if self.part.fem.metadata["rotate"] is not None:
            rotate = self.part.fem.metadata["rotate"]
            vecs = ", ".join([str(x) for x in rotate[0]])
            vece = ", ".join([str(x) for x in rotate[1]])
            angle = rotate[2]
            move_str = """{move_str}\n {vecs}, {vece}, {angle}""".format(
                move_str=mo_str, vecs=vecs, vece=vece, angle=angle
            )
        else:
            move_str = "" if mo_str == "0.,        0.,           0." else mo_str
        return move_str


class AbaSection:
    def __init__(self, fem_sec: FemSection, fem_writer):
        self.fem_sec = fem_sec
        self._fem_writer = fem_writer

    @property
    def _temp_str(self):
        _temperature = self.fem_sec.metadata["temperature"] if "temperature" in self.fem_sec.metadata.keys() else None
        return _temperature if _temperature is not None else "GRADIENT"

    @property
    def section_data(self):
        if "section_type" in self.fem_sec.metadata.keys():
            return self.fem_sec.metadata["section_type"]
        sec_type = self.fem_sec.section.type
        from ada.sections.categories import BaseTypes

        bt = BaseTypes
        base_type = SectionCat.get_shape_type(self.fem_sec.section)
        sec_map = {
            bt.CIRCULAR: "CIRC",
            bt.IPROFILE: "I",
            bt.BOX: "BOX",
            bt.GENERAL: "GENERAL",
            bt.TUBULAR: "PIPE",
            bt.ANGULAR: "L",
            bt.CHANNEL: "GENERAL",
            bt.FLATBAR: "RECT",
        }
        sec_str = sec_map.get(base_type, None)
        if sec_str is None:
            raise Exception(f'Section type "{sec_type}" is not added to Abaqus beam export yet')

        if base_type in [bt.CHANNEL]:
            logging.error(f'Profile type "{sec_type}" is not supported by Abaqus. Using a General Section instead')

        return sec_str

    @property
    def props(self):
        """
        To understand the local coordinate system and n1 direction

        https://abaqus-docs.mit.edu/2017/English/SIMACAEELMRefMap/simaelm-c-beamcrosssection.htm
        """

        n1 = ", ".join(str(x) for x in self.fem_sec.local_y)
        if "line1" in self.fem_sec.metadata.keys():
            return self.fem_sec.metadata["line1"] + f"\n{n1}"

        sec = self.fem_sec.section
        sec_data = self.section_data

        if sec_data == "CIRC":
            return f"{sec.r}\n {n1}"
        elif sec_data == "I":
            if sec.t_fbtn + sec.t_w > min(sec.w_top, sec.w_btn):
                new_width = sec.t_fbtn + sec.t_w + 5e-3
                if sec.w_btn == min(sec.w_top, sec.w_btn):
                    sec.w_btn = new_width
                else:
                    sec.w_top = new_width
                logging.error(f"For {self.fem_sec.name}: t_fbtn + t_w > min(w_top, w_btn). {log_fin}")
            return f"{sec.h / 2}, {sec.h}, {sec.w_btn}, {sec.w_top}, {sec.t_fbtn}, {sec.t_ftop}, {sec.t_w}\n {n1}"
        elif sec_data == "BOX":
            if sec.t_w * 2 > min(sec.w_top, sec.w_btn):
                raise ValueError("Web thickness cannot be larger than section width")
            return f"{sec.w_top}, {sec.h}, {sec.t_w}, {sec.t_ftop}, {sec.t_w}, {sec.t_fbtn}\n {n1}"
        elif sec_data == "GENERAL":
            mat = self.fem_sec.material.model
            gp = eval_general_properties(sec)
            return f"{gp.Ax}, {gp.Iy}, {gp.Iyz}, {gp.Iz}, {gp.Ix}\n {n1}\n {mat.E:.3E}, {mat.G},{mat.alpha:.2E}"
        elif sec_data == "PIPE":
            return f"{sec.r}, {sec.wt}\n {n1}"
        elif sec_data == "L":
            return f"{sec.w_btn}, {sec.h}, {sec.t_fbtn}, {sec.t_w}\n {n1}"
        elif sec_data == "RECT":
            return f"{sec.w_btn}, {sec.h}\n {n1}"
        else:
            raise NotImplementedError(f'section type "{sec.type}" is not added to Abaqus export yet')

    @property
    def beam_str(self):
        """
        BOX, CIRC, HEX, I, L, PIPE, RECT, THICK PIPE, and TRAPEZOID sections
        https://abaqus-docs.mit.edu/2017/English/SIMACAEKEYRefMap/simakey-r-beamsection.htm


        General Section
        https://abaqus-docs.mit.edu/2017/English/SIMACAEKEYRefMap/simakey-r-beamgeneralsection.htm#simakey-r-beamgeneralsection__simakey-r-beamgeneralsection-s-datadesc1


        Comment regarding Rotary Inertia and Explicit analysis
        https://abaqus-docs.mit.edu/2017/English/SIMACAEELMRefMap/simaelm-c-beamsectionbehavior.htm#hj-top

        """
        top_line = f"** Section: {self.fem_sec.elset.name}  Profile: {self.fem_sec.elset.name}"
        density = self.fem_sec.material.model.rho if self.fem_sec.material.model.rho > 0.0 else 1e-4
        ass = self.fem_sec.parent.parent.get_assembly()

        rotary_str = ""
        if len(ass.fem.steps) > 0:
            initial_step = ass.fem.steps[0]
            if type(initial_step) is StepExplicit:
                rotary_str = ", ROTARY INERTIA=ISOTROPIC"
        sec_data = self.section_data
        if sec_data != "GENERAL":
            return (
                f"{top_line}\n*Beam Section, elset={self.fem_sec.elset.name}, material={self.fem_sec.material.name}, "
                f"temperature={self._temp_str}, section={sec_data}{rotary_str}\n{self.props}"
            )
        else:
            return f"""{top_line}
*Beam General Section, elset={self.fem_sec.elset.name}, section=GENERAL{rotary_str}, density={density}
 {self.props}"""

    @property
    def shell_str(self):
        return f"""** Section: {self.fem_sec.name}
*Shell Section, elset={self.fem_sec.elset.name}, material={self.fem_sec.material.name}
 {self.fem_sec.thickness}, {self.fem_sec.int_points}"""

    @property
    def solid_str(self):
        return f"""** Section: {self.fem_sec.name}
*Solid Section, elset={self.fem_sec.elset.name}, material={self.fem_sec.material.name}
,"""

    @property
    def str(self):
        if self.fem_sec.type == Elem.EL_TYPES.SOLID:
            return self.solid_str
        elif self.fem_sec.type == Elem.EL_TYPES.SHELL:
            return self.shell_str
        elif self.fem_sec.type == Elem.EL_TYPES.LINE:
            return self.beam_str
        else:
            raise ValueError()


def eval_general_properties(section: Section) -> GeneralProperties:
    gp = section.properties
    name = gp.parent.parent.name
    if gp.Ix <= 0.0:
        gp.Ix = 1
        logging.error(f"Section {name} Ix <= 0.0. Changing to 2. {log_fin}")
    if gp.Iy <= 0.0:
        gp.Iy = 2
        logging.error(f"Section {name} Iy <= 0.0. Changing to 2. {log_fin}")
    if gp.Iz <= 0.0:
        gp.Iz = 2
        logging.error(f"Section {name} Iz <= 0.0. Changing to 2. {log_fin}")
    if gp.Iyz <= 0.0:
        gp.Iyz = (gp.Iy + gp.Iz) / 2
        logging.error(f"Section {name} Iyz <= 0.0. Changing to (Iy + Iz) / 2. {log_fin}")
    if gp.Iy * gp.Iz - gp.Iyz ** 2 < 0:
        old_y = str(gp.Iy)
        gp.Iy = 1.1 * (gp.Iy + (gp.Iyz ** 2) / gp.Iz)
        logging.error(
            f"Warning! Section {name}: I(11)*I(22)-I(12)**2 MUST BE POSITIVE. " f"Mod Iy={old_y} to {gp.Iy}. {log_fin}"
        )
    if (-(gp.Iy + gp.Iz) / 2 < gp.Iyz <= (gp.Iy + gp.Iz) / 2) is False:
        raise ValueError("Iyz must be between -(Iy+Iz)/2 and (Iy+Iz)/2")
    return gp


class AbaConstraint:
    """

    Coupling definition:
    https://abaqus-docs.mit.edu/2017/English/SIMACAEKEYRefMap/simakey-r-coupling.htm#simakey-r-coupling

    """

    def __init__(self, constraint: Constraint, fem_writer):
        self.constraint = constraint
        self._fem_writer = fem_writer

    @property
    def _coupling(self):
        dofs_str = "".join(
            [f" {x[0]}, {x[1]}\n" if type(x) != int else f" {x}, {x}\n" for x in self.constraint.dofs]
        ).rstrip()

        if type(self.constraint.s_set) is FemSet:
            new_surf = surface_str(
                Surface(
                    f"{self.constraint.name}_surf",
                    Surface.TYPES.NODE,
                    self.constraint.s_set,
                    1.0,
                    parent=self.constraint.s_set.parent,
                ),
                self._fem_writer,
            )
            surface_ref = f"{self.constraint.name}_surf"
            add_str = new_surf
        else:
            add_str = "**"
            surface_ref = get_instance_name(self.constraint.s_set, self._fem_writer)

        if self.constraint.csys is not None:
            new_csys_str = "\n" + csys_str(self.constraint.csys, self._fem_writer)
            cstr = f", Orientation={self.constraint.csys.name.upper()}"
        else:
            cstr = ""
            new_csys_str = ""

        rnode = f"{get_instance_name(self.constraint.m_set.members[0], self._fem_writer)}"
        return f"""** ----------------------------------------------------------------
** Coupling element {self.constraint.name}
** ----------------------------------------------------------------{new_csys_str}
** COUPLING {self.constraint.name}
{add_str}
*COUPLING, CONSTRAINT NAME={self.constraint.name}, REF NODE={rnode}, SURFACE={surface_ref}{cstr}
*KINEMATIC
{dofs_str}""".rstrip()

    @property
    def _mpc(self):
        mpc_type = self.constraint.mpc_type
        m_members = self.constraint.m_set.members
        s_members = self.constraint.s_set.members
        mpc_vars = "\n".join([f" {mpc_type},{m.id:>8},{s.id:>8}" for m, s in zip(m_members, s_members)])
        return f"** Constraint: {self.constraint.name}\n*MPC\n{mpc_vars}"

    @property
    def _shell2solid(self):
        mname = self.constraint.m_set.name
        sname = self.constraint.s_set.name
        influence = self.constraint.influence_distance
        influence_str = "" if influence is None else f", influence distance={influence}"
        return (
            f"** Constraint: {self.constraint.name}\n*Shell to Solid Coupling, "
            f"constraint name={self.constraint.name}{influence_str}\n{mname}, {sname}"
        )

    @property
    def str(self):
        if self.constraint.type == Constraint.TYPES.COUPLING:
            return self._coupling
        elif self.constraint.type == Constraint.TYPES.TIE:
            return _tie(self.constraint)
        elif self.constraint.type == Constraint.TYPES.RIGID_BODY:
            rnode = get_instance_name(self.constraint.m_set, self)
            return f"*Rigid Body, ref node={rnode}, elset={get_instance_name(self.constraint.s_set, self)}"
        elif self.constraint.type == Constraint.TYPES.MPC:
            return self._mpc
        elif self.constraint.type == Constraint.TYPES.SHELL2SOLID:
            return self._shell2solid
        else:
            raise NotImplementedError(f"{self.constraint.type}")


def step_inp_str(step: _step_types) -> str:
    return f"""*INCLUDE,INPUT=core_input_files\\step_{step.name}.inp"""


def part_inp_str(part: Part) -> str:
    return """**\n*Part, name={name}\n*INCLUDE,INPUT=bulk_{name}\\{inp_file}\n*End Part\n**""".format(
        name=part.name, inp_file="aba_bulk.inp"
    )


def _tie(constraint: Constraint) -> str:
    num = 80
    pos_tol_str = ""
    if constraint.pos_tol is not None:
        pos_tol_str = f", position tolerance={constraint.pos_tol},"

    coupl_text = "**" + num * "-" + """\n** COUPLING {}\n""".format(constraint.name) + "**" + num * "-" + "\n"
    name = constraint.name

    adjust = constraint.metadata.get("adjust", "no")

    coupl_text += f"""** Constraint: {name}
*Tie, name={name}, adjust={adjust}{pos_tol_str}
{constraint.m_set.name}, {constraint.s_set.name}"""
    return coupl_text


def aba_write(el: Elem):
    nl = NewLine(10, suffix=7 * " ")
    if len(el.nodes) > 6:
        di = " {}"
    else:
        di = "{:>13}"
    return f"{el.id:>7}, " + " ".join([f"{di.format(no.id)}," + next(nl) for no in el.nodes])[:-1]


def elwriter(eltype_set, elements):
    if "connector" in eltype_set:
        return None
    eltype, elset = eltype_set
    el_set_str = f", ELSET={elset.name}" if elset is not None else ""
    el_str = "\n".join(map(aba_write, elements))
    return f"""*ELEMENT, type={eltype}{el_set_str}\n{el_str}\n"""


def interaction_str(interaction: Interaction, fem_writer) -> str:
    # Allowing Free text to be parsed directly through interaction class.
    if "aba_bulk" in interaction.metadata.keys():
        return interaction.metadata["aba_bulk"]

    contact_mod = interaction.metadata["contact_mod"] if "contact_mod" in interaction.metadata.keys() else "NEW"
    contact_incl = (
        interaction.metadata["contact_inclusions"]
        if "contact_inclusions" in interaction.metadata.keys()
        else "ALL EXTERIOR"
    )

    top_str = f"**\n** Interaction: {interaction.name}"
    if interaction.type == ContactTypes.SURFACE:
        adjust_par = interaction.metadata.get("adjust", None)
        geometric_correction = interaction.metadata.get("geometric_correction", None)
        small_sliding = interaction.metadata.get("small_sliding", None)

        first_line = "" if small_sliding is None else f", {small_sliding}"

        if issubclass(type(interaction.parent), Step):
            step = interaction.parent
            first_line += "" if type(step) is StepExplicit else f", type={interaction.surface_type}"
        else:
            first_line += f", type={interaction.surface_type}"

        if interaction.constraint is not None:
            first_line += f", mechanical constraint={interaction.constraint}"

        if adjust_par is not None:
            first_line += f", adjust={adjust_par}" if adjust_par is not None else ""

        if geometric_correction is not None:
            first_line += f", geometric correction={geometric_correction}"

        return f"""{top_str}
*Contact Pair, interaction={interaction.interaction_property.name}{first_line}
{get_instance_name(interaction.surf1, fem_writer)}, {get_instance_name(interaction.surf2, fem_writer)}"""
    else:
        return f"""{top_str}\n*Contact, op={contact_mod}
*Contact Inclusions, {contact_incl}
*Contact Property Assignment
 ,  , {interaction.interaction_property.name}"""


def material_str(material: Material) -> str:
    if "aba_inp" in material.metadata.keys():
        return material.metadata["aba_inp"]
    if "rayleigh_damping" in material.metadata.keys():
        alpha, beta = material.metadata["rayleigh_damping"]
    else:
        alpha, beta = None, None

    no_compression = material.metadata["no_compression"] if "no_compression" in material.metadata.keys() else False
    compr_str = "\n*No Compression" if no_compression is True else ""

    if material.model.eps_p is not None and len(material.model.eps_p) != 0:
        pl_str = "\n*Plastic\n"
        pl_str += "\n".join(
            ["{x:>12.5E}, {y:>10}".format(x=x, y=y) for x, y in zip(material.model.sig_p, material.model.eps_p)]
        )
    else:
        pl_str = ""

    if alpha is not None and beta is not None:
        d_str = "\n*Damping, alpha={alpha}, beta={beta}".format(alpha=material.model.alpha, beta=material.model.beta)
    else:
        d_str = ""

    if material.model.zeta is not None and material.model.zeta != 0.0:
        exp_str = "\n*Expansion\n {zeta}".format(zeta=material.model.zeta)
    else:
        exp_str = ""

    # Density == 0.0 is unsupported
    density = material.model.rho if material.model.rho > 0.0 else 1e-6

    return f"""*Material, name={material.name}
*Elastic
{material.model.E:.6E},  {material.model.v}{compr_str}
*Density
{density},{exp_str}{d_str}{pl_str}"""


def amplitude_str(amplitude: Amplitude) -> str:
    name, x, y, smooth = amplitude.name, amplitude.x, amplitude.y, amplitude.smooth
    a = 1
    data = ""
    for i, var in enumerate(zip(list(x), list(y))):
        if a == 4:
            if i == len(list(x)) - 1:
                data += "{:.4E}, {:.4E}, ".format(var[0], var[1])
            else:
                data += "{:.4E}, {:.4E},\n         ".format(var[0], var[1])
            a = 0
        else:
            data += "{:.4E}, {:.4E}, ".format(var[0], var[1])
        a += 1

    smooth = ", DEFINITION=TABULAR, SMOOTH={}".format(smooth) if smooth is not None else ""
    amplitude = """*Amplitude, name={0}{2}\n         {1}\n""".format(name, data, smooth)
    return amplitude.rstrip()


def connector_str(connector: Connector, fem_writer) -> str:
    csys_ref = "" if connector.csys is None else f'\n "{connector.csys.name}",'

    end1 = get_instance_name(connector.n1, fem_writer)
    end2 = get_instance_name(connector.n2, fem_writer)
    return f"""**
** ----------------------------------------------------------------
** Connector element representing {connector.name}
** ----------------------------------------------------------------
**
*Elset, elset={connector.name}
 {connector.id},
*Element, type=CONN3D2
 {connector.id}, {end1}, {end2}
*Connector Section, elset={connector.name}, behavior={connector.con_sec.name}
 {connector.con_type},{csys_ref}
*Elset, elset={connector.name}_set
 {connector.id}
**
{csys_str(connector.csys, fem_writer)}
**"""


def connector_section_str(con_sec: ConnectorSection):
    """

    :param con_sec:
    :type con_sec: ada.fem.ConnectorSection
    :return:
    """

    conn_txt = """*Connector Behavior, name={0}""".format(con_sec.name)
    elast = con_sec.elastic_comp
    damping = con_sec.damping_comp
    plastic_comp = con_sec.plastic_comp
    rigid_dofs = con_sec.rigid_dofs
    soft_elastic_dofs = con_sec.soft_elastic_dofs
    if type(elast) is float:
        conn_txt += """\n*Connector Elasticity, component=1\n{0:.3E},""".format(elast)
    else:
        for i, comp in enumerate(elast):
            if isinstance(comp, Iterable) is False:
                conn_txt += """\n*Connector Elasticity, component={1} \n{0:.3E},""".format(comp, i + 1)
            else:
                conn_txt += f"\n*Connector Elasticity, nonlinear, component={i + 1}, DEPENDENCIES=1"
                for val in comp:
                    conn_txt += "\n" + ", ".join([f"{x:>12.3E}" if u <= 1 else f",{x:>12d}" for u, x in enumerate(val)])

    if type(damping) is float:
        conn_txt += """\n*Connector Damping, component=1\n{0:.3E},""".format(damping)
    else:
        for i, comp in enumerate(damping):
            if type(comp) is float:
                conn_txt += """\n*Connector Damping, component={1} \n{0:.3E},""".format(comp, i + 1)
            else:
                conn_txt += """\n*Connector Damping, nonlinear, component=1, DEPENDENCIES=1"""
                for val in comp:
                    conn_txt += "\n" + ", ".join(
                        ["{:>12.3E}".format(x) if u <= 1 else ",{:>12d}".format(x) for u, x in enumerate(val)]
                    )

    # Optional Choices
    if plastic_comp is not None:
        for i, comp in enumerate(plastic_comp):
            conn_txt += """\n*Connector Plasticity, component={}\n*Connector Hardening, definition=TABULAR""".format(
                i + 1
            )
            for val in comp:
                force, motion, rate = val
                conn_txt += "\n{}, {}, {}".format(force, motion, rate)

    if rigid_dofs is not None:
        conn_txt += "\n*Connector Elasticity, rigid\n "
        conn_txt += ", ".join(["{0}".format(x) for x in rigid_dofs])

    if soft_elastic_dofs is not None:
        for dof in soft_elastic_dofs:
            conn_txt += "\n*Connector Elasticity, component={0}\n 5.0,\n".format(dof)

    return conn_txt


def interaction_prop_str(int_prop: InteractionProperty):
    """

    :param int_prop:
    :type int_prop: ada.fem.InteractionProperty
    :return:
    """
    iprop_str = f"*Surface Interaction, name={int_prop.name}\n"

    # Friction
    iprop_str += f"*Friction\n{int_prop.friction},\n"

    # Behaviours
    tab_str = (
        "\n" + "\n".join(["{:>12.3E},{:>12.3E}".format(d[0], d[1]) for d in int_prop.tabular])
        if int_prop.tabular is not None
        else ""
    )
    iprop_str += f"*Surface Behavior, pressure-overclosure={int_prop.pressure_overclosure}{tab_str}"

    return iprop_str.rstrip()


def surface_str(surface: Surface, fem_writer):
    """

    :param surface:
    :param fem_writer:
    :type surface: ada.fem.Surface
    :return:
    """
    top_line = f"*Surface, type={surface.type}, name={surface.name}"

    if surface.id_refs is None:
        if surface.type == "NODE":
            add_str = surface.weight_factor
        else:
            add_str = surface.face_id_label
        # if surface.fem_set.name in surface.parent.elsets.keys():
        #     return f"{top_line}\n{surface.fem_set.name}, {add_str}"
        # else:
        return f"""{top_line}\n{get_instance_name(surface.fem_set, fem_writer)}, {add_str}"""
    else:
        id_refs_str = "\n".join([f"{m[0]}, {m[1]}" for m in surface.id_refs]).strip()
        return f"""{top_line}\n{id_refs_str}"""


def bc_str(bc: Bc, fem_writer) -> str:
    ampl_ref_str = "" if bc.amplitude_name is None else ", amplitude=" + bc.amplitude_name
    fem_set = bc.fem_set
    inst_name = get_instance_name(fem_set, fem_writer)

    if bc.type in _valid_aba_bcs:
        aba_type = bc.type
    else:
        aba_type = _aba_bc_map[bc.type]

    dofs_str = ""
    for dof, magn in zip(bc.dofs, bc.magnitudes):
        if dof is None:
            continue
        magn_str = f", {magn:.6E}" if magn is not None else ""
        if bc.type in [Bc.TYPES.CONN_DISPL, Bc.TYPES.CONN_VEL] or type(dof) is str:
            dofs_str += f" {inst_name}, {dof}{magn_str}\n"
        else:
            dofs_str += f" {inst_name}, {dof}, {dof}{magn_str}\n"

    dofs_str = dofs_str.rstrip()
    add_map = {
        Bc.TYPES.CONN_DISPL: ("*Connector Motion", ", type=DISPLACEMENT"),
        Bc.TYPES.CONN_VEL: ("*Connector Motion", ", type=VELOCITY"),
    }

    if bc.type in add_map.keys():
        bcstr, add_str = add_map[bc.type]
    else:
        bcstr, add_str = "*Boundary", ""

    return f"""** Name: {bc.name} Type: {aba_type}
{bcstr}{ampl_ref_str}{add_str}
{dofs_str}"""


def mass_str(mass: Mass) -> str:
    type_str = f", type={mass.point_mass_type}" if mass.point_mass_type is not None else ""
    mstr = ",".join([str(x) for x in mass.mass]) if type(mass.mass) is list else str(mass.mass)

    if mass.type == Mass.TYPES.MASS:
        return f"""*Mass, elset={mass.fem_set.name}{type_str}\n {mstr}"""
    elif mass.type == Mass.TYPES.NONSTRU:
        return f"""*Nonstructural Mass, elset={mass.fem_set.name}, units={mass.units}\n  {mstr}"""
    elif mass.type == Mass.TYPES.ROT_INERTIA:
        return f"""*Rotary Inertia, elset={mass.fem_set.name}\n  {mstr}"""
    else:
        raise ValueError(f'Mass type "{mass.type}" is not supported by Abaqus')


def aba_set_str(aba_set: FemSet, fem_writer=None):
    if len(aba_set.members) == 0:
        if "generate" in aba_set.metadata.keys():
            if aba_set.metadata["generate"] is False:
                raise ValueError(f'set "{aba_set.name}" is empty. Please check your input')
        else:
            raise ValueError("No Members are found")

    generate = aba_set.metadata.get("generate", False)
    internal = aba_set.metadata.get("internal", False)
    newline = NewLine(15)

    el_str = "*Elset, elset" if aba_set.type == FemSet.TYPES.ELSET else "*Nset, nset"

    el_instances = dict()

    for parent, mem in groupby(aba_set.members, key=attrgetter("parent")):
        el_instances[parent.name] = list(mem)

    set_str = ""
    for elinst, members in el_instances.items():
        el_root = f"{el_str}={aba_set.name}"
        if type(fem_writer) in (AbaqusWriter, AbaStep):
            if internal is True:
                el_root += "" if "," in el_str[-2] else ", "
                el_root += "internal"
            if elinst != aba_set.parent.name:
                el_root += "" if "," in el_str[-2] else ", "
                el_root += f"instance={elinst}"

        if generate is True:
            assert len(aba_set.metadata["gen_mem"]) == 3
            el_root += "" if "," in el_root[-2] else ", "
            set_str += (
                el_root + "generate\n {},  {},   {}" "".format(*[no for no in aba_set.metadata["gen_mem"]]) + "\n"
            )
        else:
            set_str += el_root + "\n " + " ".join([f"{no.id}," + next(newline) for no in members]).rstrip()[:-1] + "\n"
    return set_str.rstrip()


def orientations_str(assembly: Assembly, fem_writer) -> str:
    """Add orientations associated with loads"""
    cstr = "** Orientations associated with Loads"
    for step in assembly.fem.steps:
        for load in step.loads:
            if load.csys is None:
                continue
            cstr += "\n"
            coord_str = ", ".join([str(x) for x in chain.from_iterable(load.csys.coords)])[:-1]
            name = load.fem_set.name.upper()
            inst_name = get_instance_name(load.fem_set, fem_writer)
            cstr += f"*Nset, nset=_T-{name}, internal\n{inst_name},\n"
            cstr += f"*Transform, nset=_T-{name}\n{coord_str}\n"
            cstr += csys_str(load.csys, fem_writer)

    return cstr.strip()


def csys_str(csys: Csys, fem_writer):
    name = csys.name.replace('"', "").upper()
    ori_str = f'*Orientation, name="{name}"'
    if csys.nodes is None and csys.coords is None:
        ori_str += "\n 1.,           0.,           0.,           0.,           1.,           0.\n 1, 0."
    elif csys.nodes is not None:
        if len(csys.nodes) != 3:
            raise ValueError("CSYS number of nodes must be 3")
        ori_str += ", SYSTEM=RECTANGULAR, DEFINITION=NODES\n {},{},{}".format(
            *[get_instance_name(no, fem_writer) for no in csys.nodes]
        )
    else:
        ax, ay, az = csys.coords[0]
        ori_str += f" \n{ax}, {ay}, {az}"
        bx, by, bz = csys.coords[1]
        ori_str += f", {bx}, {by}, {bz}"
        if len(csys.coords) == 3:
            cx, cy, cz = csys.coords[2]
            ori_str += f", {cx}, {cy}, {cz}"
        ori_str += "\n 1, 0."
    return ori_str


def hist_output_str(hist_output: HistOutput) -> str:
    hist_map = dict(
        connector="*Element Output, elset=",
        node="*Node Output, nset=",
        energy="*Energy Output",
        contact="*Contact Output",
    )

    if hist_output.type not in hist_map.keys():
        raise Exception('Unknown output type "{}"'.format(hist_output.type))

    set_type_str = hist_map[hist_output.type]
    newline = NewLine(10)
    var_str = "".join([" {},".format(val) + next(newline) for val in hist_output.variables])[:-1]

    if hist_output.type == HistOutput.TYPES.CONTACT:
        iname1 = get_instance_name(hist_output.fem_set[1], hist_output.parent)
        iname2 = get_instance_name(hist_output.fem_set[0], hist_output.parent)
        fem_set_str = f", master={iname1}, slave={iname2}"
    else:
        fem_set_str = "" if hist_output.fem_set is None else get_instance_name(hist_output.fem_set, hist_output.parent)
    return f"""*Output, history, {hist_output.int_type}={hist_output.int_value}
** HISTORY OUTPUT: {hist_output.name}
**
{set_type_str}{fem_set_str}
{var_str}"""


def field_output_str(field_output: FieldOutput) -> str:
    if len(field_output.nodal) > 0:
        nodal_str = "*Node Output\n "
        nodal_str += ", ".join([str(val) for val in field_output.nodal])
    else:
        nodal_str = "** No Nodal Output"

    if len(field_output.element) > 0:
        element_str = "*Element Output, directions=YES\n "
        element_str += ", ".join([str(val) for val in field_output.element])
    else:
        element_str = "** No Element Output"

    if len(field_output.contact) > 0:
        contact_str = "*Contact Output\n "
        contact_str += ", ".join([str(val) for val in field_output.contact])
    else:
        contact_str = "** No Contact Output"
    return f"""** FIELD OUTPUT: {field_output.name}
**
*Output, field, {field_output.int_type}={field_output.int_value}
{nodal_str}
{element_str}
{contact_str}""".strip()


def predefined_field_str(pre_field: PredefinedField) -> str:
    dofs_str = ""
    for dof, magn in zip(pre_field.dofs, pre_field.magnitude):
        if float(magn) == 0.0:
            continue
        dofs_str += f"{get_instance_name(pre_field.fem_set, pre_field)}, {dof}, {magn}\n"
    dofs_str.rstrip()
    return f"""** PREDEFINED FIELDS
**
** Name: {pre_field.name}   Type: {pre_field.type}
*Initial Conditions, type={pre_field.type}
{dofs_str}"""


def spring_str(spring: Spring) -> str:
    from ada.fem.shapes import ElemShapes

    if spring.type in ElemShapes.spring1n:
        _str = f'** Spring El "{spring.name}"\n\n'
        for dof, row in enumerate(spring.stiff):
            for j, stiffness in enumerate(row):
                if dof == j:
                    _str += f"""*Spring, elset={spring.fem_set.name}
 {dof + 1}
 {stiffness:.6E}
{spring.id}, {spring.nodes[0].id}\n"""
        return _str.rstrip()
    else:
        raise ValueError(f'Currently unsupported spring type "{spring.type}"')


def get_instance_name(obj, fem_writer: Union[Step, Load, AbaqusWriter, AbaConstraint, AbaStep, PredefinedField]) -> str:
    if type(obj) is Node:
        obj_ref = obj.id
        if type(obj.parent.parent) is Assembly:
            assembly_level = True
        else:
            assembly_level = False
    else:
        obj_ref = obj.name
        assembly_level = on_assembly_level(obj)

    if fem_writer is Load and assembly_level is False:
        return f"{obj.parent.instance_name}.{obj_ref}"
    elif issubclass(type(fem_writer), Step) and assembly_level is False:
        return f"{obj.parent.instance_name}.{obj_ref}"
    elif type(obj.parent.parent) != Assembly and type(fem_writer) in (AbaqusWriter, AbaConstraint, AbaStep):
        return f"{obj.parent.instance_name}.{obj_ref}"
    else:
        return str(obj_ref)


def on_assembly_level(obj: FEM):
    # TODO: This is not really working correctly. This must be fixed
    return True if type(obj.parent.parent) is Assembly else False
