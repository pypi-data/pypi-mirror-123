from __future__ import annotations

from ctypes import POINTER, Structure, c_double, c_int

import numpy as np
from numpy.ctypeslib import as_ctypes

from meshkernel.py_structures import (
    Contacts,
    GeometryList,
    Mesh1d,
    Mesh2d,
    MeshRefinementParameters,
    OrthogonalizationParameters,
)


class CMesh2d(Structure):
    """C-structure intended for internal use only.
    It represents a Mesh2D struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        edge_nodes (POINTER(c_int)): The nodes composing each mesh 2d edge.
        face_nodes (POINTER(c_int)): The nodes composing each mesh 2d face.
        nodes_per_face (POINTER(c_int)): The nodes composing each mesh 2d face.
        node_x (POINTER(c_double)): The x-coordinates of the nodes.
        node_y (POINTER(c_double)): The y-coordinates of the nodes.
        edge_x (POINTER(c_double)): The x-coordinates of the mesh edges' middle points.
        edge_y (POINTER(c_double)): The x-coordinates of the mesh edges' middle points.
        face_x (POINTER(c_double)): The x-coordinates of the mesh faces' mass centers.
        face_y (POINTER(c_double)): The y-coordinates of the mesh faces' mass centers.
        num_nodes (c_int): The number of mesh nodes.
        num_edges (c_int): The number of edges.
        num_faces (c_int): The number of faces.
        num_face_nodes (c_int): The total number of nodes composing the mesh 2d faces.
    """

    _fields_ = [
        ("edge_nodes", POINTER(c_int)),
        ("face_nodes", POINTER(c_int)),
        ("nodes_per_face", POINTER(c_int)),
        ("node_x", POINTER(c_double)),
        ("node_y", POINTER(c_double)),
        ("edge_x", POINTER(c_double)),
        ("edge_y", POINTER(c_double)),
        ("face_x", POINTER(c_double)),
        ("face_y", POINTER(c_double)),
        ("num_nodes", c_int),
        ("num_edges", c_int),
        ("num_faces", c_int),
        ("num_face_nodes", c_int),
    ]

    @staticmethod
    def from_mesh2d(mesh2d: Mesh2d) -> CMesh2d:
        """Creates a new CMesh instance from a given Mesh2d instance.

        Args:
            mesh2d (Mesh2d): Class of numpy instances owning the state.

        Returns:
            CMesh2d: The created CMesh2d instance.
        """

        c_mesh2d = CMesh2d()

        # Set the pointers
        c_mesh2d.edge_nodes = as_ctypes(mesh2d.edge_nodes)
        c_mesh2d.face_nodes = as_ctypes(mesh2d.face_nodes)
        c_mesh2d.nodes_per_face = as_ctypes(mesh2d.nodes_per_face)
        c_mesh2d.node_x = as_ctypes(mesh2d.node_x)
        c_mesh2d.node_y = as_ctypes(mesh2d.node_y)
        c_mesh2d.edge_x = as_ctypes(mesh2d.edge_x)
        c_mesh2d.edge_y = as_ctypes(mesh2d.edge_y)
        c_mesh2d.face_x = as_ctypes(mesh2d.face_x)
        c_mesh2d.face_y = as_ctypes(mesh2d.face_y)

        # Set the sizes
        c_mesh2d.num_nodes = mesh2d.node_x.size
        c_mesh2d.num_edges = mesh2d.edge_nodes.size // 2
        c_mesh2d.num_faces = mesh2d.face_x.size
        c_mesh2d.num_face_nodes = mesh2d.face_nodes.size

        return c_mesh2d

    def allocate_memory(self) -> Mesh2d:
        """Allocate data according to the parameters with the "num_" prefix.
        The pointers are then set to the freshly allocated memory.
        The memory is owned by the Mesh2d instance which is returned by this method.

        Returns:
            Mesh2d: The object owning the allocated memory.
        """

        edge_nodes = np.empty(self.num_edges * 2, dtype=np.int32)
        face_nodes = np.empty(self.num_face_nodes, dtype=np.int32)
        nodes_per_face = np.empty(self.num_faces, dtype=np.int32)
        node_x = np.empty(self.num_nodes, dtype=np.double)
        node_y = np.empty(self.num_nodes, dtype=np.double)
        edge_x = np.empty(self.num_edges, dtype=np.double)
        edge_y = np.empty(self.num_edges, dtype=np.double)
        face_x = np.empty(self.num_faces, dtype=np.double)
        face_y = np.empty(self.num_faces, dtype=np.double)

        self.edge_nodes = as_ctypes(edge_nodes)
        self.face_nodes = as_ctypes(face_nodes)
        self.nodes_per_face = as_ctypes(nodes_per_face)
        self.node_x = as_ctypes(node_x)
        self.node_y = as_ctypes(node_y)
        self.edge_x = as_ctypes(edge_x)
        self.edge_y = as_ctypes(edge_y)
        self.face_x = as_ctypes(face_x)
        self.face_y = as_ctypes(face_y)

        return Mesh2d(
            node_x,
            node_y,
            edge_nodes,
            face_nodes,
            nodes_per_face,
            edge_x,
            edge_y,
            face_x,
            face_y,
        )


