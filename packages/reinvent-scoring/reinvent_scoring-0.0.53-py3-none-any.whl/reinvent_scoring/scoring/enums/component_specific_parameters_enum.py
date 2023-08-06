

class ComponentSpecificParametersEnum:
    __SCIKIT = "scikit"
    __CLAB_INPUT_FILE = "clab_input_file"
    __DESCRIPTOR_TYPE = "descriptor_type"
    __TRANSFORMATION = "transformation"

    # structural components
    # ---------
    # AZDOCK
    __AZDOCK_CONFPATH = "configuration_path"
    __AZDOCK_DOCKERSCRIPTPATH = "docker_script_path"
    __AZDOCK_ENVPATH = "environment_path"
    __AZDOCK_DEBUG = "debug"

    # DockStream
    __DOCKSTREAM_CONFPATH = "configuration_path"
    __DOCKSTREAM_DOCKERSCRIPTPATH = "docker_script_path"
    __DOCKSTREAM_ENVPATH = "environment_path"
    __DOCKSTREAM_DEBUG = "debug"

    # AZGARD
    __AZGARD_CONFPATH = "configuration_path"
    __AZGARD_EXECUTORSCRIPTPATH = "executor_script_path"
    __AZGARD_ENVPATH = "environment_path"
    __AZGARD_VALUES_KEY = "values_key"
    __AZGARD_DEBUG = "debug"
    #######################

    __RAT_PK_PROPERTY = "rat_pk_property"
    __CLAB_TOP_20_VALUE = "clab_top_20_value"
    __ION_CLASS = "Ion class"
    __CONTAINER_TYPE = "container_type"

    __SMILES = "smiles"
    __MODEL_PATH = "model_path"

    @property
    def MODEL_PATH(self):
        return self.__MODEL_PATH

    @MODEL_PATH.setter
    def MODEL_PATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def SMILES(self):
        return self.__SMILES

    @SMILES.setter
    def SMILES(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def CONTAINER_TYPE(self):
        return self.__CONTAINER_TYPE

    @CONTAINER_TYPE.setter
    def CONTAINER_TYPE(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def ION_CLASS(self):
        return self.__ION_CLASS

    @ION_CLASS.setter
    def ION_CLASS(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def CLAB_TOP_20_VALUE(self):
        return self.__CLAB_TOP_20_VALUE

    @CLAB_TOP_20_VALUE.setter
    def CLAB_TOP_20_VALUE(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def RAT_PK_PROPERTY(self):
        return self.__RAT_PK_PROPERTY

    @RAT_PK_PROPERTY.setter
    def RAT_PK_PROPERTY(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZDOCK_DEBUG(self):
        return self.__AZDOCK_DEBUG

    @AZDOCK_DEBUG.setter
    def AZDOCK_DEBUG(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZDOCK_CONFPATH(self):
        return self.__AZDOCK_CONFPATH

    @AZDOCK_CONFPATH.setter
    def AZDOCK_CONFPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZDOCK_DOCKERSCRIPTPATH(self):
        return self.__AZDOCK_DOCKERSCRIPTPATH

    @AZDOCK_DOCKERSCRIPTPATH.setter
    def AZDOCK_DOCKERSCRIPTPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZDOCK_ENVPATH(self):
        return self.__AZDOCK_ENVPATH

    @AZDOCK_ENVPATH.setter
    def AZDOCK_ENVPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def DOCKSTREAM_DEBUG(self):
        return self.__DOCKSTREAM_DEBUG

    @DOCKSTREAM_DEBUG.setter
    def DOCKSTREAM_DEBUG(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def DOCKSTREAM_CONFPATH(self):
        return self.__DOCKSTREAM_CONFPATH

    @DOCKSTREAM_CONFPATH.setter
    def DOCKSTREAM_CONFPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def DOCKSTREAM_DOCKERSCRIPTPATH(self):
        return self.__DOCKSTREAM_DOCKERSCRIPTPATH

    @DOCKSTREAM_DOCKERSCRIPTPATH.setter
    def DOCKSTREAM_DOCKERSCRIPTPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def DOCKSTREAM_ENVPATH(self):
        return self.__DOCKSTREAM_ENVPATH

    @DOCKSTREAM_ENVPATH.setter
    def DOCKSTREAM_ENVPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZGARD_DEBUG(self):
        return self.__AZGARD_DEBUG

    @AZGARD_DEBUG.setter
    def AZGARD_DEBUG(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZGARD_CONFPATH(self):
        return self.__AZGARD_CONFPATH

    @AZGARD_CONFPATH.setter
    def AZGARD_CONFPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZGARD_EXECUTORSCRIPTPATH(self):
        return self.__AZGARD_EXECUTORSCRIPTPATH

    @AZGARD_EXECUTORSCRIPTPATH.setter
    def AZGARD_EXECUTORSCRIPTPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZGARD_VALUES_KEY(self):
        return self.__AZGARD_VALUES_KEY

    @AZGARD_VALUES_KEY.setter
    def AZGARD_VALUES_KEY(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def AZGARD_ENVPATH(self):
        return self.__AZGARD_ENVPATH

    @AZGARD_ENVPATH.setter
    def AZGARD_ENVPATH(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def TRANSFORMATION(self):
        return self.__TRANSFORMATION

    @TRANSFORMATION.setter
    def TRANSFORMATION(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def SCIKIT(self):
        return self.__SCIKIT

    @SCIKIT.setter
    def SCIKIT(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def CLAB_INPUT_FILE(self):
        return self.__CLAB_INPUT_FILE

    @CLAB_INPUT_FILE.setter
    def CLAB_INPUT_FILE(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")

    @property
    def DESCRIPTOR_TYPE(self):
        return self.__DESCRIPTOR_TYPE

    @DESCRIPTOR_TYPE.setter
    def DESCRIPTOR_TYPE(self, value):
        raise ValueError("Do not assign value to a ComponentSpecificParametersEnum field")
