from typing import Dict, List, Any, Type
from .model_interface import ScientificModel # Assuming model_interface.py is in the same directory
# Import the new conceptual model wrappers
from .models.maxent_model import MaxEntModelWrapper
from .models.hydro_models import SWATModelWrapper, VICModelWrapper


class ModelManager:
    """
    Manages the registration, discovery, and execution of scientific models.
    """

    def __init__(self):
        self._registered_models: Dict[str, Type[ScientificModel]] = {}
        print("ModelManager initialized.")

    def register_model(self, model_class: Type[ScientificModel]) -> None:
        """
        Registers a model class with the manager.
        The model class itself (not an instance) is stored.
        Instances will be created when needed.
        """
        if not issubclass(model_class, ScientificModel):
            raise TypeError(f"Model class '{model_class.__name__}' must inherit from ScientificModel.")

        # Instantiate temporarily to get name.
        # This assumes model's __init__ can be called without args for this purpose,
        # or get_name could be a classmethod.
        try:
            # For wrappers that might create directories on init, this might have side effects.
            # Consider if get_name/get_description should be class methods to avoid instantiation here.
            temp_instance = model_class()
            model_name = temp_instance.get_name()
        except Exception as e:
            print(f"Warning: Could not instantiate '{model_class.__name__}' to get its name during registration: {e}. Using class name as fallback.")
            model_name = model_class.__name__


        if model_name in self._registered_models:
            print(f"Warning: Model with name '{model_name}' is already registered. Overwriting with {model_class.__name__}.")

        self._registered_models[model_name] = model_class
        print(f"Model '{model_name}' (class: {model_class.__name__}) registered successfully.")

    def discover_models(self, discovery_paths: List[str] = None, module_prefix: str = "") -> None:
        """
        Discovers models from specified paths or pre-defined locations.
        This is a placeholder for a more sophisticated discovery mechanism
        (e.g., using importlib to find classes inheriting from ScientificModel).
        For now, models must be explicitly registered.

        :param discovery_paths: List of directory paths to scan for model modules.
        :param module_prefix: Prefix for module names if they are part of a package (e.g., "scientific_analysis_platform.model_integration.models.").
        """
        print(f"Model discovery initiated (currently relies on explicit registration or direct import). Paths: {discovery_paths}")
        # Example conceptual logic using importlib:
        # import importlib
        # import inspect
        # import os
        # import sys
        #
        # if discovery_paths:
        #     for path in discovery_paths:
        #         if path not in sys.path:
        #             sys.path.append(path) # Ensure path is discoverable
        #         for filename in os.listdir(path):
        #             if filename.endswith(".py") and not filename.startswith("__"):
        #                 module_name_short = filename[:-3]
        #                 full_module_name = f"{module_prefix}{module_name_short}" if module_prefix else module_name_short
        #                 try:
        #                     module = importlib.import_module(full_module_name)
        #                     for name, obj in inspect.getmembers(module):
        #                         if inspect.isclass(obj) and issubclass(obj, ScientificModel) and obj is not ScientificModel:
        #                             self.register_model(obj)
        #                 except ImportError as e:
        #                     print(f"Could not import module {full_module_name}: {e}")
        #                 except Exception as e:
        #                     print(f"Error processing module {full_module_name}: {e}")
        pass


    def list_available_models(self) -> List[Dict[str, str]]:
        """Returns a list of available models with their names and descriptions."""
        available = []
        for name, model_class in self._registered_models.items():
            try:
                # Temporarily instantiate to get metadata.
                instance = model_class() # This might have side effects for models that create dirs on init
                available.append({
                    "name": instance.get_name(), # Should match 'name' key
                    "description": instance.get_description(),
                    "version": instance.get_version(),
                    "class": model_class.__name__
                })
            except Exception as e:
                print(f"Could not retrieve details for model class {model_class.__name__}: {e}")
                available.append({
                    "name": name,
                    "description": "Error retrieving description",
                    "version": "N/A",
                    "class": model_class.__name__
                })
        return available

    def get_model_instance(self, model_name: str) -> ScientificModel:
        """
        Retrieves an instance of a registered model by its name.
        """
        if model_name not in self._registered_models:
            raise ValueError(f"Model '{model_name}' not found. Available models: {list(self._registered_models.keys())}")

        model_class = self._registered_models[model_name]
        try:
            instance = model_class()
            print(f"Created instance of model '{model_name}'.")
            return instance
        except Exception as e:
            print(f"Error instantiating model '{model_name}': {e}")
            raise

    def run_model(self, model_name: str, parameters: Dict[str, Any], inputs: Dict[str, Any], model_specific_config_path: str = None) -> Dict[str, Any]:
        """
        Initializes, sets up, runs, and cleans up a specified model.
        """
        print(f"Attempting to run model '{model_name}'...")
        model_instance = self.get_model_instance(model_name)

        try:
            print(f"Setting up model '{model_name}' with parameters: {parameters}")
            model_instance.setup(parameters, model_specific_config_path)

            print(f"Executing model '{model_name}' with inputs: {inputs}")
            results = model_instance.run(inputs)
            print(f"Model '{model_name}' execution completed. Results: {results}")

            return results
        except Exception as e:
            print(f"An error occurred during the lifecycle of model '{model_name}': {e}")
            raise
        finally:
            print(f"Cleaning up model '{model_name}'.")
            model_instance.cleanup()