class CGeometryList(Structure):
    """C-structure intended for internal use only.
    It represents a GeometryList struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        geometry_separator (c_double): The value used as a separator in the coordinates.
        inner_outer_separator (c_double): The value used to separate the inner part of a polygon from its outer part.
        n_coordinates (c_int): The number of coordinate values.
        x_coordinates (POINTER(c_double)): The x coordinates.
        y_coordinates (POINTER(c_double)): The y coordinates.
        values (POINTER(c_double)): The values on this mesh2d.
    """

    _fields_ = [
        ("geometry_separator", c_double),
        ("inner_outer_separator", c_double),
        ("n_coordinates", c_int),
        ("x_coordinates", POINTER(c_double)),
        ("y_coordinates", POINTER(c_double)),
        ("values", POINTER(c_double)),
    ]

    @staticmethod
    def from_geometrylist(geometry_list: GeometryList) -> CGeometryList:
        """Creates a new `CGeometryList` instance from the given GeometryList instance.

        Args:
            geometry_list (GeometryList): The geometry list.

        Returns:
            CGeometryList: The created C-Structure for the given GeometryList.
        """

        c_geometry_list = CGeometryList()

        c_geometry_list.geometry_separator = geometry_list.geometry_separator
        c_geometry_list.inner_outer_separator = geometry_list.inner_outer_separator
        c_geometry_list.n_coordinates = geometry_list.x_coordinates.size
        c_geometry_list.x_coordinates = as_ctypes(geometry_list.x_coordinates)
        c_geometry_list.y_coordinates = as_ctypes(geometry_list.y_coordinates)
        c_geometry_list.values = as_ctypes(geometry_list.values)

        return c_geometry_list


