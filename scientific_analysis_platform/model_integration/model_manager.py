from typing import Dict, List, Any, Type
from .model_interface import ScientificModel # Assuming model_interface.py is in the same directory

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
        # Perform basic validation
        if not issubclass(model_class, ScientificModel):
            raise TypeError(f"Model class '{model_class.__name__}' must inherit from ScientificModel.")

        # Instantiate temporarily to get name (or could make get_name a static/class method)
        try:
            temp_instance = model_class()
            model_name = temp_instance.get_name()
        except Exception as e:
            # This might happen if __init__ of the model class requires arguments.
            # For simplicity, we assume a no-arg constructor for registration purposes,
            # or that get_name can be accessed without full instantiation.
            # A more robust solution might involve class-level attributes for metadata.
            print(f"Warning: Could not instantiate '{model_class.__name__}' to get its name during registration: {e}. Using class name as fallback.")
            model_name = model_class.__name__


        if model_name in self._registered_models:
            print(f"Warning: Model with name '{model_name}' is already registered. Overwriting.")

        self._registered_models[model_name] = model_class
        print(f"Model '{model_name}' (class: {model_class.__name__}) registered successfully.")

    def discover_models(self, discovery_paths: List[str] = None) -> None:
        """
        Discovers models from specified paths or pre-defined locations.
        This is a placeholder for a more sophisticated discovery mechanism
        (e.g., using importlib to find classes inheriting from ScientificModel).
        For now, models must be explicitly registered.
        """
        print(f"Model discovery initiated (currently relies on explicit registration). Paths: {discovery_paths}")
        # In a real implementation, this would scan modules in discovery_paths
        # for classes that are subclasses of ScientificModel.
        # Example using importlib (conceptual):
        # for path in discovery_paths:
        #   for module_name in find_modules_in_path(path):
        #     module = importlib.import_module(module_name)
        #     for attribute_name in dir(module):
        #       attribute = getattr(module, attribute_name)
        #       if isinstance(attribute, type) and issubclass(attribute, ScientificModel) and attribute is not ScientificModel:
        #         self.register_model(attribute)
        pass

    def list_available_models(self) -> List[Dict[str, str]]:
        """Returns a list of available models with their names and descriptions."""
        available = []
        for name, model_class in self._registered_models.items():
            try:
                # Temporarily instantiate to get metadata. Consider class/static methods for this.
                instance = model_class()
                available.append({
                    "name": instance.get_name(),
                    "description": instance.get_description(),
                    "version": instance.get_version()
                })
            except Exception as e:
                print(f"Could not retrieve details for model class {model_class.__name__}: {e}")
                available.append({
                    "name": name, # Fallback to registered name
                    "description": "Error retrieving description",
                    "version": "N/A"
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
            instance = model_class() # Assumes a no-argument constructor for instantiation
            print(f"Created instance of model '{model_name}'.")
            return instance
        except Exception as e:
            print(f"Error instantiating model '{model_name}': {e}")
            raise # Re-raise the exception as instantiation failed

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
            # Potentially re-raise or handle more gracefully
            raise
        finally:
            print(f"Cleaning up model '{model_name}'.")
            model_instance.cleanup()


if __name__ == '__main__':
    print("ModelManager class defined.")

    # --- Example Usage ---
    # (Requires a concrete ScientificModel implementation, e.g., DummyHydrologicalModel from model_interface.py)
    # For demonstration, let's redefine a minimal DummyModel here or import it.

    class SimpleDummyModel(ScientificModel):
        def get_name(self) -> str: return "SimpleDummy"
        def get_description(self) -> str: return "A very simple dummy model for manager testing."
        def get_version(self) -> str: return "1.0"
        def get_parameters_definition(self) -> Dict[str, Any]: return {"param1": None} # Simplified
        def get_inputs_definition(self) -> Dict[str, Any]: return {"input1": None} # Simplified
        def get_outputs_definition(self) -> Dict[str, Any]: return {"output1": None} # Simplified
        def setup(self, parameters: Dict[str, Any], model_specific_config_path: str = None) -> None:
            self.params = parameters
            print(f"SimpleDummyModel setup with: {self.params}. Config path: {model_specific_config_path}")
        def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            print(f"SimpleDummyModel running with: {inputs}")
            return {"output1": f"processed_{inputs.get('input1', 'default_input')}_with_{self.params.get('param1', 'default_param')}"}
        def validate_parameters(self, parameters: Dict[str, Any]) -> bool: return True # Simplified
        def cleanup(self) -> None: print("SimpleDummyModel cleanup.")

    manager = ModelManager()
    manager.register_model(SimpleDummyModel)
    # manager.register_model(str) # Test type error

    print("\nAvailable models:")
    for model_info in manager.list_available_models():
        print(f"  - {model_info['name']} (v{model_info['version']}): {model_info['description']}")

    print("\nTesting model execution:")
    try:
        model_params = {"param1": "value1"}
        model_inputs = {"input1": "data_A.csv"}
        # Example of model_specific_config_path
        config_file = "path/to/optional/specific_model_config.ini"

        results = manager.run_model("SimpleDummy", model_params, model_inputs, model_specific_config_path=config_file)
        print(f"Results from manager: {results}")
    except Exception as e:
        print(f"Error during manager execution test: {e}")

    print("\nTesting getting a model instance directly:")
    try:
        instance = manager.get_model_instance("SimpleDummy")
        print(f"Successfully got instance: {type(instance)}, Name: {instance.get_name()}")
        # You could then call instance.setup(), instance.run() manually if needed
    except Exception as e:
        print(f"Error getting instance: {e}")

    print("\nTesting non-existent model:")
    try:
        manager.run_model("NonExistentModel", {}, {})
    except ValueError as ve:
        print(f"Caught expected error: {ve}")