if __name__ == '__main__':
    print("ModelManager class defined.")

    # --- Example Usage ---
    # This demonstrates registering the conceptual models.
    # Their actual run methods are just simulations.

    class SimpleDummyModel(ScientificModel): # Keep this for basic manager testing
        def get_name(self) -> str: return "SimpleDummyTestModel"
        def get_description(self) -> str: return "A very simple dummy model for manager testing."
        def get_version(self) -> str: return "1.0"
        def get_parameters_definition(self) -> Dict[str, Any]: return {"param1": ModelParameter("param1", "A dummy param", str, "default_val")}
        def get_inputs_definition(self) -> Dict[str, Any]: return {"input1": ModelInput("input1", "Dummy input", "text")}
        def get_outputs_definition(self) -> Dict[str, Any]: return {"output1": ModelOutput("output1", "Dummy output", "text")}
        def setup(self, parameters: Dict[str, Any], model_specific_config_path: str = None) -> None:
            self.params = parameters
            print(f"SimpleDummyModel '{self.get_name()}' setup with: {self.params}. Config path: {model_specific_config_path}")
        def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            print(f"SimpleDummyModel '{self.get_name()}' running with: {inputs}")
            return {"output1": f"processed_{inputs.get('input1', 'default_input')}_with_{self.params.get('param1', 'default_param')}"}
        def validate_parameters(self, parameters: Dict[str, Any]) -> bool: return True
        def cleanup(self) -> None: print(f"SimpleDummyModel '{self.get_name()}' cleanup.")

    manager = ModelManager()
    manager.register_model(SimpleDummyModel)

    # Register the new conceptual models
    # These models might create temp directories on instantiation if their __init__ does so.
    # This is a side effect of calling model_class() in list_available_models or register_model.
    # Ideally, metadata methods (get_name, etc.) should be classmethods to avoid this.
    print("\nRegistering conceptual models...")
    try:
        manager.register_model(MaxEntModelWrapper)
        manager.register_model(SWATModelWrapper)
        manager.register_model(VICModelWrapper)
    except Exception as e:
        print(f"Error during registration of conceptual models: {e}")
        print("This might be due to file operations in their __init__ if run in a restricted env.")

    print("\nAvailable models after registering conceptual ones:")
    for model_info in manager.list_available_models():
        print(f"  - {model_info['name']} (v{model_info['version']}, class: {model_info['class']}): {model_info['description']}")

    print("\nTesting execution of SimpleDummyTestModel via manager:")
    try:
        model_params = {"param1": "test_value"}
        model_inputs = {"input1": "sample_data.txt"}
        results = manager.run_model("SimpleDummyTestModel", model_params, model_inputs)
        print(f"Results from SimpleDummyTestModel: {results}")
    except Exception as e:
        print(f"Error during SimpleDummyTestModel execution test: {e}")

    # Note: Running the conceptual wrappers (MaxEnt, SWAT, VIC) via manager.run_model()
    # would execute their simulated run methods. This requires their dummy input files/paths
    # to be set up as expected by their `setup` and `run` methods, which was shown
    # in their respective `if __name__ == '__main__'` blocks.
    # For brevity, not repeating those full setups here, but they *could* be run.

    print("\nModelManager example finished.")
    # Cleanup for directories created by conceptual models during testing
    import shutil
    import os
    # Directories created by the __init__ of the wrapper models if they were instantiated
    if os.path.exists("temp_maxent_outputs"): shutil.rmtree("temp_maxent_outputs", ignore_errors=True)
    if os.path.exists("temp_swat_workspace"): shutil.rmtree("temp_swat_workspace", ignore_errors=True)
    if os.path.exists("temp_vic_workspace"): shutil.rmtree("temp_vic_workspace", ignore_errors=True)
    print("Cleaned up temporary model directories if they were created by instantiation.")