class COrthogonalizationParameters(Structure):
    """C-structure intended for internal use only.
    It represents an OrthogonalizationParameters struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        outer_iterations (c_int): Number of outer iterations in orthogonalization.
        boundary_iterations (c_int): Number of boundary iterations in grid/net orthogonalization within itatp.
        inner_iterations (c_int): Number of inner iterations in grid/net orthogonalization within itbnd.
        orthogonalization_to_smoothing_factor (c_double): Factor from between grid smoothing (0) and
                                                          grid orthogonality (1).
        orthogonalization_to_smoothing_factor_at_boundary (c_double): Minimum ATPF on the boundary.
        areal_to_angle_smoothing_factor (c_double): Factor between smoother 1d0 and area-homogenizer 0d0.
    """

    _fields_ = [
        ("outer_iterations", c_int),
        ("boundary_iterations", c_int),
        ("inner_iterations", c_int),
        ("orthogonalization_to_smoothing_factor", c_double),
        ("orthogonalization_to_smoothing_factor_at_boundary", c_double),
        ("areal_to_angle_smoothing_factor", c_double),
    ]

    @staticmethod
    def from_orthogonalizationparameters(
        orthogonalization_parameters: OrthogonalizationParameters,
    ) -> COrthogonalizationParameters:
        """Creates a new `COrthogonalizationParameters` instance from the given OrthogonalizationParameters instance.

        Args:
            orthogonalization_parameters (OrthogonalizationParameters): The orthogonalization parameters.

        Returns:
            COrthogonalizationParameters: The created C-Structure for the given OrthogonalizationParameters.
        """

        c_orthogonalizationparameters = COrthogonalizationParameters()
        c_orthogonalizationparameters.outer_iterations = (
            orthogonalization_parameters.outer_iterations
        )
        c_orthogonalizationparameters.boundary_iterations = (
            orthogonalization_parameters.boundary_iterations
        )
        c_orthogonalizationparameters.inner_iterations = (
            orthogonalization_parameters.inner_iterations
        )
        c_orthogonalizationparameters.orthogonalization_to_smoothing_factor = (
            orthogonalization_parameters.orthogonalization_to_smoothing_factor
        )
        c_orthogonalizationparameters.orthogonalization_to_smoothing_factor_at_boundary = (
            orthogonalization_parameters.orthogonalization_to_smoothing_factor_at_boundary
        )
        c_orthogonalizationparameters.areal_to_angle_smoothing_factor = (
            orthogonalization_parameters.areal_to_angle_smoothing_factor
        )

        return c_orthogonalizationparameters


class CMeshRefinementParameters(Structure):
    """C-structure intended for internal use only.
    It represents a MeshRefinementParameters struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        max_refinement_iterations (c_int): Maximum number of refinement iterations.
        refine_intersected (c_int): Whether to compute faces intersected by polygon (yes=1/no=0)
        use_mass_center_when_refining (c_int): Whether to use the mass center when splitting a face in the refinement
                                               process (yes=1/no=0)
        min_face_size (c_double): Minimum cell size.
        refinement_type (c_int): Refinement criterion type.
        connect_hanging_nodes (c_int): Whether to connect hanging nodes at the end of the iteration.
        account_for_samples_outside (c_int): Whether to take samples outside face into account.
    """

    _fields_ = [
        ("max_refinement_iterations", c_int),
        ("refine_intersected", c_int),
        ("use_mass_center_when_refining", c_int),
        ("min_face_size", c_double),
        ("refinement_type", c_int),
        ("connect_hanging_nodes", c_int),
        ("account_for_samples_outside_face", c_int),
    ]

    @staticmethod
    def from_meshrefinementparameters(
        mesh_refinement_parameters: MeshRefinementParameters,
    ) -> CMeshRefinementParameters:
        """Creates a new `CMeshRefinementParameters` instance from the given MeshRefinementParameters instance.

        Args:
            mesh_refinement_parameters (MeshRefinementParameters): The mesh refinement parameters.

        Returns:
            CMeshRefinementParameters: The created C-Structure for the given MeshRefinementParameters.
        """

        c_parameters = CMeshRefinementParameters()
        c_parameters.max_refinement_iterations = (
            mesh_refinement_parameters.max_refinement_iterations
        )
        c_parameters.refine_intersected = mesh_refinement_parameters.refine_intersected
        c_parameters.use_mass_center_when_refining = (
            mesh_refinement_parameters.use_mass_center_when_refining
        )
        c_parameters.min_face_size = mesh_refinement_parameters.min_face_size
        c_parameters.refinement_type = mesh_refinement_parameters.refinement_type
        c_parameters.connect_hanging_nodes = (
            mesh_refinement_parameters.connect_hanging_nodes
        )
        c_parameters.account_for_samples_outside_face = (
            mesh_refinement_parameters.account_for_samples_outside_face
        )

        return c_parameters


