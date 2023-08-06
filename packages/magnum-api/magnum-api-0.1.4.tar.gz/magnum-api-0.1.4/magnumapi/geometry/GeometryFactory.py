from enum import Enum, auto
from typing import List, Dict, Type
import json

import pandas as pd

from magnumapi.geometry.SlottedGeometry import SlottedGeometry, SlottedRelativeCosThetaGeometry
from magnumapi.geometry.blocks.CosThetaBlock import AbsoluteCosThetaBlock, RelativeCosThetaBlock
from magnumapi.geometry.Geometry import Geometry, RelativeCosThetaGeometry
from magnumapi.geometry.blocks.RectangularBlock import RectangularBlock
from magnumapi.geometry.definitions.AbsoluteCosThetaBlockDefinition import AbsoluteCosThetaBlockDefinition
from magnumapi.geometry.definitions.LayerDefinition import LayerDefinition, SlottedLayerDefinition
from magnumapi.geometry.definitions.RectangularBlockDefinition import RectangularBlockDefinition
from magnumapi.geometry.definitions.RelativeCosThetaBlockDefinition import RelativeCosThetaBlockDefinition
from magnumapi.cadata.CableDatabase import CableDatabase
import magnumapi.tool_adapters.roxie.RoxieAPI as RoxieAPI


# ToDo: BuilderDesign pattern:
# - with_geometry_type - use single dispatch mechanism (dict or dataframe as input; ABSOLUTE, RELATIVE as output) - this actually is deduced when block def is provided
# - with_aperture_radius - either a value or none
# - with_block_definition - use a single dispatch mechanism (dict or dataframe or list of definitions as input; List of Block definitions as output) - from that one can deduce what is the geometry type - get_keys() also as a single dispatch
# - with_layer_definition - use a single dispatch mechanism (dict or dataframe or list of defitnitions as input; List of Layer definitions as output) - from that one can deduce what is the layer type
# use generators to iterate over a dict and a dataframe to use the same for loop!!! - also with a single dispatch mechanism for the generator
# param = {'block_defs': self.block_defs, 'layer_defs': self.layer_defs}
# if self.r_aperture:
#     param['r_aperture'] = r_aperture
# return object_dct[geometry_type](**param)
# geometry_type is 'Absolute, Relative, SlottedAbsolute, SlottedRelative'

class GeometryType(Enum):
    """GeometryType is an enum type used to distinguish between an absolute and relative geometry.

    """
    ABSOLUTE = auto()
    RELATIVE = auto()


