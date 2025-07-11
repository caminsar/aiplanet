from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ModelParameter:
    """
    Describes a single parameter for a model.
    """
    def __init__(self, name: str, description: str, data_type: type, default_value: Any = None, required: bool = True, options: List[Any] = None):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.default_value = default_value
        self.required = required
        self.options = options # e.g., for dropdowns or specific choices

    def __repr__(self):
        return f"<ModelParameter(name='{self.name}', type={self.data_type.__name__})>"

class ModelInput:
    """
    Describes a single input for a model (e.g., a dataset, a timeseries).
    """
    def __init__(self, name: str, description: str, data_format: str, required: bool = True):
        # data_format could be 'csv', 'netcdf', 'geotiff', 'json_timeseries', 'data_record_list' etc.
        self.name = name
        self.description = description
        self.data_format = data_format
        self.required = required

    def __repr__(self):
        return f"<ModelInput(name='{self.name}', format='{self.data_format}')>"

class ModelOutput:
    """
    Describes a single output of a model.
    """
    def __init__(self, name: str, description: str, data_format: str):
        self.name = name
        self.description = description
        self.data_format = data_format # Similar to ModelInput data_format

    def __repr__(self):
        return f"<ModelOutput(name='{self.name}', format='{self.data_format}')>"


class ScientificModel(ABC):
    """
    Abstract Base Class for all scientific models integrated into the platform.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Returns the unique name of the model."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Returns a brief description of the model."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Returns the version of the model."""
        pass

    @abstractmethod
    def get_parameters_definition(self) -> Dict[str, ModelParameter]:
        """
        Returns a dictionary defining the parameters the model accepts.
        Keys are parameter names, values are ModelParameter objects.
        """
        pass

    @abstractmethod
    def get_inputs_definition(self) -> Dict[str, ModelInput]:
        """
        Returns a dictionary defining the input datasets/files the model requires.
        Keys are input names, values are ModelInput objects.
        """
        pass

    @abstractmethod
    def get_outputs_definition(self) -> Dict[str, ModelOutput]:
        """
        Returns a dictionary defining the outputs the model produces.
        Keys are output names, values are ModelOutput objects.
        """
        pass

    @abstractmethod
    def setup(self, parameters: Dict[str, Any], model_specific_config_path: str = None) -> None:
        """
        Configures the model with the given parameters.
        'model_specific_config_path' could point to a file with further detailed settings if needed.
        This method should prepare the model for execution but not run it.
        """
        pass

    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the model with the provided inputs.
        'inputs' is a dictionary where keys match those defined in get_inputs_definition(),
        and values are the actual data (e.g., file paths, dataframes, DataRecord lists).

        Returns a dictionary of outputs, where keys match those in get_outputs_definition(),
        and values are the results (e.g., file paths to output files, processed data).
        """
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validates if the provided parameters are suitable for the model."""
        # Basic implementation could check types, ranges, required fields
        definitions = self.get_parameters_definition()
        for name, param_def in definitions.items():
            if param_def.required and name not in parameters:
                print(f"Error: Required parameter '{name}' is missing.")
                return False
            if name in parameters:
                value = parameters[name]
                if not isinstance(value, param_def.data_type):
                    print(f"Error: Parameter '{name}' expected type {param_def.data_type.__name__} but got {type(value).__name__}.")
                    return False
                if param_def.options and value not in param_def.options:
                    print(f"Error: Parameter '{name}' value '{value}' is not in allowed options: {param_def.options}.")
                    return False
        return True

    @abstractmethod
    def cleanup(self) -> None:
        """Performs any necessary cleanup after model execution (e.g., deleting temporary files)."""
        pass

if __name__ == '__main__':
    print("ScientificModel interface and helper classes defined.")
    # This file primarily defines interfaces, so direct execution doesn't do much.
    # Example usage would involve creating a concrete implementation of ScientificModel.

    class DummyHydrologicalModel(ScientificModel):
        def get_name(self) -> str: return "DummyHydroModel"
        def get_description(self) -> str: return "A placeholder hydrological model."
        def get_version(self) -> str: return "0.0.1"

        def get_parameters_definition(self) -> Dict[str, ModelParameter]:
            return {
                "rainfall_multiplier": ModelParameter("rainfall_multiplier", "Multiplier for rainfall input", float, 1.0),
                "simulation_duration": ModelParameter("simulation_duration", "Duration in days", int, 7)
            }

        def get_inputs_definition(self) -> Dict[str, ModelInput]:
            return {
                "rainfall_data": ModelInput("rainfall_data", "Path to rainfall timeseries CSV", "csv_filepath"),
                "catchment_shapefile": ModelInput("catchment_shapefile", "Path to catchment boundary", "shp_filepath", required=False)
            }

        def get_outputs_definition(self) -> Dict[str, ModelOutput]:
            return {
                "outflow_timeseries": ModelOutput("outflow_timeseries", "Path to output flow timeseries CSV", "csv_filepath"),
                "summary_report": ModelOutput("summary_report", "Path to a text summary report", "txt_filepath")
            }

        def setup(self, parameters: Dict[str, Any], model_specific_config_path: str = None) -> None:
            if not self.validate_parameters(parameters):
                raise ValueError("Invalid parameters for model setup.")
            self.params = parameters
            print(f"Model '{self.get_name()}' setup with parameters: {self.params}")
            if model_specific_config_path:
                print(f"Using model specific config: {model_specific_config_path}")


        def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            print(f"Model '{self.get_name()}' running with inputs: {inputs}")
            # Simulate model execution
            output_dir = inputs.get("output_directory", ".")
            outflow_file = f"{output_dir}/outflow_{inputs.get('rainfall_data', 'default_rain').split('/')[-1]}"
            summary_file = f"{output_dir}/summary_{inputs.get('rainfall_data', 'default_rain').split('/')[-1]}.txt"

            with open(outflow_file, 'w') as f:
                f.write("time,flow\n0,0\n1,10\n2,12") # Dummy data
            with open(summary_file, 'w') as f:
                f.write(f"Model run completed with params: {self.params}. Rainfall input: {inputs.get('rainfall_data')}")

            print(f"Model '{self.get_name()}' finished. Outputs generated.")
            return {
                "outflow_timeseries": outflow_file,
                "summary_report": summary_file
            }

        def cleanup(self) -> None:
            print(f"Model '{self.get_name()}' cleanup.")

    # Test the dummy model
    dummy_model = DummyHydrologicalModel()
    print(f"\nTesting model: {dummy_model.get_name()} v{dummy_model.get_version()}")
    print(f"Description: {dummy_model.get_description()}")
    print(f"Parameters: {dummy_model.get_parameters_definition()}")
    print(f"Inputs: {dummy_model.get_inputs_definition()}")
    print(f"Outputs: {dummy_model.get_outputs_definition()}")

    try:
        valid_params = {"rainfall_multiplier": 1.2, "simulation_duration": 10}
        dummy_model.setup(parameters=valid_params)
        # dummy_model.setup(parameters={"rainfall_multiplier": "wrong_type", "simulation_duration": 10}) # Test validation

        mock_inputs = {
            "rainfall_data": "path/to/my/rain_series.csv",
            "catchment_shapefile": "path/to/my/catchment.shp",
            "output_directory": "temp_model_outputs" # Example of passing operational params
        }
        import os
        if not os.path.exists("temp_model_outputs"): os.makedirs("temp_model_outputs")

        results = dummy_model.run(inputs=mock_inputs)
        print(f"Model results: {results}")
        dummy_model.cleanup()

    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