class CMesh1d(Structure):
    """C-structure intended for internal use only.
    It represents a Mesh1D struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        edge_nodes (POINTER(c_int)): The nodes composing each mesh 1d edge.
        node_x (POINTER(c_double)): The x-coordinates of the nodes.
        node_y (POINTER(c_double)): The y-coordinates of the nodes.
        num_nodes (c_int): The number of nodes.
        num_edges (c_int): The number of edges.
    """

    _fields_ = [
        ("edge_nodes", POINTER(c_int)),
        ("node_x", POINTER(c_double)),
        ("node_y", POINTER(c_double)),
        ("num_nodes", c_int),
        ("num_edges", c_int),
    ]

    @staticmethod
    def from_mesh1d(mesh1d: Mesh1d) -> CMesh1d:
        """Creates a new CMesh instance from a given Mesh1d instance.

        Args:
            mesh1d (Mesh1d): Class of numpy instances owning the state.

        Returns:
            CMesh1d: The created CMesh1d instance.
        """

        c_mesh1d = CMesh1d()

        # Set the pointers
        c_mesh1d.edge_nodes = as_ctypes(mesh1d.edge_nodes)
        c_mesh1d.node_x = as_ctypes(mesh1d.node_x)
        c_mesh1d.node_y = as_ctypes(mesh1d.node_y)

        # Set the sizes
        c_mesh1d.num_nodes = mesh1d.node_x.size
        c_mesh1d.num_edges = mesh1d.edge_nodes.size // 2

        return c_mesh1d

    def allocate_memory(self) -> Mesh1d:
        """Allocate data according to the parameters with the "num_" prefix.
        The pointers are then set to the freshly allocated memory.
        The memory is owned by the Mesh1d instance which is returned by this method.

        Returns:
            Mesh1d: The object owning the allocated memory.
        """

        edge_nodes = np.empty(self.num_edges * 2, dtype=np.int32)
        node_x = np.empty(self.num_nodes, dtype=np.double)
        node_y = np.empty(self.num_nodes, dtype=np.double)

        self.edge_nodes = as_ctypes(edge_nodes)
        self.node_x = as_ctypes(node_x)
        self.node_y = as_ctypes(node_y)

        return Mesh1d(
            node_x,
            node_y,
            edge_nodes,
        )


class CContacts(Structure):
    """C-structure intended for internal use only.
    It represents a Contacts struct as described by the MeshKernel API.

    Used for communicating with the MeshKernel dll.

    Attributes:
        mesh1d_indices (POINTER(c_int)): The indices of the mesh1d nodes.
        mesh2d_indices (POINTER(c_int)): The indices of the mesh2d faces.
        num_contacts (c_int): The number of contacts.
    """

    _fields_ = [
        ("mesh1d_indices", POINTER(c_int)),
        ("mesh2d_indices", POINTER(c_int)),
        ("num_contacts", c_int),
    ]

    @staticmethod
    def from_contacts(contacts: Contacts) -> CContacts:
        """Creates a new `CContacts` instance from the given Contacts instance.

        Args:
            contacts (Contacts): The contacts.

        Returns:
            CContacts: The created C-Structure for the given Contacts.
        """

        c_contacts = CContacts()

        c_contacts.mesh1d_indices = as_ctypes(contacts.mesh1d_indices)
        c_contacts.mesh2d_indices = as_ctypes(contacts.mesh2d_indices)
        c_contacts.num_contacts = contacts.mesh1d_indices.size

        return c_contacts

    def allocate_memory(self) -> Contacts:
        """Allocate data according to the parameters with the "num_" prefix.
        The pointers are then set to the freshly allocated memory.
        The memory is owned by the Contacts instance which is returned by this method.

        Returns:
            Contacts: The object owning the allocated memory.
        """

        mesh1d_indices = np.empty(self.num_contacts, dtype=np.int32)
        mesh2d_indices = np.empty(self.num_contacts, dtype=np.int32)

        self.mesh1d_indices = as_ctypes(mesh1d_indices)
        self.mesh2d_indices = as_ctypes(mesh2d_indices)

        return Contacts(mesh1d_indices, mesh2d_indices)