class GeometryFactory:
    """ GeometryFactory implements a factory design pattern and is used to produce:
    - rectangular geometry
    - absolute cos-theta geometry
    - relative cos-theta geometry

    """

    # A dictionary from geometry type to block type
    geometry_type_to_block = {1: AbsoluteCosThetaBlock,
                              2: RectangularBlock}

    # A dictionary from geometry type to block definition type
    geometry_type_to_block_definition = {1: AbsoluteCosThetaBlockDefinition,
                                         2: RectangularBlockDefinition}

    @classmethod
    def init_with_json(cls, json_file_path: str, cadata: CableDatabase) -> Type[Geometry]:
        """ Class method initializing a Geometry instance from a JSON file.

        :param json_file_path: a path to a json file
        :param cadata: a CableDatabase instance
        :return: initialized geometry instance
        """
        json_content = cls.read_json_file(json_file_path)
        block_dct_defs = json_content['block_defs']
        layer_dct_defs = json_content['layer_defs']
        r_aperture = json_content.get('r_aperture', None)
        return cls.init_with_dict(block_dct_defs, layer_dct_defs, cadata, r_aperture=r_aperture)

    @staticmethod
    def read_json_file(json_file_path: str) -> dict:
        """ Static method reading a json file and returning a list of dictionaries with block definitions.

        :param json_file_path: a path to a json file
        :return: a list of dictionaries with geometry definition (block definition)
        """
        with open(json_file_path) as f:
            return json.load(f)

    @classmethod
    def init_with_dict(cls,
                       block_dct_defs: List[Dict],
                       layer_dct_defs: List[Dict],
                       cadata: CableDatabase,
                       r_aperture=None) -> Type[Geometry]:
        """ Class method initializing a Geometry instance from a list of dictionaries with block definition.

        :param block_dct_defs: a list of dictionaries with geometry definition (block definition)
        :param layer_dct_defs: a list of dictionaries with layer definitions
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized geometry instance
        """
        geom_type = cls.retrieve_geometry_type_dict(block_dct_defs)

        if geom_type == GeometryType.ABSOLUTE:
            return cls.init_absolute_with_dict(block_dct_defs, layer_dct_defs, cadata, r_aperture=r_aperture)

        if geom_type == GeometryType.RELATIVE:
            return cls.init_relative_with_dict(block_dct_defs, layer_dct_defs, cadata, r_aperture=r_aperture)

    @staticmethod
    def retrieve_geometry_type_dict(block_dct_defs: List[Dict]) -> GeometryType:
        """ Static method returning a geometry type enumeration for a given list of block definitions.
        An AttributeError is raised in case of inconsistencies in the definition.

        :param block_dct_defs: list of block definitions
        :return: a geometry type enumeration
        """
        if all(['alpha_r' in dct.keys() for dct in block_dct_defs]):
            return GeometryType.RELATIVE
        elif any(['alpha_r' in dct.keys() for dct in block_dct_defs]):
            raise AttributeError(
                'Error, inconsistent geometry definition. '
                'The geometry definition should consist of either all relative definitions or none.')
        else:
            return GeometryType.ABSOLUTE

    @classmethod
    def init_absolute_with_dict(cls,
                                block_defs: List[Dict],
                                layer_dct_defs: List[Dict],
                                cadata: CableDatabase,
                                r_aperture=None) -> Type[Geometry]:
        """ Static method initializing an absolute geometry (either rectangular or cos-theta) from a list of block
        definitions.

        :param block_defs: a list of block definitions
        :param layer_dct_defs: a list of dictionaries with layer definitions
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized absolute geometry instance
        """
        blocks = []
        for block_def in block_defs:
            BlockClass = GeometryFactory.geometry_type_to_block[block_def['type']]
            BlockDefinitionClass = GeometryFactory.geometry_type_to_block_definition[block_def['type']]
            block_abs = BlockDefinitionClass(**block_def)
            block = BlockClass(block_def=block_abs,
                               cable_def=cadata.get_cable_definition(block_abs.condname),
                               insul_def=cadata.get_insul_definition(block_abs.condname),
                               strand_def=cadata.get_strand_definition(block_abs.condname),
                               conductor_def=cadata.get_conductor_definition(block_abs.condname))

            blocks.append(block)

        if r_aperture:
            layer_defs = cls.init_slotted_layer_defs_with_dict(layer_dct_defs)
            return SlottedGeometry(r_aperture=r_aperture, blocks=blocks, layer_defs=layer_defs)
        else:
            layer_defs = cls.init_layer_defs_with_dict(layer_dct_defs)
            return Geometry(blocks=blocks, layer_defs=layer_defs)

    @staticmethod
    def init_slotted_layer_defs_with_dict(layer_dct_defs: List[Dict]) -> List[SlottedLayerDefinition]:
        """ Static method initializing a list of slotted layer definitions from a dataframe.

        :param layer_dct_defs: a list with layer definitions
        :return: a list of layer definitions
        """
        return [SlottedLayerDefinition(**layer_dct_def) for layer_dct_def in layer_dct_defs]

    @staticmethod
    def init_layer_defs_with_dict(layer_dct_defs: List[Dict]) -> List[LayerDefinition]:
        """ Static method initializing a list of layer definitions from a dataframe.

        :param layer_dct_defs: a list with layer definitions
        :return: a list of layer definitions
        """
        return [LayerDefinition(**layer_dct_def) for layer_dct_def in layer_dct_defs]

    @classmethod
    def init_relative_with_dict(cls,
                                block_dct_defs: List[Dict],
                                layer_dct_defs: List[Dict],
                                cadata: CableDatabase,
                                r_aperture=None) -> Geometry:
        """ Static method initializing an absolute cos-theta geometry from a list of block definitions.

        :param block_dct_defs: a list of block definitions
        :param layer_dct_defs: a list of dictionaries with layer definitions
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized relative geometry instance
        """
        blocks = []
        for block_def in block_dct_defs:
            block_rel = RelativeCosThetaBlockDefinition(**block_def)
            block = RelativeCosThetaBlock(block_def=block_rel,
                                          cable_def=cadata.get_cable_definition(block_rel.condname),
                                          insul_def=cadata.get_insul_definition(block_rel.condname),
                                          strand_def=cadata.get_strand_definition(block_rel.condname),
                                          conductor_def=cadata.get_conductor_definition(block_rel.condname))
            blocks.append(block)

        if r_aperture:
            layer_defs = cls.init_slotted_layer_defs_with_dict(layer_dct_defs)
            return SlottedRelativeCosThetaGeometry(r_aperture=r_aperture, blocks=blocks, layer_defs=layer_defs)
        else:
            layer_defs = cls.init_layer_defs_with_dict(layer_dct_defs)
            return RelativeCosThetaGeometry(blocks=blocks, layer_defs=layer_defs)

    @classmethod
    def init_with_data(cls, data_file_path: str, cadata: CableDatabase, r_aperture=None) -> Geometry:
        """ Class method initializing a Geometry instance from a DATA ROXIE file.

        :param data_file_path: a path to a json file
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized geometry instance
        """
        block_df = RoxieAPI.read_bottom_header_table(data_file_path, keyword='BLOCK')
        layer_df = RoxieAPI.read_nested_bottom_header_table(data_file_path, keyword='LAYER')
        return cls.init_with_df(block_df, layer_df, cadata, r_aperture=r_aperture)

    @classmethod
    def init_with_csv(cls,
                      block_csv_file_path: str,
                      layer_csv_file_path: str,
                      cadata: CableDatabase,
                      r_aperture=None) -> Geometry:
        """ Class method initializing a Geometry instance from a CSV file.

        :param block_csv_file_path: a path to a csv file with block definitions
        :param layer_csv_file_path: a path to a csv file with layer definitions
        :param cadata: a CableDatabase instance
        :return: initialized geometry instance
        """
        block_df = pd.read_csv(block_csv_file_path, index_col=0)
        layer_df = pd.read_csv(layer_csv_file_path, index_col=0)
        return cls.init_with_df(block_df, layer_df, cadata, r_aperture=r_aperture)

    @classmethod
    def init_with_df(cls, block_df: pd.DataFrame, layer_df, cadata: CableDatabase, r_aperture=None) -> Geometry:
        """ Class method initializing a Geometry instance from a dataframe with block definition.

        :param block_df: a dataframe with geometry definition (block definition)
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized geometry instance
        """
        geom_type = cls.retrieve_geometry_type_df(block_df)
        if geom_type == GeometryType.ABSOLUTE:
            return cls.init_absolute_with_df(block_df, layer_df, cadata, r_aperture=r_aperture)

        if geom_type == GeometryType.RELATIVE:
            return cls.init_relative_with_df(block_df, layer_df, cadata, r_aperture=r_aperture)

    @staticmethod
    def retrieve_geometry_type_df(block_df: pd.DataFrame) -> "GeometryType":
        """ Static method returning a geometry type enumeration for a given dataframe with block definitions.
        An AttributeError is raised in case of inconsistencies in the definition.

        :param block_defs: list of block definitions
        :return: a geometry type enumeration
        """
        if ('alpha_r' in block_df.columns) and ('phi_r' in block_df.columns):
            return GeometryType.RELATIVE
        elif ('alpha_r' in block_df.columns) or ('phi_r' in block_df.columns):
            raise AttributeError('Error, inconsistent geometry definition')
        else:
            return GeometryType.ABSOLUTE

    @classmethod
    def init_absolute_with_df(cls,
                              block_df: pd.DataFrame,
                              layer_df: pd.DataFrame,
                              cadata: CableDatabase,
                              r_aperture=None) -> Geometry:
        """ Static method initializing an absolute geometry (either rectangular or cos-theta) from a dataframe with
        block definitions.

        :param block_df: a dataframe with block definitions
        :param layer_defs: a dataframe with layer definitions
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized absolute geometry instance
        """
        blocks = []
        for _, row in block_df.iterrows():
            BlockClass = GeometryFactory.geometry_type_to_block[row['type']]
            BlockDefinitionClass = GeometryFactory.geometry_type_to_block_definition[row['type']]
            if row['type'] == 2:
                row = row.rename(BlockClass.roxie_to_magnum_dct)

            block_def = BlockDefinitionClass(**row.to_dict())
            block = BlockClass(block_def=block_def,
                               cable_def=cadata.get_cable_definition(block_def.condname),
                               insul_def=cadata.get_insul_definition(block_def.condname),
                               strand_def=cadata.get_strand_definition(block_def.condname),
                               conductor_def=cadata.get_conductor_definition(block_def.condname))

            blocks.append(block)

        if r_aperture:
            layer_defs = cls.init_slotted_layer_defs_with_df(layer_df)
            return SlottedGeometry(blocks=blocks, layer_defs=layer_defs, r_aperture=r_aperture)
        else:
            layer_defs = cls.init_layer_defs_with_df(layer_df)
            return Geometry(blocks=blocks, layer_defs=layer_defs)

    @staticmethod
    def init_slotted_layer_defs_with_df(layer_df: pd.DataFrame) -> List[SlottedLayerDefinition]:
        """ Static method initializing a list of slotted layer definitions from a dataframe.

        :param layer_df: a dataframe with layer definitions
        :return: a list of layer definitions
        """
        return [SlottedLayerDefinition(**row.to_dict()) for _, row in layer_df.iterrows()]

    @staticmethod
    def init_layer_defs_with_df(layer_df: pd.DataFrame) -> List[LayerDefinition]:
        """ Static method initializing a list of layer definitions from a dataframe.

        :param layer_df: a dataframe with layer definitions
        :return: a list of layer definitions
        """
        return [LayerDefinition(**row.to_dict()) for _, row in layer_df.iterrows()]

    @classmethod
    def init_relative_with_df(cls,
                              block_df: pd.DataFrame,
                              layer_df: pd.DataFrame,
                              cadata: CableDatabase,
                              r_aperture=None) -> Geometry:
        """ Static method initializing an absolute cos-theta geometry from a dataframe with block definitions.

        :param block_df: a dataframe with block definitions
        :param layer_df: a dataframe with layer definitions
        :param cadata: a CableDatabase instance
        :param r_aperture: aperture radius in mm, None by default
        :return: initialized relative geometry instance
        """
        blocks = []
        for row_dict in block_df.to_dict('records'):
            block_rel = RelativeCosThetaBlockDefinition(**row_dict)

            block = RelativeCosThetaBlock(block_def=block_rel,
                                          cable_def=cadata.get_cable_definition(block_rel.condname),
                                          insul_def=cadata.get_insul_definition(block_rel.condname),
                                          strand_def=cadata.get_strand_definition(block_rel.condname),
                                          conductor_def=cadata.get_conductor_definition(block_rel.condname))

            blocks.append(block)

        if r_aperture:
            layer_defs = cls.init_slotted_layer_defs_with_df(layer_df)
            return SlottedRelativeCosThetaGeometry(blocks=blocks, layer_defs=layer_defs, r_aperture=r_aperture)
        else:
            layer_defs = cls.init_layer_defs_with_df(layer_df)
            return RelativeCosThetaGeometry(blocks=blocks, layer_defs=layer_defs)
